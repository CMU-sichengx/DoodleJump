from cmu_112_graphics import *
import math
import random
import time

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Stretegy for side scrolling:
always keep the player in the center of the screen
When the player moves upper by x, minus x from the y of every plat
denoted by [VAR] isvisible
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	Citation
I used images for the game:
(1)	playerWithNothing.png: https://poki.com/en/g/doodle-jump
(2)	playerWithArmor.png: https://commons.wikimedia.org/wiki/File:Doodle_Jump.png
(3)	playerWithRocketBag.png: https://icons8.com/icons/set/doodle-jump
https://bsmknighterrant.org/2011/09/27/doodle-jump-lands-on-the-android/
(4)	armor.png: https://pngtree.com/so/cartoon-shield
(5)	rocketBag.png
https://www.models-resource.com/mobile/doodlejumpgalaxyprototype/model/30037/
(6)	enemy.png: https://www.pinterest.com/walls360/doodle-jump-wall-graphics/
* This citation is also in the design proposal
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# density: the aveage number of plats
# Check that if the game is playable: there is always one possible move however
### link: https://youtu.be/1S-dwdHuuk8 
class Bullet(object):
    allBullets = [ ]
    def __init__(self, shooter, x, y, mouseX, mouseY): # x and y is chosen to be the position of the player
        # here the x and y works in the context of 
        # the canvas coordinate
        self.x = x
        self.y = y
        self.shooter = shooter
        self.mouseX = mouseX
        self.mouseY = mouseY
        self.r = 5
        self.speed = 30
        self.ifExist = True
        # fix the bearing 
        deltaX = self.mouseX - self.x
        deltaY = self.mouseY - self.y
        dist = math.sqrt(deltaX**2 + deltaY**2)
        self.moveX = deltaX / dist
        self.moveY = deltaY / dist
        # add to records
        Bullet.allBullets.append(self)
    
    # the bullet flies
    # to be implemented every time
    def moveBullet(self, pivotY):
        self.x += self.moveX * 10
        self.y += self.moveY * 10

    # to be implemented every timerFired
    # see if the bullet shoots an enemy
    def hitEnemy(self, pivotY, imgWidth, imgHeight):
        # after each move, check if the bullet hits an enemy
        for plat in Platform.allPlats:
            if plat.isVisible:
                if isinstance(plat.holding, Enemy):
                    self.shooter.numOfEnemies =+ 1
                    # the normal height coordinate
                    upper, lower, left, right = plat.getBounds()
                    # the screen
                    upperScreen = pivotY + Player.screenHeight / 2
                    lowerScreen = pivotY - Player.screenHeight / 2
                    # convert to the canvas coordinate
                    upper = Player.screenHeight - (upper - lowerScreen)
                    lower = Player.screenHeight - (lower - lowerScreen)
                    left = left
                    right = right
                    # calculate the boundary of the enemy
                    x0 = (left + right) / 2 - imgWidth / 2
                    x1 = (left + right) / 2 + imgWidth / 2
                    y0 = upper - imgHeight
                    y1 = upper
                    # position of the bullet
                    bulletX = self.x
                    bulletY = self.y
                    if x0 <= bulletX <= x1 and y0 <= bulletY <= y1:
                        plat.holding = None
                        self.ifExist = False    

    # this method moves all the bullets
    @staticmethod
    def moveAllBullets(pivotY, imgWidth, imgHeight):
        for bullet in Bullet.allBullets:
            if bullet.ifExist:
                bullet.moveBullet(pivotY)
                bullet.hitEnemy(pivotY, imgWidth, imgHeight)


    def drawBullet(self, canvas):
        # first convert the 
        if self.ifExist:
            canvas.create_oval(self.x-self.r, self.y-self.r, 
                               self.x+self.r, self.y+self.r, fill="green")
    
    @staticmethod
    def drawAllBullets(canvas):
        for bullet in Bullet.allBullets:
            bullet.drawBullet(canvas)
