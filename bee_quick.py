""" Project name.

Description
"""

__copyright__ = "(c) Geoff Goldrick 2014"
__license__ = "Creative Commons Attribution-ShareAlike 2.0 Generic License."
__author__ = "Prof. Stick"
__version__ = "0.1"
__revision__ = "20150925"

""" revision notes:
0.1 set layout grid based on screen size

"""
import random as R
import pygame as P

P.init()

#set up the display
screen_width, screen_height = P.display.Info().current_w, P.display.Info().current_h
screen = P.display.set_mode([screen_width, screen_height],P.FULLSCREEN)
P.display.set_caption("Bee Quick")

#set up a grid for layout assuming display ratio of 16:9
GRID_X = int(screen_width/16)
GRID_Y = int(screen_height/9)

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#define max rate of movement
MAX_RATE = 3

#define fonts
big_font = P.font.SysFont("monospace",GRID_X)
font = P.font.SysFont("monospace",int(GRID_X/2))
small_font = P.font.SysFont("monospace",int(GRID_X/3))

#much as I hate global variables, I feel lazy



class Bee(object):
    """Bee racer.

    Create a bee with necessary parameters to draw it

    Attributes:

    """

    def __init__(self,bee_num):
        """Inits Bee."""
        self.id = bee_num
        self.image = P.image.load('media/bee{}.png'.format(self.id))
        self.image = P.transform.scale(self.image,(GRID_X,GRID_Y))
        self.x = 0
        self.y = (bee_num*3-2)*GRID_Y
        self.rectangle = self.image.get_rect().move(self.x,self.y)
        self.rate= R.randrange(1,MAX_RATE+1)
        self.moves = 0
        self.start = False
        self.finish = False
        self.home = False #has bee completely crossed the finish line

    def update(self):
        """Updates the bees during the race."""
        if not self.start:
            self.start = P.time.get_ticks()

        if not self.home:
            self.moves += 1

            #change the rate at random intervals
            if self.moves > R.randrange(5,50):
                #change rate by +-1 or 0, but never more than MAX_RATE or less than 0
                self.rate= R.randrange(max(1,self.rate-1),min(MAX_RATE+1,self.rate+2))
                self.moves = 0

            self.rectangle = self.rectangle.move(self.rate,0)

            if self.rectangle.collidepoint((screen_width,self.y)):
                self.home = True


        if not self.finish:
            if self.rectangle.collidepoint((screen_width - GRID_X,self.y)):
                self.finish = int(round((P.time.get_ticks() - self.start),-1)/10)

class letter(object):
    """A letter of the guess word.

    holds all the details of a letter including its position on the screen
    and whether it has been selected

    Attributes:
        alpha: the letter of the alphabet
        image: the letter rendeRED as an image.
        position: the coordinates of the image.
        selected: a boolean indicating whether the letter has been selected
    """

    def __init__(self, alpha, colour=RED):
        """Inits letter.

        arguments:
            alpha - the letter of the alphabet
            colour - the colour to display the letter. the default is RED

        """
        self.alpha = alpha
        self.image = font.render(alpha,True,colour)
        self.position = [0,0]
        self.selected = False
        self.rect = P.Rect(self.position,self.image.get_size())

    def update(self):
        """updates the status and rect of the letter when the parameters change."""
        if self.selected:
            self.image = font.render(self.alpha,True,DARK_RED)
        else:
            self.image = font.render(self.alpha,True,RED)

        self.rect = P.Rect(self.position,self.image.get_size())



def draw_track():
    ''' Draws the race track
    '''
    # Clear the screen and set the screen background
    screen.fill(BLUE)

    # Draw finish lines 5 pixels wide.
    P.draw.line(screen, GREEN, [GRID_X, 0], [GRID_X,screen_height], 5)
    P.draw.line(screen, GREEN, [screen_width - GRID_X, 0], [screen_width - GRID_X,screen_height], 5)

def display_splash():
    return 'start'

def start_race(start_time,count_array):
    status = 'start'

    print('start time: {}'.format(start_time))
    time_elapsed = P.time.get_ticks() - start_time
    count = time_elapsed//1000
    print(count)

    if count > 4:
        status = 'race'
    else: screen.blit(count_array[count].image,(GRID_X*8,0))
    return status

def run_race(b_array):
    status = 'done'
    for bee in b_array:
        bee.update()
        if not bee.home: status = 'race'
    return status

def display_finish(b_array):
    for b in b_array:
        print('Bee {} started {} finished in {}:{}'.format(b.id,b.start,b.finish//100,str(b.finish%100).zfill(2)))



def main():
    race_started = False

    #make the bees
    bee_array = []
    for i in range(1,4):
        bee_array.append(Bee(i))

    countdown_array = []
    for i in range(0,5):
        countdown_array.append(letter(str(5-i)))

    #Loop until the user clicks the close button.
    play = True
    clock = P.time.Clock()
    loop_rate = 100 #number of times per second does loop
    state = 'splash' #keeps track of the state of the game

    #start = P.time.get_ticks()

    while play:
        clock.tick(loop_rate) #cycle through loop 'rate' times per second

        event = P.event.poll() #did the player do something?

        if event.type == P.QUIT: #player clicked close so quit
            play = False
        elif event.type == P.KEYDOWN:
            if event.key == P.K_ESCAPE:
                play = False

        #draw the track
        draw_track()

        if state == 'splash':
            state = display_splash()

        elif state == 'start':
            if not race_started: race_started = P.time.get_ticks()
            state = start_race(race_started,countdown_array)

        elif state == 'race':
            state = run_race(bee_array)

        elif state == 'done':
            state = display_finish(bee_array)

        for bee in bee_array:
            screen.blit(bee.image,bee.rectangle)

        P.display.flip()

    # Be IDLE friendly
    P.quit()

if __name__ == '__main__':
    main()