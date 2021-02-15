from game import Maze, Character, Path, blockSize
import time


########### TO PARSE THE TEST FILE INTO AN ARRAY CALLED "grid" BELOW #########################

input_level = input("Please, Enter the level that you want to solve: ")
read_maze = open(input_level , 'r')  #to read the maze from the file
maze_lines= read_maze.readlines()    #to read the maze line by line
global grid
grid = [list(i.strip()) for i in maze_lines] #to convert the maze to 2d array with every line as string

#define somw important variables and lists will be used in while loop
#define this list to save the coordinates of every step of the turtle path(it should be outside While loop)
path_coordinates = []
#define this list to save the coordinates of every coin that the turtle collects(it should be outside While loop)
coin_coordinates = []
#define the variable that will hold the number of collected coins(it should be outside While loop)
collected_coins = 0

###############################################################################################

maze = Maze()
maze.setUpMaze(grid)
startingPos = maze.getStartingPosition()

character = Character(startingPos)

wall = maze.getWall()

finish = maze.getFinish()

coins = maze.getCoins()

path = Path()


while(True):
    """
    * The coordinates of the walls stored in "wall" list in the form of tuples [(x,y), (i,j)] -- list of tuples

    * The coordinates of the end point stored in "finish" tuple in the form of (x,y)

    * The coordinates of the coins stored in "coins" list in the form of tuples [(x,y), (i,j)] -- list of tuples

    * At each itteration:
        - X coordinate of the character stored in "currentX" variable
        - Y coordinate of the character stored in "currentY" variable
        - Current angle of the character stored in "angle" variable

    * To move the character forward write character.moveForward()

    * To rotate the character to the right write character.rotateRight()

    * To rotate the character to the left write character.rotateLeft()

    * To update the coordinates after moving write the following lines:
        -   currentX = character.getCurrentX()
        -   currentY = character.getCurrentY()

    * To update the angle after rotating write the following line:
        -   angle = character.getAngle()

    * To draw the path you can use either of the following functions:
        - path.drawBlock(x,y) to draw a box on x,y coordinates
        - path.drawArray(array) to draw a series of boxes by passing a list that contains a
        tuple of coordinates i.e.
                array = [(10,20), (5, 30)]
                path.drawArray(array) #this will draw two blue boxes one at(10,20) and the other at (5,30)


    * The angles are illustrated below


                           angle  = 90
                                |
                                |
                                |
                   _____________|_____________
         angle = 180            |           angle = 0
                                |
                                |
                                |
                           angle = 270
                           
    """

    currentX = character.getCurrentX()
    currentY = character.getCurrentY()
    angle = character.getAngle()
    print("X: " + str(currentX) + " Y: " + str(currentY) + " Angle: " + str(angle))

    ######################### GAME LOOP ###############################
    ################## WRITE YOUR CODE BELOW ##########################

    #finish the loop once reach the finish
    if (currentX,currentY) == finish:
        print("Max coins that could be collected is ",collected_coins)
        break



    #we need to update the coordinates from the current coordinates to detect the next object before the turtle moves to
    #calculating the quantities that we are going to add to the current coordinates to update the coordinates according to angle
    #define variables
    #these variables will be added for detecting the dead front wall
    px_forward = 0
    py_forward = 0
    #these variables will be added for detecting the dead wall from left
    px_rotating_l = 0
    py_rotating_l = 0
    #these variables will be added for detecting the dead wall from right
    px_rotating_r = 0
    py_rotating_r = 0
    #defining the quantites according to angle
    if angle == 270:
        py_forward = -24
        px_rotating_l = 24
        px_rotating_r = -24
    elif angle == 0:
        px_forward = 24
        py_rotating_l = 24
        py_rotating_r = -24
    elif angle == 180:
        px_forward = -24
        py_rotating_l = -24
        py_rotating_r = 24
    else:
        py_forward = 24
        px_rotating_l = -24
        px_rotating_r = 24


        
    def check_left(x,y):
        '''
        this function detects the existing of blocks in the left path from the current point
        and returns a bool with true or false values
        '''
        #define the bool
        left = False
        #the function body
        if (x+px_rotating_l,y+py_rotating_l) in wall:
            left = True
        else:
            left = False
        #return
        return left

    def check_right(x,y):
        '''
        this function detects the existing of blocks in the right path from the current point
        and returns a bool with true or false values
        '''
        #define the bool
        right = False
        #the function body
        if (x+px_rotating_r,y+py_rotating_r) in wall:
            right = True
        else:
            right = False
        #return
        return right

    def check_forward(x,y):
        '''
        this function detects the existing of blocks in the forward path from the current point
        and returns a bool with true or false values
        '''
        #define the bool
        forward = False
        #the function body
        if (x+px_forward,y+py_forward) in wall:
            forward = True
        else:
            forward = False
        #return
        return forward
            



    #control the movement of the turtle
    #(the used algorithm is explained in docx file)
    if not(check_left(currentX,currentY)):
        character.rotateLeft()
        character.moveForward()
    elif (check_left(currentX,currentY)) and (not(check_right(currentX,currentY))):
        character.rotateRight()
        character.moveForward()
    elif check_left(currentX,currentY) and check_right(currentX,currentY) and check_forward(currentX,currentY):
        character.rotateRight()
        character.rotateRight()
        character.moveForward()
    else:
        character.moveForward()


    
    #appending the current coordinates of the turtle to list path_coordinates
    path_coordinates.append(tuple((currentX,currentY)))
    steps_num = len(path_coordinates)



    #appeending coordinates that have intersections between right and left paths to list 'wall' to make the turtle not move into again
    #(the used algorithm is explained in docx file)
    if check_left(currentX,currentY):
        if not(check_right(currentX,currentY)) and not(check_forward(currentX,currentY)):
            wall.append(path_coordinates[steps_num-2])

    if not(check_left(currentX,currentY)):
        if not(check_right(currentX,currentY) and check_forward(currentX,currentY)):
            wall.append(path_coordinates[steps_num-2])



    #display the path
    path.drawBlock(currentX,currentY)


    
    #collecting the coins
    if (currentX,currentY) in coins:
        if not((currentX,currentY) in coin_coordinates):  #this if condition is for not calculating the coin twice if the turtle moves more than one time on the coin
            coin_coordinates.append(tuple((currentX,currentY)))
            collected_coins += 1

    
        
    ###################################################################


maze.endProgram()