'''
'''
'''
'''
class File(object):
    fileName = "scoreboard.txt"
    @staticmethod
    # Citation: from the course website:
    # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

    @staticmethod
    # Citation: from the course website:
    # https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
'''
'''
'''
'''
class Enemy(object):
    image = None
    pass
'''
'''
'''
'''
class RocketBag(object):
    speed = 25
    duration = 1.5
    image = None
    def boostPlayer(self, player): # player is an instance of the Player
        player.y += RocketBag.speed
        self.image = None
'''
'''
'''
'''
class Armor(object):
    duration = 2
    image = None
    pass
'''
'''
'''
'''
class Platform(App):
    # static variables
    allPlats = [ ]
    platWidth = 40
    platHeight = 9
    screenHeight = 500
    screenWidth = 500
    
    # generate a new platform (general type)
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.isVisible = False
        self.holding = None # what the object is holding 
                            # can be enemy or powerups
        self.holdingImage = None
        self.num = num # for debugging purposes

    def setHolding(self, obj):
        self.holding = obj
        self.holdingImage = obj.image

    def __repr__(self):
        return f"(x = {self.x}, y = {self.y})"

    def getBounds(self):
        upper = self.y + Platform.platHeight / 2
        lower = self.y - Platform.platHeight / 2
        left = self.x - Platform.platWidth / 2
        right = self.x + Platform.platWidth / 2
        return upper, lower, left, right

    def getMovingBound(self):
        if self.holdingImage == None:
            return self.getBounds()
        else:
            upper_, lower_, left_, right_ = self.getBounds()
            imgWidth, imgHeight = self.holdingImage.size
            upper = upper_ + imgHeight
            lower = lower_
            left = min(self.x-imgWidth/2, left_)
            right = max(self.x+imgWidth/2, right_)
            return upper, lower, left, right

    @staticmethod
    # checks if the point (x, y) is inside a platform:
    def pointInsidePlat(pt, plat):
        x, y = pt[0], pt[1]
        upper, lower, left, right = plat.getMovingBound()
        return left <= x <= right and lower <= y <= upper

    @staticmethod
    # checks if two plats overlap
    def ifOverlap(plat1, plat2):
        upper, lower, left, right = plat1.getMovingBound()
        # UL - upper left; UR - upper right; LL - lower left; LR - lower right
        UL = left, upper
        UR = right, upper
        LL = left, lower
        LR = right, lower
        return Platform.pointInsidePlat(UL, plat2) or \
               Platform.pointInsidePlat(UR, plat2) or \
               Platform.pointInsidePlat(LL, plat2) or \
               Platform.pointInsidePlat(LR, plat2)

    @staticmethod
    # checks if a newly generated plat form fits into the existing platforms
    # without causing overlapo
    def notOverlap(newPlat, plats):
        for plat in plats:
            if Platform.ifOverlap(newPlat, plat): 
                return False
        return True

    # return the distance between this plat to another
    def getDist(self, other):
        assert(isinstance(other, Platform) == True)
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        dist = math.sqrt(dx**2 + dy**2)
        return dist

    # this method examines if the random layout of platforms is solvable
    # Var plats: partial list of plats
    # for horizontal: just make sure that the player can finish a complete 
    # wrap around during one duration

    @staticmethod
    # this function address every pixel of hights
    # to see if the range from h0 to h1 is covered
    def isSolvable():
        reachable = dict()
        for h in range(300, 10000):
            reachable[h] = False
        
        for plat in Platform.allPlats:
            if isinstance(plat.holding, Enemy): 
                continue
            # bounds of the plat
            upper, lower, left, right = plat.getBounds()
            hLower = int(lower)
            hHigher = int(upper + Player.duration * Player.vy)
            for h in range(hLower, hHigher+1):
                if h in reachable:
                    reachable[h] = True
        
        for h in reachable:
            if reachable[h] == False:
                return False
        return True
               
    @staticmethod
    def generatePartialPlats(h0, h1, density):
        totPlats = int((h1-h0) * density)
        plats = [ ]
        while len(plats) < totPlats:
            num = len(plats)
            randomInt1 = random.randint(1, 20) # determine the type of plat
            randomInt2 = random.randint(1, 30) # determine the object on the plat
            # generate a moving platform [1 in 20]
            if randomInt1 == 1:
                x = Platform.platWidth/2 + MovingPlatform.span/2 + (Platform.screenWidth-MovingPlatform.span) * random.random()
                y = h0 + Platform.platHeight/2 + (h1-h0-Platform.platHeight) * random.random()
                newPlat = MovingPlatform(x, y, num)
            # generate a temp platform [3 in 20]
            elif randomInt1 == 2 or randomInt1 == 3 or randomInt1 == 4:
                x = Platform.platWidth/2 + (Platform.screenWidth-Platform.platWidth) * random.random()
                y = h0 + Platform.platHeight/2 + (h1-h0-Platform.platHeight) * random.random()
                newPlat = TempPlatform(x, y, num)                
            # generate a normal platform [16 in 20]
            else:
                x = Platform.platWidth/2 + (Platform.screenWidth-Platform.platWidth) * random.random()
                y = h0 + Platform.platHeight/2 + (h1-h0-Platform.platHeight) * random.random()
                newPlat = Platform(x, y, num)
            # generate holding for the platform
            # generate a rocket bag [3 in 20]
            if randomInt2 == 1 or randomInt2 == 2 or randomInt2 ==  3: 
                newPlat.setHolding(RocketBag())
            # generate a armor [3 in 20]
            elif randomInt2 == 4 or randomInt2 == 5 or randomInt2 == 6:
                newPlat.setHolding(Armor())
            # generate an enemy [2 in 20]
            elif randomInt2 == 7:
                newPlat.setHolding(Enemy())


            # put the platform onto canvas
            if Platform.notOverlap(newPlat, plats):
                plats.append(newPlat)
        return plats
    
    @staticmethod
    def generateAllPlats():
        Platform.allPlats = [ ]
        h = 20
        deltah = 600
        maxHeight = 10000 # the max height which is assumed to be impossible for a player to reach
        while h <= maxHeight:
            density = 0.05 - h / 10000000
            newPlats = [ ]
            #while Platform.isSolvable(h, h+deltah, newPlats) == False:
            newPlats = Platform.generatePartialPlats(h, h+deltah, density)
            Platform.allPlats += newPlats
            h += deltah
        return Platform.allPlats

    @staticmethod
    # to be implemented every timerFired
    # the screen always centers at maxHeightSoFar of the player
    def refreshScreen(pivotY):
        lowerBound = pivotY - Platform.screenHeight / 2
        upperBound = pivotY + Platform.screenHeight / 2
        for plat in Platform.allPlats:
            upper, lower, left, right = plat.getBounds()
            # all such plats are the "visible" ones
            if upper <= upperBound and lower >= lowerBound:
                plat.isVisible = True
            else:
                plat.isVisible = False


    def drawPlat(self, canvas, pivotY):
        upper, lower, left, right = self.getBounds()
        # the upper and lower height of the screen
        upperScreen = pivotY + Platform.screenHeight / 2
        lowerScreen = pivotY - Platform.screenHeight / 2
        # the parameters relative to the canvas screen
        x0 = left
        x1 = right
        y0 = upperScreen - upper
        y1 = upperScreen - lower
        canvas.create_rectangle(x0, y0, x1, y1)
        tx = (x0 + x1) / 2
        ty = (y0 + y1) / 2
        canvas.create_text(tx, ty)          
    
    # draw something that this platform holds
    def drawObjOntoPlat(self, canvas, pivotY, obj):
        upper, left, left, right = self.getBounds()
        imgWidth, imgHeight = obj.image.size
        upperScreen = pivotY + Platform.screenHeight / 2
        lowerScreen = pivotY - Platform.screenHeight / 2
        # calculate the four coordinate for the obj on canvas
        x = (left + right) / 2
        y = upperScreen - upper - imgHeight / 2
        canvas.create_image(x, y, image=ImageTk.PhotoImage(obj.image))


    @staticmethod
    def drawAllPlats(canvas, pivotY):
        for plat in Platform.allPlats:
            if plat.isVisible:
                plat.drawPlat(canvas, pivotY)
                if plat.holding != None:
                    plat.drawObjOntoPlat(canvas, pivotY, plat.holding)
    
    @staticmethod
    # this is used to renew the game data
    def renewGame():
        Platform.allPlats = [ ]
