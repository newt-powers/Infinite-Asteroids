#from python_serial import position
import time
import pygame
import serial  #from pyserial package
import random

with serial.Serial('/dev/cu.usbmodemSDA44586E6C1',115200) as ser:

    #start game
    pygame.init()
    #set up game window
    window = pygame.display.set_mode((500,500))
    pygame.display.set_caption("First game!")

    # define the asteroids, draw them outside of the screen to start
    # asteroid 1
    asteroidImage1 = pygame.image.load('asteroid.PNG')
    asteroid1 = asteroidImage1.get_rect()
    window.blit(asteroidImage1, (0, -75))
    # asteroid 2
    asteroidImage2 = pygame.image.load('asteroid2 copy.PNG')
    asteroid2 = asteroidImage2.get_rect()
    window.blit(asteroidImage2, (0, -150))
    # asteroid 3
    asteroidImage3 = pygame.image.load('asteroid3.PNG')
    asteroid3 = asteroidImage3.get_rect()
    window.blit(asteroidImage3, (0, -225))
    # asteroid 4
    asteroidImage4 = pygame.image.load('asteroid4.PNG')
    asteroid4 = asteroidImage4.get_rect()
    window.blit(asteroidImage4, (0, -300))
    # asteroid 5
    asteroidImage5 = pygame.image.load('asteroid5.PNG')
    asteroid5 = asteroidImage5.get_rect()
    window.blit(asteroidImage5, (0, -375))
    # asteroid 6
    asteroidImage6 = pygame.image.load('asteroid6.PNG')
    asteroid6 = asteroidImage6.get_rect()
    window.blit(asteroidImage6, (0, -450))
    # asteroid 7
    asteroidImage7 = pygame.image.load('asteroid7.PNG')
    asteroid7 = asteroidImage6.get_rect()
    window.blit(asteroidImage7, (0, -525))

    #speed of the asteroids
    asteroidVelocity = 1

    #define the spaceship attributes
    spaceship = pygame.image.load('spaceship.PNG')
    rect = spaceship.get_rect()
    #draw on the bottom middle of the screen
    window.blit(spaceship, (250, 400))

    #define character attributes (initial position, boundaries, rect)
    width = 40
    height = 60

    #screen properties
    screenWidth = 500
    screenHeight = 500

    #set initial player start position
    rect.x = 250
    rect.y = 400

    #making a score counter
    font = pygame.font.SysFont('comicsans', 30, True)
    scoreValue = 0

    #determines whether the button has been pressed
    isPressed = False

    #determines whether the player hits a asteroid
    isCollided = False

    def score(score):
        #get rid of old text
        text = font.render('Score: ' + str(score - 1), 1, (0, 0, 0))
        window.blit(text, (300, 10))
        #write in new text
        text = font.render('Score: ' + str(score), 1, (100, 0, 0))
        window.blit(text, (300, 10))

    #main loop
    run = True
    while run:
        #no delay in this code, frames run as fast as possible
        #gets list of event like keyboard press, mouse, etc and ends the game if the X icon on the top left of the screen is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        asteroids = [asteroid1, asteroid2, asteroid3, asteroid4, asteroid5, asteroid6, asteroid7]
        #loop through every asteroid
        for asteroid in asteroids:
            #starting point
            if  asteroid.y == -75:
                # random position from 0 to 425, so the position for all of them change each time
                asteroid.x = random.randint(0, 425)
            if asteroid.y == screenHeight + 75:
                asteroid.x = random.randint(0, 425)
                asteroid.y = -75

        #make this the same as the background, draws the background black and then redraws everything else
        window.fill((0,0,0))


        #read the x value from the accelerometer and convert it to an int
        x = ser.readline()[3:6]
        xValue = int(x[0:3])

        #change position of the character every frame
        rect.x += float(xValue/150)

        #not reacting fast enough
        #the accelerometer should be changing serial values faster than the spaceship is reading those values

        #draw in the asteroids
        window.blit(asteroidImage1, asteroid1)
        window.blit(asteroidImage2, asteroid2)
        window.blit(asteroidImage3, asteroid3)
        window.blit(asteroidImage4, asteroid4)
        window.blit(asteroidImage5, asteroid5)
        window.blit(asteroidImage6, asteroid6)
        window.blit(asteroidImage7, asteroid7)

        # draw the spaceship
        window.blit(spaceship, rect)

        #end game screen with final score by drawing text
        if isCollided == True:
            game_over = font.render('PRESS SW1 TO RESET', 1, (255, 255, 255))
            window.blit(game_over, (75, 250))
            final_score = font.render('FINAL SCORE WAS: ' + str(finalScore), 1, (255, 255, 255))
            window.blit(final_score, (50, 125))

        #if button is pressed
        on = int(ser.readline()[21:25])
        if on == 1:
            isPressed = True
        #score logic
        if isPressed == False and isCollided == False:
            # increment the score by 1
            scoreValue = scoreValue + 1
            score(scoreValue)
            #make the asteroids move at a set velocity downwards (+y direction is positive in pygame)
            for asteroid in asteroids:
                asteroid.y += asteroidVelocity
        #the button is pressed to start the game again
        elif isPressed == True:
            #set the score back to 0
            scoreValue = 0
            score(scoreValue)
            isPressed = False
            isCollided = False
            asteroidVelocity = 1

        #goes down to 0 and keeps counting up sometimes as ser.readline()[21:25] is sometimes printed twice

        #stay within game bounds, if you hit and edge it throws you back to the center
        if rect.x < 0:
            rect.x = screenWidth/2
        elif rect.x > screenWidth:
            rect.x = screenWidth/2

        #collision code
        if rect.colliderect(asteroid1) or rect.colliderect(asteroid2) or rect.colliderect(asteroid3) or rect.colliderect(asteroid4) or rect.colliderect(asteroid5) or rect.colliderect(asteroid6) or rect.colliderect(asteroid7):
            #send the asteroids off screen when the reset screen pops up and prevent them from moving down
            asteroid1.y = -75
            asteroid2.y = -75
            asteroid3.y = -75
            asteroid4.y = -75
            asteroid5.y = -75
            asteroid6.y = -75
            asteroid7.y = -75
            asteroidVelocity = 0
            isCollided = True
            finalScore = scoreValue

        #update the game display
        pygame.display.update()
    pygame.quit()