__author__ = 'Dr G'

import random as R
import pygame as P

P.init()

#set up the display
screen_width, screen_height = P.display.Info().current_w, P.display.Info().current_h
screen = P.display.set_mode([screen_width, screen_height],P.FULLSCREEN)

P.display.set_caption("Bee Quick")

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#MAX_RATE = int(screen_width*10/2400)
MAX_RATE = 3


class Bee(object):
    """Bee racer.

    Create a bee with necessary parameters to draw it

    Attributes:
        screen_size: the size of the display screen in pixels

    """

    def __init__(self,bee_num):
        """Inits Bee."""
        self.image = P.image.load('media/bee{}.png'.format(bee_num))
        self.size = int(screen_width/12)
        self.image = P.transform.scale(self.image,(self.size,self.size))
        self.x = 0
        self.y = (bee_num - 0.5)*screen_height/3 - self.size/2
        self.rectangle = self.image.get_rect().move(self.x,self.y)
        self.rate= R.randrange(1,MAX_RATE+1)
        self.moves = 0
        self.finish = False

    def update(self):
        """Performs operation blah."""
        self.moves += 1
        if self.moves > R.randrange(5,50):
            #self.rate= R.choice([self.rate,max(1,self.rate-1),min(MAX_RATE,self.rate+1)])
            self.rate= R.randrange(max(1,self.rate-1),min(MAX_RATE+1,self.rate+2))

            self.moves = 0
        if not self.rectangle.collidepoint((screen_width,self.y)):
            self.rectangle = self.rectangle.move(self.rate,0)
        if not self.finish:
            #self.rectangle = self.rectangle.move(self.rate,0)
            if self.rectangle.collidepoint((screen_width*11/12,self.y)):
                self.finish = int(round((P.time.get_ticks() - start),-1)/10)
                print(self.finish)
                print("{}:{}".format(self.finish//100,str(self.finish%100).zfill(2)))
                print(self.rate)


#make the bees
bee_array = []
for i in range(1,4):
    bee_array.append(Bee(i))


#Loop until the user clicks the close button.
play = True
clock = P.time.Clock()
loop_rate = 100 #number of times per second does loop

start = P.time.get_ticks()
print(start)
while play:
    clock.tick(loop_rate) #cycle through loop 'rate' times per second

    event = P.event.poll() #did the player do something?

    if event.type == P.QUIT: #player clicked close so quit
        play = False
    elif event.type == P.KEYDOWN:
        if event.key == P.K_ESCAPE:
            play = False

    # Clear the screen and set the screen background
    screen.fill(BLUE)

    # Draw on the screen a GREEN line from (0,0) to (50.75)
    # 5 pixels wide.
    P.draw.line(screen, GREEN, [screen_width/12, 0], [screen_width/12,screen_height], 5)
    P.draw.line(screen, GREEN, [11*screen_width/12, 0], [11*screen_width/12,screen_height], 5)

    for bee in bee_array:
        bee.update()
        screen.blit(bee.image,bee.rectangle)
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    P.display.flip()

# Be IDLE friendly
P.quit()