'''
'''
'''
'''
class MovingPlatform(Platform):
    speed = 8
    span = Platform.screenWidth / 4
    
    def __init__(self, x, y, num):
        super().__init__(x, y, num)
        self.leftBound = self.x - MovingPlatform.span / 2 - Platform.platWidth / 2
        self.rightBound = self.x + MovingPlatform.span / 2 + Platform.platWidth / 2
        self.direction = +1
    
    # Overriden
    def getMovingBound(self):
        upper = self.y + Platform.platHeight / 2
        lower = self.y - Platform.platHeight / 2
        left = self.leftBound
        right = self.rightBound
        return upper, lower, left, right

    # move a moveingplat
    def movePlat(self):
        self.x += self.direction * MovingPlatform.speed
        upper, lower, left, right = self.getBounds()
        # if reach right bound
        if right >= self.rightBound:
            self.x = self.rightBound - Platform.platWidth / 2
            self.direction *= -1
        # if reach left bound
        if left <= self.leftBound:
            self.x = self.leftBound + Platform.platWidth / 2
            self.direction *= -1

    @staticmethod
    # to be implemented every 
    # this function moves all the movePlats
    def moveAllPlats():
        for plat in Platform.allPlats:
            if isinstance(plat, MovingPlatform):
                plat.movePlat()
    
    # Overriden
    def drawPlat(self, canvas, pivotY):
        upper, lower, left, right = self.getBounds()
        # the upper and lower height of the screen
        upperScreen = pivotY + Platform.screenHeight / 2
        lowerScreen = pivotY - Platform.screenHeight / 2
        # the parameters relative to the canvas screen
        x0 = left
        x1 = right
        y0 = upperScreen - upper
        y1 = upperScreen - lower
        canvas.create_rectangle(x0, y0, x1, y1)
