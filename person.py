import pygame, math
import random as ra
"status can be either 'healthy', 'sick', or 'recovered'"

"""
    high social distancing people 75% of people are distancing 
    medium social distancing 50% of people are distancing
    No social distancing 25% of people are distancing
"""

green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)


class person:
      
    def __init__(self, x, y, status, socialDistancing):
        self.x = x
        self.y = y
        self.status = status
        self.velocityOfX = 0
        self.velocityOfY = 0
        self.socialDistancing = socialDistancing
        self.radius = 7
        self.recoveryTime = 200
        self.isSick = 0
        self.leftBounds = 2
        self.downBounds = 795
        self.upBounds = 2
        self.rightBounds = 1195
        self.recoveredCount = 0
        self.colour = 0
        self.distance = 0
        self.healthyCount = 200
        
        if not self.socialDistancing:
            while -0.50 < self.velocityOfX < 0.50 or -0.50 < self.velocityOfY < .50:
                self.velocityOfX = ra.uniform(-5, 5)
                self.velocityOfY = ra.uniform(-5, 5)
        else:#if we are social distancing
            self.velocityOfX = 0
            self.velocityOfY = 0
 
    def drawPerson(self, screen):
        if self.status == 'sick':
            self.colour = red
        if self.status == 'recovered':
            self.colour = blue
        if self.status == 'dead':
            self.colour = black
        if self.status == 'healthy':
            self.colour = green
        pygame.draw.circle(screen, self.colour, (round(self.x), round(self.y)), self.radius)
    
    #roll a random number between 1/100 to give ourselves
    #1/100 = .01 and we have three oportunities making it
    #a 0.03 chance of death
    def isDead(self):
        death = ra.randint(1, 100)
        if death == 1 or death == 2 or death == 3:
           return True
        return False
    
    def movePerson(self):
        if not self.socialDistancing:
            self.x += (self.velocityOfX)
            self.y += (self.velocityOfY)
    
    def updatePerson(self,people,wall):
        self.movePerson()
        self.checkCollisionWithBorder(self.leftBounds,self.rightBounds,
                                      self.upBounds,self.downBounds)
        if wall:
            self.checkCollisionWithWall(wall)
        for person in people:
            #check that the person in the list of the people is not ourselves
            if self != person:
                if self.iscollidingWithOther(person):
                    if self.status == 'sick' and person.status == 'healthy':
                        person.status = 'sick'
                        return True
                    elif self.status == 'healthy' and person.status == 'sick':
                          self.status = 'sick'
                          return True
        self.checkRecovery()
   
    def checkRecovery(self):
        if self.status == 'sick':
            self.isSick += 1
            if self.isSick == self.recoveryTime:
                self.status = 'recovered'
                if self.isDead():
                    self.status = 'dead'
                return True
        return False
             
    def checkCollisionWithBorder(self,leftBounds = 0,rightBounds = 0,upBounds = 0,downBounds = 0):
        #if we hit the leftside of the boarder
        if self.x - self.radius < leftBounds and self.velocityOfX < 0:
            self.velocityOfX *= -1
        #if we hit the rightside of the border
        elif self.x + self.radius > rightBounds and self.velocityOfX > 0:
            self.velocityOfX *= -1
        #if we hit the bottom of the border
        elif self.y + self.radius > downBounds and self.velocityOfY > 0:
            self.velocityOfY *= -1
        #if we hit the top of the border
        elif self.y - self.radius < upBounds and self.velocityOfY < 0:
            self.velocityOfY *= -1
            
    def checkCollisionWithQuarintine(self,leftBounds,rightBounds,downBounds):
        if self.x >= leftBounds and self.x <= rightBounds and self.velocityOfY > 0:
            if self.y + self.radius > downBounds:
                self.velocityOfY *= -1
        elif self.x <= leftBounds and self.y >= downBounds:
            if self.x + self.radius > leftBounds and self.velocityOfX > 0:
                self.velocityOfX *= -1
            
    def checkCollisionWithWall(self,wall):
        rightBoundOfWall = 462
        if self.x + self.radius < rightBoundOfWall and self.y < wall.height:
            if self.x + self.radius > wall.x-2 and self.velocityOfX > 0:
                self.velocityOfX *= -1
        else:
            if self.x - self.radius < rightBoundOfWall and self.velocityOfX < 0 and self.y < wall.height:
                self.velocityOfX *= -1
        if self.x < rightBoundOfWall and  self.x >wall.x:
            if self.y - self.radius < wall.height:
                self.velocityOfY *=-1

   
    def iscollidingWithOther(self,otherPerson):
        if isinstance(otherPerson,person):
            #calculate distance betweeen two points by using c = sqrt(a**2 + b**2)
            self.distance = math.sqrt(
                ( (self.x - otherPerson.x )**2) + ((self.y - otherPerson.y)**2)
                )
            if  abs(self.distance) <= self.radius + otherPerson.radius:
                return True
            return False
            
    def __str__(self):
        return str(self.status) + str((self.x,self.y)) + " " + "social distancing " + str(self.socialDistancing)       

