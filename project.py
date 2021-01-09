import pygame
import random as ra
import time
from person import person

green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
grey = (230, 230, 230)
    
class Button:
    
    def __init__(self,width,height,text,colour,outline,screen,x,y):
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.outline = outline
        self.screen = screen
        self.x = x
        self.y = y
        self.clickedCounter = 0
    #size is a tuple
    #based on external idea from https://www.youtube.com/watch?v=4_9twnEduFA&t=176s&ab_channel=TechWithTim
    def drawButton(self,insideColour):
        pygame.draw.rect(self.screen, insideColour,(self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(self.screen,self.colour,(self.x,self.y,self.width,self.height))
        font = pygame.font.SysFont('comicsans',20)
        text = font.render(self.text,1,black)
        self.screen.blit(text, (self.x + (self.width/2 - (text.get_width()/2)),
                        self.y + (self.height/2 - (text.get_height()/2))))
    def isOntop(self,mouse):
        mouseX = mouse[0]
        mouseY = mouse[1]
        if mouseY >= self.y and mouseY <= self.y + self.height and mouseX >= self.x and mouseX <= self.x + self.width:
            self.colour = green
            return True
        self.colour = blue
        return False
    def __str__(self):
        return self.text + str(self.isClicked)
    
    
class Menu:
    
    def createButtons(self,screen):
        x = 400
        width = 400
        height = 80
        highSocialDistancingButton = Button(width, height, 'High Social Distancing', blue,
                                            None, screen, x, 200)
        mediumSocialDistancingButton = Button(width, height, 'Medium Social Distancing', blue,
                                            None, screen, x, 300)
        noSocialDistancingButton = Button(width, height, 'No Social Distancing', blue,
                                        None, screen, x, 400)
        socialBubblesButton = Button(width, height, 'Social Bubbles', blue,
                                    None, screen, x, 500)
        buttonList = [highSocialDistancingButton, mediumSocialDistancingButton,
                    noSocialDistancingButton, socialBubblesButton]
        return buttonList
    
    def intro(self,screen):
        intro = True
        buttonList = self.createButtons(screen)
        
        smallfont = pygame.font.SysFont(None, 30)
        checkMarkImg = pygame.image.load('checkmark.jpg')
        checkMarkImg = pygame.transform.scale(checkMarkImg,(112,112))
        checkMarkX = 900
        checkMarkY = 175
        
        while intro:
            socialDistancing = 'None'
            socialBubbles = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro = False
                screen.fill(white)
                for button in buttonList:
                    button.drawButton(black)
                    button.isOntop(pygame.mouse.get_pos())
                    if event.type == pygame.MOUSEBUTTONDOWN and button.isOntop(pygame.mouse.get_pos()):
                        button.clickedCounter += 1
                text = smallfont.render(
                'Welcome to my Pygame for Covid 19, Click The Buttons Below To Configure Your Options', True, black)
                screen.blit(text, [200, 150])
            if (buttonList[0].clickedCounter % 2) != 0:
                screen.blit(checkMarkImg, (checkMarkX, 175))
                socialDistancing = 'High' 
            if (buttonList[1].clickedCounter % 2) != 0:
                screen.blit(checkMarkImg, (checkMarkX, 275))
                socialDistancing = 'Medium'
            if (buttonList[2].clickedCounter % 2) != 0:
                screen.blit(checkMarkImg, (checkMarkX, 375))
                socialDistancing = 'None'
            if (buttonList[3].clickedCounter % 2) != 0:
                screen.blit(checkMarkImg, (checkMarkX, 475))
                socialBubbles = True
            pygame.display.update()
        return (socialDistancing,socialBubbles)

class Simulation:
    
    def __init__(self, width, height, Population, healthyCount, font,screen):
        self.width = width
        self.height = height
        self.Population = Population
        self.recoveredCount = 0
        self.sickCount = 0
        self.healthyCount = healthyCount
        self.font = font
        self.screen = screen
        self.running = True
        self.MAXFPS = 20
        self.newSickCount = 0
        self.deathCount = 0
        
    def showScore(self,x, y,count,string,colour):
        score = font.render(string + ' :'  + str(count), True, colour)
        screen.blit(score,(x,y))
         
    def initializePopulation(self,socialDistancingStr,people):
        minimum = 10
        patientZero = person(ra.randint(minimum, self.width),
                             ra.randint(minimum, self.height), 'sick', False)
        for i in range(self.Population - 1):
            socialDistancing = False
            if socialDistancingStr == 'Medium':  
                rolledNum = ra.randint(0,1)
                #half the people social distancing
                if rolledNum:
                    socialDistancing = True
            elif socialDistancingStr == 'High':
                rolledNum = ra.randint(0,3)
                if rolledNum:
                    socialDistancing = True        
            guy = (person(ra.randint(minimum, self.width),
                          ra.randint(minimum, self.height), 'healthy', socialDistancing))    
            people.append(guy)
            for person2 in people:
                while person2.iscollidingWithOther(guy):
                        people.remove(person2)
                        person2 = (person(ra.randint(minimum, self.width),
                                        ra.randint(minimum, self.height), 'healthy', socialDistancing))
                        people.append(person2)
        people.insert(0, patientZero)
        
    def runSimulation(self, people, socialBubbles):
        self.sickCount = 1
        wall = None
        if socialBubbles:
            wall = Wall(425, 0, 30, 800,self.screen)
        width = (self.width / 4)
        height = (self.height / 4)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(white)
            self.recoveredCount = 0
            self.deathCount = 0
            for person in people:
                if person.updatePerson(people,wall):
                    self.healthyCount -= 1
                    self.sickCount += 1
                if person.isSick == person.recoveryTime:
                    self.recoveredCount +=1
                    if person.status == 'dead':
                        self.deathCount += 1
                        self.recoveredCount -= 1
                person.drawPerson(screen)
            self.newSickCount = self.sickCount - self.recoveredCount - self.deathCount
            if socialBubbles:        
                wall.drawRectangle(self.healthyCount)
            self.showScore(10, 10, self.newSickCount, 'Sick', red)
            self.showScore(100, 10,self.healthyCount,'Healthy',green)
            self.showScore(215, 10, self.recoveredCount, 'Recovered',blue)
            self.showScore(350, 10, self.deathCount, 'Dead',black)
            pygame.display.flip()
            clock.tick(MAXFPS)
           
            pygame.display.update()
            
class Wall:
    
    def __init__(self,x,y,width,height,screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        
    def drawRectangle(self,delay):
        pygame.draw.rect(self.screen,black,(self.x-2,self.y-2,self.width+4,self.height+4))
        pygame.draw.rect(self.screen,white,(self.x,self.y,self.width,self.height))
        if delay<= 180:
            self.moveWall()
    
    def moveWall(self):
        self.height -= 1
#button for social distance high medium or none 
if __name__ == "__main__":         
    healthyCount = 199
    width = 1200
    height = 800
    testX = 10
    testY = 10
    Population = 200
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 16)
    running = True
    MAXFPS = 20
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width,height))

    sim = Simulation(width, height, Population, healthyCount, font,screen)
    menu = Menu()
    introResults = menu.intro(screen)
    socialDistancing = introResults[0]
    socialBubbles = introResults[1]
    pygame.display.set_caption('Simulation of Covid-19')
    people = []
    sim.initializePopulation(socialDistancing,people)
    sim.runSimulation(people,socialBubbles)
   
