''' CS5001-Project
    button.py
    Akash Kulkarni

    classes necessary to create the both the graphics of a button managing the
    click events of possibly multiple buttons
'''
import turtle

class ButtonManager:
    def __init__(self,buttons):
        ''' Paramters: list of Button objects to be added
        '''
        self.buttons = buttons
        # variable used for testing
        self.testVar = None

    def initializeScreen(self):
        screen = turtle.Screen()
        screen.onclick(self.callback)
        

    def callback(self, x_click, y_click):
        ''' Parameters: coordinates of click
        '''
        
        if not self.buttons:
            return
        # print(x_click, y_click, self.buttons[0].x, self.buttons[0].y, self.buttons[0].textX)
        for button in self.buttons:
            if button.isWithinBounds(x_click, y_click):
                button.callback(x_click, y_click)
               
                button.clicked = True

        

class Button:
    def __init__(self, position, text, callback):
        ''' Parameters: size of button (width, height) -tuple,
            position of button (x,y)-tuple, text content- string
            creates a button instance
        '''
        # callback function for when button is clicked
        self.callback = callback
        self.x = position[0]
        self.y = position[1]
        self.textX = 0
        self.text = text
        self.clicked = False

        self.screen = None
        
        
    def isWithinBounds(self, x_click, y_click):
            ''' Parameters: coordinates of point clicked
                Return: whether the point is within the button
            '''
            if int(x_click) in range(int(self.x), int(self.textX)) and \
               int(y_click) in range(int(self.y), int(self.y) + 34):
                return True
            return False
        
    def drawButton(self):
        ''' Parameters: None
            Return: None
            draws button
        '''
        self.screen = turtle.Screen()
        self.buttonTurtle = turtle.Turtle()
        self.screen.tracer(0)
        self.buttonTurtle.ht()
        self.buttonTurtle.up()
        self.buttonTurtle.goto(self.x, self.y)
        self.buttonTurtle.write(self.text, move=True, font=("Arial", 24, "normal"))

        
        self.textX = self.buttonTurtle.xcor()

        
        self.buttonTurtle.lt(90)
        self.buttonTurtle.down()
        self.buttonTurtle.goto(self.textX, self.y + 34)
        self.buttonTurtle.goto(self.x, self.y + 34)
        self.buttonTurtle.goto(self.x, self.y)
        self.buttonTurtle.goto(self.textX, self.y)
        self.screen.update()
        
