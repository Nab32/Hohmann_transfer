import pygame, sys, math
from Body import Body
from Rocket import Rocket
import constants

pygame.init()



win = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption("Hohmann transfer orbit")



WHITE = (255,255,255)
BLACK = (0,0,0)


def orbitalspeed(mass,distance):

    #calculate the orbital speed for a specific orbit around the earth
    return math.sqrt((constants.G * mass)/distance)
    

def Keplers3rdlaw(r1,r2):
    a = (r1+r2)/2
    #convert to AU
    aInAU=a/constants.AU
    #Period of full ellipse in years
    p = math.sqrt(aInAU * aInAU* aInAU)
    
    return (p) * 12


def findlaunch(T,p):
    angleForLaunch=(-1*(360*(T/12)/(p/12)-180))
    return angleForLaunch



#fields for satellite
startdist=constants.AU #distance from the surface of the earth for starting orbital
targetdist=constants.AU * 1.524 #distance from the surface of the earth for target orbital
r1=constants.SUN_RADIUS+startdist #radius of starting orbital
r2=constants.SUN_RADIUS+targetdist#radius of target orbital
satelliteStartOS=orbitalspeed(constants.SUN_M,r1) #orbital speed of satellite for initial orbit
satelliteTargetOS=orbitalspeed(constants.SUN_M, r2) #orbital speed of satellite for target orbit
marsTime=Keplers3rdlaw(r1,r2)/2 #Time to go to mars
marsPeriod=Keplers3rdlaw(r2,r2)
angleNeeded=findlaunch(marsTime,marsPeriod)





#create bodies
sun = Body(0, 0, constants.SUN_M, 16,'yellow')
satellite = Rocket(0, r1, 500, 3, "green")
mars = Body(r2,0,constants.MARS_M,8,'red')

#mars initial velocity
marsInitialVel=orbitalspeed(constants.SUN_M,r2)
mars.y_vel=-marsInitialVel


#find orbital speed of the satellite for its initial orbit
satellite.x_vel = satelliteStartOS



#list of all bodies in the simulation
bodies=[sun,satellite]

def main():

    font1=pygame.font.Font('SourceSansPro-Bold.ttf',50)
    font2=pygame.font.Font('SourceSansPro-Bold.ttf',25)
    counter=0
    clock = pygame.time.Clock()
    count=0 #for trail
    finalThrust=True #check if final thrust has been executed yet
    initialThrust=True #check if launch to Mars has been executed yet
    errorBound = (0.1 * constants.AU)/200 #error bound for final thrust execution
    angleErrorBound=0.01 #error bound for the inital thrust angle

    coordinateList=[] #list of coordinates for satellite trail
    drawTrail=False #check if initial thrust was executed to start drawing trail

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and initialThrust:
                    #Spacebar to activate the initial thrust of the rocket
                    satellite.initThrust(r1,r2,math.sqrt(satellite.x_vel**2 + satellite.y_vel**2))
                    initialThrust=False
                    drawTrail=True
                if event.key == pygame.K_b and mars not in bodies:
                    bodies.append(mars)


        win.fill(BLACK)          

        #determine if the satellite has reached the target orbit within the error bound to execute the final thrust

        if math.sqrt(satellite.x ** 2 + satellite.y **2) >= (r2 - errorBound) and math.sqrt(satellite.x ** 2 + satellite.y **2) <= (r2 + errorBound) and finalThrust:
            satellite.finalThrust(r1,r2,satelliteTargetOS)
            finalThrust=False

        #check if the satellite is at the right angle from mars to execute inital thrust for Hohmann transfer

        if mars.angle(satellite) >= angleNeeded-angleErrorBound and mars.angle(satellite) <= angleNeeded+angleErrorBound and initialThrust and mars in bodies:
            satellite.initThrust(r1,r2,math.sqrt(satellite.x_vel**2 + satellite.y_vel**2))
            initialThrust=False
            drawTrail=True
            
        if drawTrail:

            if count % 300 == 0 and finalThrust:
                coordinateList.append([satellite.x * constants.SCALE,satellite.y * constants.SCALE])
                count=0

            count+=1

            for coord in coordinateList:
                pygame.draw.circle(win, "white", (coord[0] + constants.SCREEN_WIDTH/2, coord[1] + constants.SCREEN_HEIGHT/2), 2)
                
                
        
        #Initial orbit (Earth)
        pygame.draw.circle(win,"blue",(0 + constants.SCREEN_WIDTH/2,0 + constants.SCREEN_HEIGHT/2),r1*constants.SCALE,1)
        
        #Target orbit (Mars)
        pygame.draw.circle(win,"red",(0 + constants.SCREEN_WIDTH/2,0 + constants.SCREEN_HEIGHT/2),r2*constants.SCALE,1) 

        sun.x_vel=0
        sun.y_vel=0

        #Loop through all bodies
        
        for body in bodies:
            #Draw object on screen
            body.draw(win)
            #update position of object
            body.update(bodies)

        satellite.draw(win)
        #Calculate velocity of satellite every frame    
        satelliteVelocity=math.sqrt(satellite.x_vel**2 + satellite.y_vel**2)

        win.blit(font1.render("Speed of the rocket: " + str(int(satelliteVelocity)) + " m/s",True,"White"),(10,10))

        win.blit(font2.render("Hohmann transfer orbit",True,"White"),(10,840))
        win.blit(font2.render("Press B to activate the mars mission simulation",True,"White"),(10,870))
        win.blit(font2.render("Press SPACE to simulate the hohmann transfer at current position",True,"White"),(10,900))
        
        if not initialThrust and finalThrust:
            counter+=constants.TIME_STEP
            
        win.blit(font1.render("Time: " + str(int(counter/(60*60*24))) + " days",True,"White"),(10,70))

        mars.angle(satellite)
        
        pygame.display.update()
        
        clock.tick(1000)
        
        

main()  