'''
'''
'''
'''
class TempPlatform(Platform):
    def __init__(self, x, y, num):
        super().__init__(x, y, num)
        self.remJumps = 3
    
    # Overriden
    def drawPlat(self, canvas, pivotY):
        upper, lower, left, right = self.getBounds()
        # the upper and lower height of the screen
        upperScreen = pivotY + Platform.screenHeight / 2
        lowerScreen = pivotY - Platform.screenHeight / 2
        # the parameters relative to the canvas screen
        x0 = left
        x1 = right
        y0 = upperScreen - upper
        y1 = upperScreen - lower
        canvas.create_oval(x0, y0, x1, y1, fill="green")
'''
'''
'''
'''
class Player(App):
    players = [ ]
    screenWidth = 500
    screenHeight = 500
    playerHeight = 30
    playerWidth = 30
    vx = 10
    vy = 10
    duration = 1.6 # player rises for 1.5 secs

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isFalling = False
        self.height = Player.playerHeight
        self.width = Player.playerWidth
        self.maxHeightSoFar = self.x + self.height / 2
        self.startMoveTime = time.time()
        self.equip = None # power up
        self.isAlive = True
        self.numOfJumps = 0
        self.numOfRocketBags = 0
        self.numOfArmors = 0
        self.numOfEnemies = 0
    
    def setImageWithNothing(self, image):
        self.playerWithNothingImg = image
        imgLength, imgWidth = self.playerWithNothingImg.size
        Player.playerHeight = self.height = imgLength
        Player.playerWidth = self.width = imgWidth

    def setImageWithRocketBag(self, image):
        self.playerWithRocketBagImg = image
        imgLength, imgWidth = self.playerWithRocketBagImg.size
        Player.playerHeight = self.height = imgLength
        Player.playerWidth = self.width = imgWidth

    def setImageWithArmor(self, image):
        self.playerWithArmorImg = image
        imgLength, imgWidth = self.playerWithArmorImg.size
        Player.playerHeight = self.height = imgLength
        Player.playerWidth = self.width = imgWidth 

    def getBounds(self):
        upper = self.y + self.height / 2
        lower = self.y - self.height / 2
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        return upper, lower ,left ,right

    @staticmethod
    # set horizontal speed
    def setHorizontalSpeed(v):
        Player.vx = v
    
    @staticmethod
    # set vertical speed
    def setVerticalSpeed(v):
        Player.vy = v
    
    @staticmethod
    # set gravitational acceleration
    def setGravity(g):
        Player.g = g
        Player.duration = 2 * Player.vy / Player.g

    # checks if the player falls onto a plat
    def collideWithPlat(self, plat):
        platUpper, platLower, platLeft, platRight = plat.getBounds()
        playerUpper, playerLower, playerLeft, playerRight = self.getBounds()
        # check
        verticalCollide = platLower <= playerLower <= platUpper
        horizontalCollide = playerRight >= platLeft and playerLeft <= platRight
        return verticalCollide and horizontalCollide

    def moveVertical(self):
        if self.equip == None:
            self.moveVerticalWithNothing()
        else:
            self.moveVerticalWithEquip()

    def moveVerticalWithNothing(self):
        # when the player is rising:
        # 1. update maxHeightSoFar
        # 2. nothing to do with plats
        nowTime = time.time()
        deltaTime = nowTime - self.startMoveTime
        vyNow = self.vy - self.g * deltaTime
        self.y += vyNow
        self.maxHeightSoFar = max(self.maxHeightSoFar, self.y)
        # when the player starts falling
        # 1. nothing to do with maxHeightSoFar
        # 2. check collision with plats
        if vyNow < 0:
            # the upper and lowerbound height of the screen:
            upperScreen = self.maxHeightSoFar + Player.screenHeight / 2
            lowerScreen = self.maxHeightSoFar - Player.screenHeight / 2
            # the bounds of the player
            upper, lower, left, right = self.getBounds()
            if self.y <= lowerScreen:
                self.isAlive = False
                print("You loss")
                return
            # falls normally to see if it is caught by a platform
            FLAG = False
            for plat in Platform.allPlats:
                if plat.isVisible:
                    if self.collideWithPlat(plat):
                        self.numOfJumps += 1
                        if isinstance(plat.holding, Armor):
                            self.numOfArmors += 1
                        elif isinstance(plat.holding, RocketBag):
                            self.numOfRocketBags += 1
                        # print(plat.num)
                        # pick up the stuff on the platform
                        if plat.holding != None:
                            if isinstance(plat.holding, Enemy) and not isinstance(self.equip, Armor):
                                self.isAlive = False
                                return
                            elif isinstance(plat.holding, RocketBag):
                                self.getEquip(plat.holding)
                                plat.holding = None
                            elif isinstance(plat.holding, Armor):
                                self.getEquip(plat.holding)
                                plat.holding = None
                        # or be killed by the enemy on that platform
                        # separately deal with temp plat form
                        if isinstance(plat, TempPlatform):
                            plat.remJumps -= 1
                            if plat.remJumps < 0:
                                Platform.allPlats.remove(plat)
                        # bounds of plat
                        upper, lower, left, right = plat.getBounds()
                        self.y = upper + Player.playerHeight / 2
                        self.startMoveTime = time.time()



    def getEquip(self, equipObj):
        self.equip = equipObj   
        self.equipStartTime = time.time()

    def moveVerticalWithEquip(self):
        self.maxHeightSoFar = max(self.maxHeightSoFar, self.y)
        nowTime = time.time()
        if nowTime >= self.equipStartTime + self.equip.duration:
            self.equip = None
        else:
            # let the equip perform the operation
            if isinstance(self.equip, RocketBag): self.equip.boostPlayer(self)
            elif isinstance(self.equip, Armor): self.moveVerticalWithNothing()
    def moveHorizontal(self, speed):
        self.x += speed
        # wrap around
        self.x %= Player.screenWidth
    
    # This function is for debugging purpose
    def moveVert(self, speed):
        self.y += speed
        self.maxHeightSoFar = max(self.maxHeightSoFar, self.y)
        print(self.maxHeightSoFar)

    def refreshSize(self):
        if self.equip == None:
            imgWidth, imgHeight = self.playerWithNothingImg.size
        elif isinstance(self.equip, RocketBag):
            imgWidth, imgHeight = self.playerWithRocketBagImg.size
        elif isinstance(self.equip, Armor):
            imgWidth, imgHeight = self.playerWithArmorImg.size

        Player.playerHeight = self.height = imgHeight
        Player.playerWidth = self.width = imgWidth

    # draw the player
    # Note: the screen pivots vertically at maxHeightSoFar!
    def drawPlayer(self, canvas):
        # the bounds of the player at the current time
        upper, lower, left, right = self.getBounds()
        # the height of the upper and lower bound of the screen
        upperScreen = self.maxHeightSoFar + Player.screenHeight / 2
        lowerScreen = self.maxHeightSoFar - Player.screenHeight / 2
        # relative position in the canvas screen
        relativeUpper = upper - lowerScreen
        relativeLower = lower - lowerScreen
        relativeLeft = left
        relativeRight = right
        # the x, y coordinate of the canvas
        x0 = relativeLeft
        x1 = relativeRight
        y0 = upperScreen - upper
        y1 = upperScreen - lower
        x = (x0 + x1) / 2
        y = (y0 + y1) / 2
        if self.equip == None:
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.playerWithNothingImg))
        elif isinstance(self.equip, RocketBag):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.playerWithRocketBagImg))   
        elif isinstance(self.equip, Armor):
            canvas.create_image(x, y, image=ImageTk.PhotoImage(self.playerWithArmorImg))
    # the player attcks to the position of mousePressed
    
    def attack(self, x, y, pivotY):
        # here the argument x and y are coordinates on the canvas
        # so this function works in the coordinate sys of the canvas
        xPlayer = self.x
        lowerScreen = pivotY - Platform.screenHeight / 2
        yPlayer = Platform.ScreenHeight - (self.y - lowerScreen)
        # 

