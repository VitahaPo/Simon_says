__author__ = 'Vitaliy'
from livewires import games, color
import random

#init screen
games.init(screen_width = 640, screen_height = 480, fps = 50)


def typing(type):
    """type of blink"""
    x, y =1, 1
    if type == 1:
        x, y = -1, 1
    if type == 2:
        x, y = 1, 1
    if type == 3:
        x, y = -1, -1
    if type == 4:
        x, y = 1, -1
    return x,y

class Blink(games.Sprite):
    """blinks when simon says something"""

    #sounds and images for blinks
    GREEN = 1
    RED = 2
    YELLOW = 3
    BLUE = 4
    images = {GREEN : games.load_image('green.bmp'),
              RED : games.load_image('red.bmp'),
              YELLOW : games.load_image('yellow.bmp'),
              BLUE : games.load_image('blue.bmp')}
    sounds = {GREEN : games.load_sound('sound1.wav'),
              RED : games.load_sound('sound2.wav'),
              YELLOW : games.load_sound('sound3.wav'),
              BLUE : games.load_sound('sound4.wav')}
    LIFETIME = 100

    def __init__(self, type):
        """init blink"""
        super(Blink, self).__init__(image = Blink.images[type],
                                    x = games.screen.width/2 + typing(type)[0]*72,
                                    y = games.screen.height/2 - typing(type)[1]*72)
        self.type = type

        Board.m = False
        self.sound = Blink.sounds[type]
        self.sound.play()
        self.lifetime = Blink.LIFETIME

    def update(self):
        #destroy blink and sound
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
            self.sound.stop()
            Board.m = True

class Board(games.Sprite):
    #simon board
    board_image = games.load_image('board.bmp')
    r = None #parametrs for realising sequence of blinking
    l = None #it's be better to use any other algorithm
    m = None #in new version
    i = None

    def __init__(self, game, x, y):
        #reinit board
        super(Board, self).__init__(image = Board.board_image,
                                    x = x,
                                    y = y,
                                    interval = 50)
        self.game = game

    def update(self):
        #human_move
        if games.keyboard.is_pressed(games.K_KP4) and Board.r and Board.m == True:
            Board.r = False
            type = 1
            self.game.human_say(type)
        elif games.keyboard.is_pressed(games.K_KP5) and Board.r and Board.m == True:
            Board.r = False
            type = 2
            self.game.human_say(type)
        elif games.keyboard.is_pressed(games.K_KP1) and Board.r and Board.m == True:
            Board.r = False
            type = 3
            self.game.human_say(type)
        elif games.keyboard.is_pressed(games.K_KP2) and Board.r and Board.m == True:
            Board.r = False
            type = 4
            self.game.human_say(type)

    def tick(self):
        #simon say
        if Board.r == False and Board.l == True and Board.m == True:
            type = self.game.simon_sequence[Board.i]
            new_blink = Blink(type)
            games.screen.add(new_blink)
            if Board.i == len(self.game.simon_sequence) - 1:
                Board.r = True
                Board.l = False
            Board.i += 1

class Game(object):
    """main game"""
    lose_sound = games.load_sound('explosion.wav')
    win_sound = games.load_sound('missile.wav')

    def __init__(self):
        """init board and information"""
        new_board = Board(game = self,
                          x = games.screen.width/2,
                          y = games.screen.height/2)
        games.screen.add(new_board)
        self.new_game()

        #init sequences
        self.simon_sequence = []
        self.human_sequence = []

        #information
        self.init_inf()

        #start from simon
        self.simon_say()

        #init loop
        games.mouse.is_visible = False
        games.screen.mainloop()

    def init_inf(self):
        #score
        self.score = games.Text(value = 0,
                                size = 40,
                                color = color.white,
                                bottom = games.screen.height - 5,
                                right = games.screen.width - 10)
        games.screen.add(self.score)

        #keyboard information
        Num4 = games.Text(value = 'Num4',
                           size = 40,
                           color = color.green,
                           y = games.screen.height/2 - 150,
                           x = games.screen.width/2 - 150)
        games.screen.add(Num4)
        Num5 = games.Text(value = 'Num5',
                           size = 40,
                           color = color.red,
                           y = games.screen.height/2 - 150,
                           x = games.screen.width/2 + 150)
        games.screen.add(Num5)
        Num1 = games.Text(value = 'Num1',
                           size = 40,
                           color = color.yellow,
                           y = games.screen.height/2 + 150,
                           x = games.screen.width/2 - 150)
        games.screen.add(Num1)
        Num2 = games.Text(value = 'Num2',
                           size = 40,
                           color = color.blue,
                           y = games.screen.height/2 + 150,
                           x = games.screen.width/2 + 150)
        games.screen.add(Num2)

    def simon_say(self):
        """simon say"""
        self.simon_sequence.append(random.randint(1, 4))
        print('simon: ', self.simon_sequence) #additional console information for testing
        Board.i = 0

    def human_say(self, type):
        """human say"""
        #create new blink
        self.human_sequence.append(type)
        print('human: ',self.human_sequence)
        new_blink = Blink(type)
        games.screen.add(new_blink)

        #check for sequense true
        if self.human_sequence == self.simon_sequence:
            Game.win_sound.play()
            self.score.value += 10
            self.score.right = games.screen.width - 10
            self.human_sequence = []
            self.simon_say()
            Board.r = False
            Board.l = True

        #check for element sequence[i] true
        else:
            if self.human_sequence[-1] == self.simon_sequence[len(self.human_sequence)-1]:
                Board.r = True
            else:
                #if sequense false -  loose and start new game
                Game.lose_sound.play(2)
                message = games.Message(value = 'YOU LOSE! Score: ' + str(self.score.value),
                                size = 40,
                                color = color.white,
                                y = 20,
                                x = games.screen.width/2,
                                lifetime = 3 * games.screen.fps,
                                after_death = self.new_game)
                games.screen.add(message)
                self.score.value = 0
                self.score.right = games.screen.width - 10

    def new_game(self):
        """start new game"""
        message = games.Message(value = 'NEW GAME',
                                size = 40,
                                color = color.white,
                                y = 20,
                                x = games.screen.width/2,
                                lifetime = 3 * games.screen.fps,
                                after_death = self.init)
        games.screen.add(message)

    def init(self):
        """init board parametrs"""
        self.simon_sequence = []
        self.human_sequence = []
        self.simon_say()
        Board.r = False
        Board.l = True
        Board.m = True
        Board.i = 0


#start game
Game()

