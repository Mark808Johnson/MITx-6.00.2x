# 6.00.2x Problem Set 2: Simulating robots

# Simulation Overview
# iRobot is a company (started by MIT alumni and faculty) that sells the Roomba vacuuming robot
# (watch one of the product videos to see these robots in action). Roomba robots move around the floor,
# cleaning the area they pass over.
#
# In this problem set, you will code a simulation to compare how much time a group of Roomba-like robots
# will take to clean the floor of a room using two different strategies.
#

# Simulation Details
# Here are additional details about the simulation model. Read these carefully.
#
# Multiple robots
# In general, there are N > 0 robots in the room, where N is given. For simplicity, assume that robots are
# points and can pass through each other or occupy the same point without interfering.
#
# The room
# The room is rectangular with some integer width w and height h, which are given. Initially the entire floor is dirty.
# A robot cannot pass through the walls of the room. A robot may not move to a point outside the room.
#
# Tiles
# You will need to keep track of which parts of the floor have been cleaned by the robot(s). We will divide the area
# of the room into 1x1 tiles (there will be w * h such tiles). When a robot's location is anywhere in a tile, we will
# consider the entire tile to be cleaned (as in the pictures above). By convention, we will refer to the tiles using
# ordered pairs of integers: (0, 0), (0, 1), ..., (0, h-1), (1, 0), (1, 1), ..., (w-1, h-1).
#
# Robot motion rules
# Each robot has a position inside the room. We'll represent the position using coordinates (x, y) which are floats
# satisfying 0 ≤ x < w and 0 ≤ y < h. In our program we'll use instances of the Position class to store these
# coordinates.
#
# A robot has a direction of motion. We'll represent the direction using an integer d satisfying 0 ≤ d < 360, which
# gives an angle in degrees.
#
# All robots move at the same speed s, a float, which is given and is constant throughout the simulation.
# Every time-step, a robot moves in its direction of motion by s units.
#
# If a robot detects that it will hit the wall within the time-step, that time step is instead spent picking a new
# direction at random. The robot will attempt to move in that direction on the next time step, until it reaches
# another wall.
#
# Termination
# The simulation ends when a specified fraction of the tiles in the room have been cleaned.

import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

# For Python 3.8:
from ps2_verify_movement38 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using Python 3.8

# === Provided class Position

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)

# PROBLEM 1- define RectangularRoom class

# In this problem you will implement the RectangularRoom class. For this class, decide what fields you will
# use and decide how the following operations are to be performed:
#
# Initializing the object
# Marking an appropriate tile as cleaned when a robot moves to a given position (casting floats to ints - and/or
# the function math.floor - may be useful to you here)

# Determining if a given tile has been cleaned
# Determining how many tiles there are in the room
# Determining how many cleaned tiles there are in the room
# Getting a random position in the room
# Determining if a given position is in the room
# Complete the RectangularRoom class by implementing its methods in ps2.py.
#
# Although this problem has many parts, it should not take long once you have chosen how you wish to represent
# your data. For reasonable representations, a majority of the methods will require only a couple of lines of code.)
#
# Hint: During debugging, you might want to use random.seed(0) so that your results are reproducible.
#
# Enter your code for RectangularRoom below.

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        coordinates = {}
        for w in range(0, width):
            for h in range(0, height):
                coordinates[(w, h)] = 0 # 0 indicates tile  is uncleaned
        self.room = coordinates

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.room[int((pos.getX())), int(pos.getY())] = 1 # 1 indicates room has been cleaned

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.room[m, n] == 1:
            return True
        else:
            return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return len(self.room)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return list(self.room.values()).count(1)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.getX() >= self.width or pos.getX() < 0 or pos.getY() < 0 or pos.getY() >= self.height:
            return False
        else:
            return True

    def __str__(self):
        return str(self.room)


# PROBLEM 2- define Robot class