'''
'''
'''
'''
class Button(App):
    allButtons = [ ]
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.color = "green"
        self.shape = "rectangle"
        self.width = 50
        self.height = 50
        Button.allButtons.append(self)
    
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height - height
    
    def setShape(self, shape):
        self.shape = shape
    
    def setColor(self, color):
        self.color = color
    
    # here this bound is x, y coordinate of canvas
    def getCanvasBounds(self):
        x0 = self.x - self.width / 2
        x1 = self.x + self.width / 2
        y0 = self.y - self.height / 2
        y1 = self.y + self.height / 2
        return x0, y0, x1, y1

    def drawButton(self, canvas):
        # draw shape
        x0, y0, x1, y1 = self.getCanvasBounds()
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.color)
        # draw text
        canvas.create_text(
            self.x,
            self.y,
            text = self.text
        )
    @staticmethod
    def drawAllButtons(canvas):
        for button in Button.allButtons:
            button.drawButton()
'''
''' 
'''
'''
class GameMode(Mode):
    def appStarted(mode):
        mode.timerDelay = 10
        ''''''''' set the image for rocketbags   '''''''''
        tempImage = mode.loadImage("rocketBag.png")
        tempImage = mode.scaleImage(tempImage, 0.05)
        RocketBag.image = tempImage

        ''''''''' set the image for armors   '''''''''
        tempImage = mode.loadImage("armor.png")
        tempImage = mode.scaleImage(tempImage, 0.05)
        Armor.image = tempImage

        ''''''''' set the image for enemy   '''''''''
        tempImage = mode.loadImage("enemy.png")
        tempImage = mode.scaleImage(tempImage, 0.1)
        print("The size", tempImage.size)
        Enemy.image = tempImage

        ''''''''' generate all the platforms along the way '''''''''
        Platform.generateAllPlats()
        # generate an instance of the player
        # put the player on the first platform generated as above

        ''''''''' generate the player 1 '''''''''
        '''
        idx = 0
        plat1 = Platform.allPlats[idx]
        while plat1.y < mode.height/2:
            idx += 1
            plat1 = Platform.allPlats[idx]
        # bounds of plat1
        upper, lower, left, right = plat1.getBounds()
        mode.player1 = Player(x = upper + Player.playerHeight / 2, 
                              y = (left + right)/ 2)
        '''
        mode.player1 = Player(
            x = mode.height / 2,
            y = 800
        )
        mode.player1.setHorizontalSpeed(20)
        mode.player1.setVerticalSpeed(8)
        mode.player1.setGravity(10)

        tempImage = mode.loadImage("playerWithNothing.png")
        tempImage = mode.scaleImage(tempImage, 0.3)
        mode.player1.setImageWithNothing(tempImage)

        tempImage = mode.loadImage("playerWithRocketBag.png")
        tempImage = mode.scaleImage(tempImage, 0.5)
        mode.player1.setImageWithRocketBag(tempImage)

        tempImage = mode.loadImage("playerWithArmor.png")
        tempImage = mode.scaleImage(tempImage, 0.4)
        mode.player1.setImageWithArmor(tempImage)

        ''''''''' generate the ifGameOver status '''''''''
        mode.ifGameOver = False

        ''''''''' generate the ifPaused status '''''''''
        mode.ifPaused = False

    def timerFired(mode):
        # pause and gameover
        if mode.ifGameOver: return
        if mode.ifPaused: return

        if mode.player1.isAlive == False:
            mode.ifGameOver = True
            Platform.renewGame()
            # round it to the nearest integer
            mode.player1.maxHeightSoFar = int(mode.player1.maxHeightSoFar)
            File.writeFile("currentScore.txt", str(mode.player1.maxHeightSoFar))
            highestScore = int(File.readFile("highestScore.txt"))
            if mode.player1.maxHeightSoFar > highestScore:
                File.writeFile("highestScore.txt", str(mode.player1.maxHeightSoFar))
            # transport info from game mode to game over mode
            mode.app.numOfJumps = mode.player1.numOfJumps
            mode.app.numOfRocketBags = mode.player1.numOfRocketBags
            mode.app.numOfArmors = mode.player1.numOfArmors
            mode.app.numOfEnemies = mode.player1.numOfEnemies
            # set to game over ode    
            mode.app.setActiveMode(mode.app.gameOverMode)
        
        # the game is running
        Bullet.moveAllBullets(mode.player1.maxHeightSoFar, 48, 30)
        mode.player1.refreshSize()
        mode.player1.moveVertical()
        Platform.refreshScreen(mode.player1.maxHeightSoFar)
        MovingPlatform.moveAllPlats()

    def mousePressed(mode, event):
        # calculate the x and y of the bullet when it starts
        upperScreen = mode.player1.maxHeightSoFar + mode.height / 2
        lowerScreen = mode.player1.maxHeightSoFar - mode.height / 2
        bulletX = mode.player1.x
        bulletY = mode.height - (mode.player1.y - lowerScreen)
        bulletObj = Bullet(mode.player1, bulletX, bulletY, event.x, event.y)

    def keyPressed(mode, event):
        # pause and gameover
        if mode.ifGameOver: return

        # running mode
        if event.key == "Right":
            mode.player1.moveHorizontal(mode.player1.vx)
        elif event.key == "Left":
            mode.player1.moveHorizontal(-mode.player1.vx)
        elif event.key == "Up":
            mode.player1.moveVert(20)
            Platform.refreshScreen(pivotY = mode.player1.maxHeightSoFar)
        elif event.key == "Down":
            mode.player1.moveVert(-20)
            Platform.refreshScreen(pivotY = mode.player1.maxHeightSoFar)
        elif event.key == "p":
            mode.ifPaused = not mode.ifPaused
        
    def redrawAll(mode, canvas):
        # draw all the platforms
        Platform.drawAllPlats(canvas, pivotY = mode.player1.maxHeightSoFar)
        # draw the player
        mode.player1.drawPlayer(canvas)
        # draw the current height
        canvas.create_rectangle(5, 5, 55, 35, fill="cyan")
        canvas.create_text(30, 20, text=int(mode.player1.maxHeightSoFar))
        # draw all the bullets
        Bullet.drawAllBullets(canvas)
