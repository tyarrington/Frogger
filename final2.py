from graphics import *
import random
WIDTH=800
HEIGHT=600

#----------------------------------------------------------------
class Wheel:
    """A class with two concentric circles"""

    def __init__( self, center, r1, r2 ):
        self.circ1 = Circle( center, r1 )
        self.circ2 = Circle( center, r2 )
        r1, r2 = min( r1, r2 ), max( r1, r2 )
        self.radius1 = r1
        self.radius2 = r2
       
    def draw( self, win ):
        self.circ2.draw( win )
        self.circ1.draw( win )

    def setFill( self ):
        self.circ1.setFill( "black" )
        self.circ2.setFill( "gray" )

    def getRadius1( self ):
        return self.radius1

    def getRadius2( self ):
        return self.radius2

    def move( self, dx, dy ):
        self.circ1.move( dx, dy )
        self.circ2.move( dx, dy )

#----------------------------------------------------------------
class Car:
    """a class containing a rectangle and 2 wheels"""

    def __init__( self, P1):
        """constructs the car.  The top-left and bottom-right points
        defining the body of the car are given."""
        self.P1 = P1
        self.P2 = Point(P1.getX()+80, P1.getY()+30)
        self.width = 100
        self.height= 50
       
        #--- define rectangle---
        self.body    = Rectangle( P1, self.P2 )
       
        #--- and the two wheels ---
        center1      = Point(self.P2.getX()-self.width//5, self.P2.getY())
        center2      = Point( self.P2.getX()-self.width*3//5, self.P2.getY() )
        radius2      = self.height/3
        radius1      = radius2/2
        self.wheel1  = Wheel( center1, radius1, radius2 )
        self.wheel2  = Wheel( center2, radius1, radius2 )

    def draw( self, win ):
        """draw rectangle  2 wheels on window"""
        self.body.draw( win )
        self.wheel1.draw( win )
        self.wheel2.draw( win )

    def setFill( self, color):
        """defines the color of the car.  First is body, then inside wheel, then tire color"""
        self.body.setFill( color )
        self.wheel1.setFill()
        self.wheel2.setFill()

    def moveRight( self ):
        """defines direction of movement for all 3 elements of car"""
        if self.body.getCenter().getX() >= WIDTH:
            dx = 0 - self.body.getCenter().getX()
            dy = 0
        else:
            dx = 15
            dy = 0
            
        self.body.move( dx, dy )
        self.wheel1.move( dx, dy )
        self.wheel2.move( dx, dy )

    def moveLeft( self ):
        """defines direction of movement for all 3 elements of car"""
        if self.body.getCenter().getX() <= 0:
            dx = WIDTH - self.body.getCenter().getX()
            dy = 0
        else:
            dx = -15
            dy = 0
            
        self.body.move( dx, dy )
        self.wheel1.move( dx, dy )
        self.wheel2.move( dx, dy )

#------------------------------------------------------------------
class Banner:
    def __init__( self, message ):
        """constructor.  Creates a message at the top of the graphics window"""
        self.text = Text( Point( WIDTH//2, 20 ), message )
        self.text.setFill( "black" )
        self.text.setTextColor( "black" )
        self.text.setSize( 20 )
       
    def draw( self, win ):
        """draws the text of the banner on the graphics window"""
        self.text.draw( win )
        self.win = win
       
    def setText( self, message ):
        """change the text of the banner."""
        self.text.setText( message )

class Frog:
    def __init__ (self, xx, yy, img):
        self.x = xx
        self.y = yy
        self.image = Image( Point( xx, yy ), img )

    def draw( self, win ):
        self.image.draw( win )

    def clickDown(self):
        deltaX = 0
        deltaY = 50
        self.image.move(deltaX, deltaY)

    def clickUp(self):
        deltaX = 0
        deltaY = -50
        self.image.move(deltaX, deltaY)

    def moveToStart(self):
        deltaX = 0
        deltaY = HEIGHT-50-self.image.getAnchor().getY()
        self.image.move(deltaX, deltaY)

    def hitCar(self, centerCar):
        frogX = self.image.getAnchor().getX()
        frogY = self.image.getAnchor().getY()
        topCarY = centerCar.getY()
        botCarY = centerCar.getY() + 50
        leftCarX = centerCar.getX()
        rightCarX = centerCar.getX() + 100

        if frogX>=leftCarX and frogX<=rightCarX and frogY>=topCarY and frogY<=botCarY:
            return True
        else:
            return False
        
def main():
    # creates a window
    win = GraphWin( "Froggy: Tinli Yarrington", WIDTH, HEIGHT )

    # draw the banner at the top
    lifePoints = 3
    crossings = 0
    banner = Banner( "{0:1} life point(s), {1:1} crossing(s)".format(lifePoints, crossings) )
    banner.draw( win )

    road1 = Rectangle(Point(0, HEIGHT//4), Point(WIDTH, HEIGHT//4+20))
    road1.setFill("gray")
    road1.draw(win)
    road2 = Rectangle(Point(0, HEIGHT*3//4), Point(WIDTH, HEIGHT*3//4+20))
    road2.setFill("gray")
    road2.draw(win)

    frog = Frog(WIDTH//2, HEIGHT-50, "Frog3.gif")
    frog.draw(win)

    colors = ["blue", "pink", "green", "seagreen", "red", "azure", "chartreuse", "coral", "cyan", "dark magenta", "deep pink", "deep sky blue", "lavender", "light green", "light salmon"]
    
    carsTop = []
    for num in range(3):
        car = Car(Point(random.randrange(20, WIDTH-20), HEIGHT//3))
        car.setFill(colors[random.randrange(len(colors)-1)])
        car.draw(win)
        carsTop.append(car)

    carsBot = []
    for num in range(3):
        car = Car(Point(random.randrange(20, WIDTH-20), HEIGHT//2))
        car.setFill(colors[random.randrange(len(colors)-1)])
        car.draw(win)
        carsBot.append(car)


    while lifePoints > 0:
        p = win.checkMouse()

        for car in carsTop:
            car.moveRight()
            center = car.body.getCenter()
            hit = frog.hitCar(center)
            if hit:
                frog.moveToStart()
                lifePoints-=1
                banner.setText("{0:1} life point(s), {1:1} crossing(s)".format(lifePoints, crossings))

        for car in carsBot:
            car.moveLeft()
            center = car.body.getCenter()
            hit = frog.hitCar(center)
            if hit:
                frog.moveToStart()
                lifePoints-=1
                banner.setText("{0:1} life point(s), {1:1} crossing(s)".format(lifePoints, crossings))
        
        if p!= None and p.getY() < HEIGHT//4 and frog.image.getAnchor().getY() > 0:
            frog.clickUp()
            if frog.image.getAnchor().getY() == HEIGHT//4:
                crossings += 1
                banner.setText("{0:1} life point(s), {1:1} crossing(s)".format(lifePoints, crossings))
                frog.moveToStart()
        elif p != None and p.getY() > HEIGHT*3//4 and frog.image.getAnchor().getY() < HEIGHT:
            frog.clickDown()

    
    banner.setText("Game over: Froggy crossed {0:1} time(s)".format(crossings))

main()