# In ps2.py we provided you with the Robot class, which stores the position and direction of a robot. For this class,
# decide what fields you will use and decide how the following operations are to be performed:
#
# Initializing the object
# Accessing the robot's position
# Accessing the robot's direction
# Setting the robot's position
# Setting the robot's direction
# Complete the Robot class by implementing its methods in ps2.py.
#
# Note: When a Robot is initialized, it should clean the first tile it is initialized on. Generally the model
# these Robots will follow is that after a robot lands on a given tile, we will mark the entire tile as clean.
# This might not make sense if you're thinking about really large tiles, but as we make the size of the tiles smaller
# and smaller, this does actually become a pretty good approximation.
#
# Although this problem has many parts, it should not take long once you have chosen how you wish to represent your
# data. For reasonable representations, a majority of the methods will require only a couple of lines of code)

# In the final implementation of Robot, not all methods will be implemented. Not to worry -- its subclass(es)
# will implement the method updatePositionAndClean()
#
# Enter your code for classes RectangularRoom (from the previous problem) and Robot below.

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.position = room.getRandomPosition()
        self.direction = random.randrange(0, 360)
        self.room = room
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

    def __str__(self):
        return "Robot with position {}, speed of {} and direction of {} degrees".format(self.position, self.speed, self.direction)

# PROBLEM 3- define StandardRobot class

# Each robot must also have some code that tells it how to move about a room, which will go in a method
# called updatePositionAndClean.
#
# Ordinarily we would consider putting all the robot's methods in a single class. However, later in this problem
# set we'll consider robots with alternate movement strategies, to be implemented as different classes with the
# same interface. These classes will have a different implementation of updatePositionAndClean but are for the
# most part the same as the original robots. Therefore, we'd like to use inheritance to reduce the amount of
# duplicated code.
#
# We have already refactored the robot code for you into two classes: the Robot class you completed in Problem 2
# (which contains general robot code), and a StandardRobot class that inherits from it (which contains its own
# movement strategy).
#
# Complete the updatePositionAndClean method of StandardRobot to simulate the motion of the robot after a single
# time-step (as described on the Simulation Overview page).

# Enter your code for classes Robot (from the previous problem) and StandardRobot below.

class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        new_position = self.position.getNewPosition(self.direction, self.speed)
        while self.room.isPositionInRoom(new_position) == False:
            self.setRobotDirection(random.randrange(0, 360))
            new_position = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(new_position)
        self.room.cleanTileAtPosition(self.position)

# random.seed(1)
# Uncomment this line to see your implementation of StandardRobot in action!
# print(testRobotMovement(StandardRobot, RectangularRoom))

# PROBLEM 4- Running the simulation