'''
'''
'''
'''
class GameOverMode(Mode):
    def appStarted(mode):
        mode.startGameButton = Button(
            mode.width / 2,
            mode.height * 3 / 4,
            "Restart!"
        )
    
    def mousePressed(mode, event):
        x0, x1, y0, y1 = mode.startGameButton.getCanvasBounds()
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            mode.app.gameMode = GameMode()
            mode.app.setActiveMode(mode.app.gameMode)
    
    def redrawAll(mode, canvas):
        highestScore = File.readFile("highestScore.txt")
        currentScore = File.readFile("currentScore.txt")
        canvas.create_text(mode.width/2, mode.height/2,
                           text=f"Your Score: {currentScore}")
        canvas.create_text(mode.width/2, mode.height/2+20,
                           text=f"Highest Score: {highestScore}")
        if currentScore > currentScore:
            canvas.create_text(mode.width/2, mode.height/2+40,
                           text="New highest score!")
        mode.startGameButton.drawButton(canvas)
        canvas.create_text(mode.width/2, mode.height/2+60,
                           text="During the journey, you:")
        canvas.create_text(mode.width/2, mode.height/2+80,
        text=f"Did {mode.app.numOfJumps} jumps; " + \
        f"Used {mode.app.numOfRocketBags} rocket bags; " + \
        f"Used {mode.app.numOfArmors} armors; " +  \
        f"Killed {mode.app.numOfEnemies} enemies!")
