import pygame
import math
import constants
from Body import Body

class Rocket(Body):

    def initThrust(self, r1, r2, initV):

        #Calculate necessary speed of the rocket to exit current orbit
        v = math.sqrt(2 * constants.G * constants.SUN_M * (1/r1 - 1/(r1+r2))) 
        speedMult = v / initV
        self.x_vel=self.x_vel * speedMult
        self.y_vel=self.y_vel * speedMult 
        
        
    def finalThrust(self, r1, r2, finalV):
        
        v = math.sqrt(2 * constants.G * constants.SUN_M * (1/r2 - 1/(r1+r2)))
        speedMult = finalV / v
        self.x_vel=self.x_vel * speedMult
        self.y_vel=self.y_vel * speedMult 