# In this problem you will write code that runs a complete robot simulation.
#
# Recall that in each trial, the objective is to determine how many time-steps are on average needed
# before a specified fraction of the room has been cleaned. Implement the following function:
#
# def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
#                   robot_type):
#     """
#     Runs NUM_TRIALS trials of the simulation and returns the mean number of
#     time-steps needed to clean the fraction MIN_COVERAGE of the room.
#
#     The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
#     speed SPEED, in a room of dimensions WIDTH x HEIGHT.
#     """
# The first six parameters should be self-explanatory. For the time being, you should pass in
# StandardRobot for the robot_type parameter, like so:
#
# avg = runSimulation(10, 1.0, 15, 20, 0.8, 30, StandardRobot)
# Then, in runSimulation you should use robot_type(...) instead of StandardRobot(...) whenever you wish
# to instantiate a robot. (This will allow us to easily adapt the simulation to run with different robot
# implementations, which you'll encounter in Problem 6.)
#
# Feel free to write whatever helper functions you wish.
#
# We have provided the getNewPosition method of Position, which you may find helpful:
#
# class Position(object):
#
#     def getNewPosition(self, angle, speed):
#         """
#         Computes and returns the new Position after a single clock-tick has
#         passed, with this object as the current position, and with the
#         specified angle and speed.
#
#         Does NOT test whether the returned position fits inside the room.
#
#         angle: integer representing angle in degrees, 0 <= angle < 360
#         speed: positive float representing speed
#
#         Returns: a Position object representing the new position.
#         """
# For your reference, here are some approximate room cleaning times. These times are with a robot speed of 1.0.
#
# One robot takes around 150 clock ticks to completely clean a 5x5 room.
#
# One robot takes around 190 clock ticks to clean 75% of a 10x10 room.
#
# One robot takes around 310 clock ticks to clean 90% of a 10x10 room.
#
# One robot takes around 3322 clock ticks to completely clean a 20x20 room.
#
# Three robots take around 1105 clock ticks to completely clean a 20x20 room.
#
# (These are only intended as guidelines. Depending on the exact details of your implementation, you may get times
# slightly different from ours.)
#
# You should also check your simulation's output for speeds other than 1.0. One way to do this is to take the above
# test cases, change the speeds, and make sure the results are sensible.
#
# For further testing, see the next page in this problem set about the optional way to use visualization methods.
# Visualization will help you see what's going on in the simulation and may assist you in debugging your code.
#
# Enter your code for the definition of runSimulation below.

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    list_time_steps = []
    for trial in range(num_trials):
        # anim = ps2_visualize.RobotVisualization(num_robots, width, height, delay=0.05)
        new_room = RectangularRoom(width, height)
        robots = []
        time_steps = 0
        for i in range(num_robots):
            robots.append(robot_type(new_room, speed))
        for i in range(10000):
            # anim.update(new_room, robots)
            robots[i%len(robots)].updatePositionAndClean()
            time_steps += 1
            if new_room.getNumCleanedTiles()/new_room.getNumTiles() <= min_coverage:
                continue
            else:
                break
        list_time_steps.append(time_steps)
        # anim.done()
    return round((sum(list_time_steps) / len(list_time_steps)) / num_robots, 0)

# Uncomment anim-related lines in above function to see visualization of the simulation
# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 2.0, 10, 12, 0.6, 100, StandardRobot))

# PROBLEM 5- define RandomWalkRobot

# iRobot is testing out a new robot design. The proposed new robots differ in that they change direction randomly
# after every time step, rather than just when they run into walls. You have been asked to design a simulation to
# determine what effect, if any, this change has on room cleaning times.
#
# Write a new class RandomWalkRobot that inherits from Robot (like StandardRobot) but implements the new movement
# strategy. RandomWalkRobot should have the same interface as StandardRobot.
#
# Test out your new class. Perform a single trial with the StandardRobot implementation and watch the visualization
# to make sure it is doing the right thing. Once you are satisfied, you can call runSimulation again, passing
# RandomWalkRobot instead of StandardRobot.
#
# Enter your code for classes Robot and RandomWalkRobot below.

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotDirection(random.randrange(0, 360))
        new_position = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        while self.room.isPositionInRoom(new_position) == False:
            self.setRobotDirection(random.randrange(0, 360))
            new_position = self.position.getNewPosition(self.direction, self.speed)
        self.setRobotPosition(new_position)
        self.room.cleanTileAtPosition(self.position)

# Uncomment this line to see your implementation of RandomWalkRobot
#print(runSimulation(1, 1, 5, 7, 0.5, 1, RandomWalkRobot))

# Provided plotting functions (showPlot1/showPlot2)

def showPlot1(title, x_label, y_label):
    """
    Plot showing number of time-steps taken for 1-10 StandardRobots and RandomWalkRobots to clean 80% of a
    20x20 tile floor.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.

# showPlot1("Number of time-steps for 1-10 robots to clean 80% of a 20x20 tile floor",
#           "Number of robots", "Time-steps")


# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
# showPlot2("Number of time-steps for 2 robots to clean 80% of variously-shaped floors",
#           "floor Aspect-Ratio", "time-steps")
#
