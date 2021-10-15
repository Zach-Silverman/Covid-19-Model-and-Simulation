import random as ra
import pygame
from person import person

green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

quarintineX = 800
quarintineY = 400
quarintineHeight = 400
quarintineWidth = 400


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

    def drawButton(self):
        pygame.draw.rect(self.screen, self.outline,(self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(self.screen,self.colour,(self.x,self.y,self.width,self.height))
        font = pygame.font.SysFont('Helvetica', 20)
        text = font.render(self.text,1,black)
        self.screen.blit(text, (self.x + (self.width/2 - (text.get_width()/2)),
                        self.y + (self.height/2 - (text.get_height()/2))))
    def isOntop(self,mouse):
        mouseX,mouseY = mouse;
        if mouseY >= self.y and mouseY <= self.y + self.height and mouseX >= self.x and mouseX <= self.x + self.width:
            self.colour = green
            return True
        self.colour = blue
        return False
    
    
class Menu:
    
    def createButtons(self, screen):
        x = 400
        width = 400
        height = 80
        y = 200
        buttonList = []
        buttonTitles = ['High Social Distancing',
                        'Medium Social Distancing', 'No Social Distancing',
                        'Social Bubbles', 'Quarantine Enabled']
        for title in buttonTitles:
            button = Button(width,height,title,blue,black,screen,x,y)
            buttonList.append(button)
            y += 100
        return buttonList
    
    def intro(self,screen):
        intro = True
        buttonList = self.createButtons(screen)
        smallfont = pygame.font.SysFont(None, 30)
        checkMarkImg = pygame.image.load('checkmark.jpg')
        checkMarkImg = pygame.transform.scale(checkMarkImg,(112,112))
        checkMarkX = 900
        simulationOptions = ['High', 'Medium', 'None','socialBubbles', 'quarintine']
        while intro:
            results = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro = False
                screen.fill(white)
                for button in buttonList:
                    button.drawButton()
                    button.isOntop(pygame.mouse.get_pos())
                    if event.type == pygame.MOUSEBUTTONDOWN and button.isOntop(pygame.mouse.get_pos()):
                        button.clickedCounter += 1
                text = smallfont.render('Welcome to my Pygame for Covid 19, Click The Buttons Below To Configure Your Options', True, black)
                screen.blit(text, [200, 150])
            checkMarkY = 175
            for i in range(len(buttonList)):
                if (buttonList[i].clickedCounter % 2) != 0:
                   screen.blit(checkMarkImg,(checkMarkX,checkMarkY))
                   results.append(simulationOptions[i])
                checkMarkY += 100      
            pygame.display.update()
            errorCount = 0
        if 'High' in results:
            errorCount += 1
        if 'Medium' in results:
            errorCount += 1
        if 'None' in results:
            errorCount += 1
        
        if errorCount > 1:
            print('Please Enter a valid number of inputs, you can have one of ' 
                    + 'the social distancing options enabled at once only')
            exit(-1)
       
        return results

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
        self.newSickCount = 0
        self.deathCount = 0
        
    def showScore(self,x, y,count,string,colour):
        score = font.render(string + ' :'  + str(count), True, colour)
        screen.blit(score,(x,y))
         
    def initializePopulation(self,results,people):
        minimum = 10
        ymin = 40
        count = 0
        socialDistancing = False
        patientZero = person(ra.randint(minimum, self.width-10),
                             ra.randint(ymin, self.height-10), 'sick', socialDistancing)
        personCount = 0
        for i in range(self.Population - 1):
            guy = (person(ra.randint(minimum, self.width-10),
                                ra.randint(ymin, self.height-10), 'healthy',socialDistancing))
            people.append(guy)
        for person2 in people:
            while person2.iscollidingWithOther(guy):
                    people.remove(person2)
                    person2 = (person(ra.randint(minimum, self.width-10),
                                    ra.randint(ymin, self.height-10), 'healthy',socialDistancing))
                    people.append(person2)
            while 'quarintine' in results and person2.x >= quarintineX and person2.y >= quarintineY:
                people.remove(person2)
                person2 = (person(ra.randint(minimum, self.width-10),
                                    ra.randint(minimum, self.height-10), 'healthy', socialDistancing))
                people.append(person2)
        
        if 'Medium' in results:
            for guy in people:
                #50% of people social distancing in a population of 200
                if personCount >= 100:
                    break
                guy.socialDistancing = True
                personCount+=1
        elif 'High' in results:
            for guy in people:
                #75% of people social distancing in a population of 200
                if personCount >= 150:
                    break
                guy.socialDistancing = True
                personCount += 1
        people.insert(0, patientZero)
        
    def generateQuarintineException(self,person):
        if person.status == 'sick':
            #quarntine 80% of the population
            person.x = ra.randint(
                quarintineX+10, quarintineWidth + quarintineX-10)
            person.y = ra.randint(
                quarintineY+10, quarintineY + quarintineHeight-10)
        
    def runSimulation(self, people, results):
        self.sickCount = 1
        wall = None
        x = 425
        y = 0;
        width = 30
        height = 800
        alreadyRecovered = False
        quarintineWall = None
        if 'quarintine' in results:
           quarintineWall = Wall(quarintineX, quarintineY,
                                 quarintineWidth, quarintineHeight, screen)
        if 'socialBubbles' in results:
            wall = Wall(x, y, width, height,self.screen)
        width = (self.width / 4)
        height = (self.height / 4)
        while self.running:
            if self.recoveredCount > 0:
                alreadyRecovered = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(white)
            self.recoveredCount = 0
            self.deathCount = 0
            if 'quarintine' in results:
                    quarintineWall.drawRectangle()
            for person in people:
                if person.updatePerson(people,wall):
                    self.healthyCount -= 1
                    self.sickCount += 1
                if person.isSick == person.recoveryTime:
                    self.recoveredCount += 1
                    if person.status == 'dead':
                        self.deathCount += 1
                        self.recoveredCount -= 1
                if 'quarintine' in results:
                    person.checkCollisionWithQuarintine(quarintineX,quarintineWidth + quarintineX,quarintineY)
                person.drawPerson(screen)
                for person in people:
                    if self.recoveredCount == 1 and person.status == 'sick' and not alreadyRecovered and 'quarintine' in results:
                        self.generateQuarintineException(person)
                        person.checkCollisionWithQuarintine(
                            quarintineX, quarintineWidth + quarintineX, quarintineY)
            self.newSickCount = self.sickCount - self.recoveredCount - self.deathCount
            if 'socialBubbles' in results:        
                wall.drawRectangle()
                wall.moveWall(self.recoveredCount)
         
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
        
    def drawRectangle(self):
        
        pygame.draw.rect(self.screen,black,(self.x-2,self.y-2,self.width+4,self.height+4))
        pygame.draw.rect(self.screen,white,(self.x,self.y,self.width,self.height))
        
    
    def moveWall(self,delay):
        if delay > 0:
            self.height -= 1

#button for social distance high medium or none 
if __name__ == "__main__":         
    healthyCount = 199
    width = 1200
    height = 800
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
    pygame.display.set_caption('Simulation of Covid-19')
    people = []
    sim.initializePopulation(introResults,people)
    sim.runSimulation(people,introResults)
   