'''
'''
'''
'''
class WelcomeMode(Mode):
    def appStarted(mode):
        '''''''''' generate start game button '''''''''
        mode.startGameButton = Button(
            mode.width / 2,
            mode.height * 3 / 4,
            "Start!"
        )
    def mousePressed(mode, event):
        x0, x1, y0, y1 = mode.startGameButton.getCanvasBounds()
        if x0 <= event.x <= x1 and y0 <= event.y <= y1:
            mode.app.gameMode = GameMode()
            mode.app.setActiveMode(mode.app.gameMode)
    
    def redrawAll(mode, canvas):
        canvas.create_text(
            mode.width / 2,
            mode.height / 4,
            text = "Welcome to Doodle Jump!"
        )
        mode.startGameButton.drawButton(canvas)
'''
'''
'''
'''
class MyModalApp(ModalApp):
    def appStarted(app):
        app.welcomeMode = WelcomeMode()
        app.gameMode = GameMode()
        app.gameOverMode = GameOverMode()
        app.timerDelay = 10
        app.setActiveMode(app.welcomeMode)
        app.numOfJumps = 0
        app.numOfRocketBags = 0
        app.numOfArmors = 0
        app.numOfEnemies = 0
'''
'''
'''
'''
class GameModalApp(ModalApp):
    def appStarted(app):
        app.gameMode = GameMode()
        app.timerDelay = 10
        app.setActiveMode(app.gameMode)
'''
'''
'''
'''
# Run this to start the app
MyModalApp(width=500, height=500)

   