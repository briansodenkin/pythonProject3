import random
import math
import pygame
import eyed3
import time

# UI
# screen initialise
pygame.display.init()
pygame.mixer.init()
play_screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption("AIST2010")
tmp = pygame.Surface((1200, 750))
tmp.fill((255, 255, 255))
# setting the background
base = pygame.Surface((1200, 750))
base = base.fill((255, 255, 255))

# Font
pygame.init()
main_font = pygame.font.Font("Azteca-Condensed.ttf", 40)
game_background = pygame.image.load("game_background.jpg").convert()
background = pygame.image.load("background.jpg").convert()

# setting the button
# button of the setting, game, exit
pygame.init()

temp_score = 0
increase = 0
rest = 0

Killed_Note = 0
Combo = 0
Perfect_count = 0
Great_count = 0
Miss_count = 0
isFirstPressed = False
MODE_FADE_OUT = False


class button(pygame.sprite.Sprite):
    def __init__(self, screen, message, x, y, font_size, action=None):
        pygame.sprite.Sprite.__init__(self)
        self.message = message
        self.screen = screen
        self.x = x
        self.y = y
        self.font_size = font_size
        self.action = action
        self.fadeOut = pygame.Surface((1200, 750))
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((0, 0, 0))
        self.image.set_alpha(0)
        self.fadeOut.fill((255, 255, 255))
        self.fadeOut.set_alpha(0)

    def update(self, button_type):
        font = pygame.font.Font('Azteca-Condensed.ttf', self.font_size)
        txt = font.render(self.message, True, (0, 0, 0))
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if self.x + 120 > mouse[0] > self.x and self.y + 80 > mouse[1] > self.y:
            # Enlarge if the mouse close to the button
            font = pygame.font.Font('Azteca-Condensed.ttf', self.font_size + 30)
            txt = font.render(self.message, True, (255, 255, 255))
            if click[0] == True and button_type == 1:
                print("GAME")
                pygame.time.delay(500)
                return 2
            elif click[0] == True and button_type == 2:
                print("SETTING")
                pygame.time.delay(500)
                return 3
            elif click[0] == True and button_type == 3:
                print("EXIT")
                pygame.time.delay(150)
                return 4
        self.screen.blit(txt, [self.x, self.y])


# button of the difficulty
class button_difficulty(pygame.sprite.Sprite):
    def __init__(self, message_1, message_2, screen, x1, y1, x2, y2, ):
        pygame.sprite.Sprite.__init__(self)
        self.selection = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.image.set_alpha(0)
        self.msg_1 = message_1
        self.msg_2 = message_2
        self.screen = screen

    def update(self, selected_num):
        easy = 0
        hard = 0
        font1 = pygame.font.Font('Azteca-Condensed.ttf', 30)
        font2 = pygame.font.Font('Azteca-Condensed.ttf', 20)
        if selected_num == 1:
            easy = font1.render(self.msg_1, True, (0, 255, 0))
            hard = font2.render(self.msg_2, True, (0, 0, 0))
            self.selection = 1
        if selected_num == 2:
            hard = font1.render(self.msg_2, True, (225, 0, 0))
            easy = font2.render(self.msg_1, True, (0, 0, 0))
            self.selection = 2
        self.screen.blit(easy, [self.x1, self.y1])
        self.screen.blit(hard, [self.x2, self.y2])


class button_back(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen

    def update(self):
        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        font = pygame.font.Font('Azteca-Condensed.ttf', 20)
        text = font.render("Back", True, (255, 255, 255))
        if 60 > self.mouse[0] > 10 and 10 < self.mouse[1] < 60:
            font = pygame.font.Font('Azteca-Condensed.ttf', 40)
            text = font.render("Back", True, (255, 0, 0))
            if self.click[0] == 1:
                return True
        self.screen.blit(text, [self.x, self.y])


game_button = button(play_screen, "Game", 300, 100, 50)
setting_button = button(play_screen, "Setting", 300, 300, 50)
exit_button = button(play_screen, "Exit", 300, 500, 50)
buttons = pygame.sprite.RenderPlain([game_button, setting_button, exit_button])
back_button = button_back(play_screen, 25, 25)
difficulty = button_difficulty("Beginner", "Advance", play_screen, 120, 600, 240, 600)


# ================================= Button End =========================================================================

# =================================== Song list ========================================================================
class Song(pygame.sprite.Sprite):
    Speed_tuple = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

    def __init__(self, file, title, artist, level, highlight=0, album_art=None, screen=None):
        pygame.sprite.Sprite.__init__(self)
        self.sound = pygame.mixer.Sound(file)
        self.file = file
        self.tag = eyed3.load(file)
        self.song_title = title
        self.artist = artist
        self.playtime = pygame.mixer.Sound.get_length(self.sound)
        self.mode = 1
        self.speed = 0
        self.level = level
        self.highlight = highlight
        self.note1 = pygame.Surface([15, 65])
        self.note2 = pygame.Surface([15, 65])
        self.note3 = pygame.Surface([15, 65])
        self.album_art = album_art
        self.screen = screen
        self.Group_Note_Map = []
        self.Group_Note_Map_SyncTime = []
        self.Group_LongNote_Map_Length = []
        self.index_map = 0
        self.index_SyncTime = 0
        self.index_LongNote = 0

    def add_note(self, note_type, sync_time, length=None):
        self.Group_Note_Map.append(note_type)
        self.Group_Note_Map_SyncTime.append(sync_time)
        if length is not None:
            self.Group_LongNote_Map_Length.append(length)
        else:
            self.Group_LongNote_Map_Length.append(0)

    def get_note(self):
        if self.mode == 1:
            return self.Group_Note_Map[self.index_map]

    def get_sync(self):
        if self.mode == 1:
            return self.Group_Note_Map_SyncTime[self.index_SyncTime]

    def move_sync_index(self):
        if self.index_SyncTime < len(self.Group_Note_Map_SyncTime) - 1:
            self.index_SyncTime += 1
            return True
        return False

    def move_index(self):
        if self.index_map < len(self.Group_Note_Map) - 1:
            self.index_map += 1

    def get_note_count(self):
        if self.mode == 1:
            return self.Group_Note_Map.__len__() - 1

    def init_index(self):
        self.index_SyncTime = 0
        self.index_map = 0
        self.index_LongNote = 0


class note(pygame.sprite.Sprite):
    Killed_Note = 0
    Combo = 0
    onCount = 0
    MODE_FADE_OUT = None

    def __init__(self, screen, width, height, type, speed=10, isLongNote=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.screen = screen
        self.width = width
        if type == 1:
            self.image = pygame.image.load("KEY_A.jpg").convert()
        elif type == 2:
            self.image = pygame.image.load("KEY_A.jpg").convert()
        else:
            self.image = pygame.image.load("KEY_A.jpg").convert()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = 1377
        self.type = type
        self.isLongNote = isLongNote
        self.LongNote_judge = 3
        if type == 1:
            self.rect.y = 128
        elif type == 2:
            self.rect.y = 256
        else:
            self.rect.y = 384

    def update(self, type=0, KeyPressed=False, KeyUp=False):
        self.rect.x -= self.speed

        if self.note_fade_out():
            if self.onCount == 0:
                # When This Loop Was First Called, init the start_time
                self.start_time = time.time()
            end_time = time.time() - self.start_time
            self.image.set_alpha(255 - (end_time * 555))
            self.onCount += 1
            if end_time > 1.25:
                self.kill()
                killed_note(1)
                self.onCount = 0
                self.note_fade_out(False)
            return
        if self.isLongNote:
            if isFirstPressed:
                if (self.rect.x + self.width) / 3 * 2 < 135 and KeyUp:
                    print('done')
                    combo(1)
                    self.note_fade_out(True)
                    score(self.LongNote_judge)
                    is_first_pressed(False)
                elif KeyUp:
                    print('miss1')
                    combo(0, True)
                    self.note_fade_out(True)
                    score(3)
                    is_first_pressed(False)
            elif 135 < self.rect.x < 165 and KeyPressed and self.type == type:
                print('miss')
                combo(0, True)
                self.note_fade_out(True)
                self.LongNote_judge = 3
                miss(1)
            elif 110 <= self.rect.x < 135 and KeyPressed and self.type == type:
                print('great')
                is_first_pressed(True)
                self.LongNote_judge = 2
                self.kill()
            elif 78 <= self.rect.x < 110 and KeyPressed and self.type == type:
                print('perfect1')
                is_first_pressed(True)
                self.LongNote_judge = 1
                self.kill()
            elif not KeyPressed and self.rect.x < 78:
                if self.rect.x + self.width < 230:
                    print('miss2')
                    combo(0, True)
                    self.note_fade_out(True)
                    score(3)
        else:
            if 135 < self.rect.x < 165 and KeyPressed and self.type == type:
                print('miss')
                combo(0, True)
                self.note_fade_out(True)
                score(3)
                miss(1)
            elif 110 <= self.rect.x < 135 and KeyPressed and self.type == type:
                print('great')
                combo(1)
                self.note_fade_out(True)
                score(2)
                great(1)
                self.kill()
            elif 78 < self.rect.x < 110 and KeyPressed and self.type == type:
                print('perfect')
                combo(1)
                self.note_fade_out(True)
                score(1)
                perfect(1)
                self.kill()
            elif self.rect.x < 78:
                print('miss3')
                combo(0, True)
                self.note_fade_out(True)
                score(3)
                miss(1)

    def re_init(self):
        self.alive()
        self.rect.x = 1377

    def note_fade_out(self, bool=None):
        if bool == None:
            return self.MODE_FADE_OUT
        self.MODE_FADE_OUT = bool
        return self.MODE_FADE_OUT


def combo(increase, init=False):
    global Combo
    if init:
        Combo = 0
    Combo += increase
    return Combo


def killed_note(increase, init=False):
    global Killed_Note
    if init:
        Killed_Note = 0
    Killed_Note += increase
    return Killed_Note


def perfect(increase, init=False):
    global Perfect_count
    if init:
        Perfect_count = 0
    Perfect_count += 1
    return Perfect_count


def great(increase, init=False):
    global Great_count
    if init:
        Great_count = 0
    Great_count += 1
    return Great_count


def miss(increase, init=False):
    pygame.mixer.Sound("Sound\mixkit-apartment-buzzer-bell-press-932.wav").play()
    global Miss_count
    if init:
        Miss_count = 0
    Miss_count += 1
    return Miss_count


def is_first_pressed(bool):
    global isFirstPressed
    isFirstPressed = bool
    return isFirstPressed


def score(__type, selected_map=None):
    global temp_score
    global rest
    global increase
    if __type == -1:
        # INIT
        temp_score = 0
        rest = 0
        increase = 0

    if not selected_map == None:
        rest = math.fmod(100000, selected_map.get_note_count())
        increase = (100000 - rest) / selected_map.get_note_count()

    if __type == 1:
        # PERFECT
        temp_score += increase
    elif __type == 2:
        # GREAT
        temp_score += (increase / 10) * 8
    elif __type == 3:
        # MISS
        temp_score += 0

    return int(temp_score)


song1 = Song("Cash_Cash_-_Overtime.ogg", "Overtime", "Cash Cash", 5)
song2 = Song("Zedd - Find You ft. Matthew Koma & Miriam Bryant (TAK Remix).ogg", "Find You", "Zedd", 2)
song3 = Song("Clarity_Zedd_Union_Mix_Zedd_320k_mp3.ogg", "Clarity(zedd union remix)", "Zedd", 1)
song_list_list = [song1, song2, song3]


class gensonglist(pygame.sprite.Sprite):
    List = []
    List_map = []
    List_font = []
    List_Background = []
    list_count = 0
    start = 200
    margin = 50
    margin_background = 600
    MODE_FADE_OUT = False
    speed = 0
    first_pos = 0
    pos = 0
    alpha_value = 180
    alpha_value_change_speed = 0
    SongSpeed = 1
    main_font = pygame.font.Font("Azteca-Condensed.ttf", 35)

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.end_time = time.time()
        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        self.image = pygame.Surface([400, 750])
        self.background = pygame.Surface((1200, 750))
        self.screen = screen
        self.list_focus = 0

    def append(self, title, background_image, artist, d, songs=None):
        self.List.append(title)
        self.List_font.append(self.main_font.render(title, True, (0, 0, 0)))
        self.List_Background.append(background_image)
        self.List_map.append(songs)
        self.list_count += 1

    def update(self, up=False, down=False, Sort_A=False, Sort_B=False, enter=False, SpeedUp=False, SpeedDown=False):
        self.margin = 50
        self.screen.blit(self.background, [0, 0])
        selected = pygame.Surface([1000, 60])
        selected.fill((255, 255, 255))

        if up:
            self.list_focus -= 1
            print("====================================")
            print(self.list_focus)
            self.start += 60
            sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
            sound.play()

        if down:
            self.list_focus += 1
            print("************************************")
            print(self.list_focus)
            self.start -= 60
            sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
            sound.play()

        if enter:
            self.cover = pygame.Surface([1000, 60])
            self.start_time = time.time()
            self.cover.fill((0, 0, 255))
            pygame.mixer.Sound("KEY_A_SOUND.wav").play()

        self.margin_background = 0
        for image in self.List_Background:
            self.screen.blit(image, [0, 0])

        i = 0
        for title in self.List:
            self.List_font[i] = (self.main_font.render(title, True, (0, 0, 0)))
            i += 1
        # only focused item Set Font with WHITE color
        self.List_font[self.list_focus] = self.main_font.render(self.List[self.list_focus], True, (0, 250, 0))

        # OUTPUT PART
        for i in self.List_font:
            if i == self.List_font[self.list_focus]:
                self.screen.blit(i, [400, self.start + self.margin])
                self.margin += 60
                continue
            self.screen.blit(i, [450, self.start + self.margin])
            self.margin += 60

        SongsList_txt = self.main_font.render('Song List', True, (250, 250, 0))
        self.screen.blit(SongsList_txt, (100, 250))
        s = "(%d / %d)" % (self.list_focus + 1, self.list_count)
        self.screen.blit(self.main_font.render(s, True, (250, 250, 0)), (100, 300))

        # Back Button
        if 75 > self.mouse[0] > 25 and 25 < self.mouse[1] < 50:
            if self.click[0] == 1:
                self.MODE_FADE_OUT = False


song_list = gensonglist(play_screen)
for song in song_list_list:
    song_list.append(song.song_title, pygame.image.load("game_background.jpg").convert(), song.artist, song.level)


# ================================= Song list End ======================================================================

# =================================== Setting ==== =====================================================================
# Setting
class setting_list(pygame.sprite.Sprite):
    main_font = pygame.font.Font("Azteca-Condensed.ttf", 35)

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.menuBar = pygame.Surface((500, 740))
        self.menuBar.fill((0, 0, 0))
        self.menuBar_pos = 600
        self.screen = screen

    def update(self):
        if not (self.menuBar_pos < 750):
            self.screen.blit(self.menuBar, [self.menuBar_pos, 0])
            self.menuBar_pos -= 10
        else:
            self.screen.blit(self.menuBar, [self.menuBar_pos, 0])
            self.screen.blit(self.main_font.render("Setting", True, (0, 0, 0)), (1000, 200))


setting = setting_list(play_screen)


# =================================== Setting End ======================================================================


# =================================== Node =============================================================================
class node(pygame.sprite.Sprite):
    count = 0

    def __init__(self, X, Y, width, height, type, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.screen = screen
        self.width = width
        self.height = height
        if type == 1:
            self.image = pygame.image.load("KEY_A.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
        elif type == 2:
            self.image = pygame.image.load("KEY_A.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
        elif type == 3:
            self.image = pygame.image.load("KEY_A.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")

        self.rect = self.image.get_rect()
        self.rect.center = (X, Y)
        self.sound.set_volume(1.5)

    def update(self, Keypressed, KeyUp, type=0):

        if Keypressed:
            self.image = pygame.image.load("KEY_A.jpg").convert()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.sound.play()
        elif KeyUp:
            if type == 1:
                self.image = pygame.image.load("KEY_A.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif type == 2:
                self.image = pygame.image.load("KEY_A.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif type == 3:
                self.image = pygame.image.load("KEY_A.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))


node1 = node(110, 192, 47, 128, 1, play_screen)
node2 = node(110, 320, 47, 128, 2, play_screen)
node3 = node(110, 448, 47, 128, 3, play_screen)
nodes = pygame.sprite.RenderPlain([node1, node2, node3])


# =================================== Node End =========================================================================
# =================================== MAP Start =========================================================================
class Map(pygame.sprite.Sprite):
    Speed_tuple = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

    def __init__(self, file, title, artist, level, highlight=0, album_art=None, screen=None):
        # Read the Play time of MP3 File
        pygame.sprite.Sprite.__init__(self)
        self.sound = pygame.mixer.Sound(file)
        self.file = file
        self.tag = eyed3.load(file)

        self.song_title = title
        self.artist = artist
        self.playtime = pygame.mixer.Sound.get_length(self.sound)  # Second
        self.mode = 1  # Easy 1/ Hard 2
        self.speed = 0

        self.level = level
        # highlight is the time when you want to set
        self.highlight = highlight

        self.note1 = pygame.Surface([15, 65])
        self.note2 = pygame.Surface([15, 65])
        self.note3 = pygame.Surface([15, 65])
        if (album_art != None):
            self.album_art = album_art
        if (screen != None):
            self.screen = screen

        # Easy Mode Map
        self.Group_Note_Map = []
        self.Group_Note_Map_SyncTime = []
        self.Group_LongNote_Map_Length = []
        self.index_map = 0
        self.index_SyncTime = 0
        self.index_LongNote = 0

        # Hard Mode Map
        self.Group_Note_Map_Hard = []
        self.Group_Note_Map_SyncTime_Hard = []
        self.Group_LongNote_Map_Length_Hard = []
        self.index_map_Hard = 0
        self.index_SyncTime_Hard = 0
        self.index_LongNote_Hard = 0

    def add_note(self, type, sync_time):
        self.Group_Note_Map.append(type)
        self.Group_Note_Map_SyncTime.append(sync_time)

    def add_note_hard(self, type, sync_time):
        self.Group_Note_Map_Hard.append(type)
        self.Group_Note_Map_SyncTime_Hard.append(sync_time)

    def set_speed(self, i):
        self.speed = self.Speed_tuple[i]

    def set_mode(self, mode):
        self.mode = mode

    def get_title(self):
        return self.song_title

    def get_artist(self):
        return self.artist

    def get_level(self):
        return self.level

    def get_album_artist(self):
        return self.album_art

    def get_note(self):
        if self.mode == 1:
            return self.Group_Note_Map[self.index_map]
        else:
            return self.Group_Note_Map_Hard[self.index_map_Hard]

    def get_sync(self):
        if self.mode == 1:
            return self.Group_Note_Map_SyncTime[self.index_SyncTime]
        else:
            return self.Group_Note_Map_SyncTime_Hard[self.index_SyncTime_Hard]

    def move_sync_index(self):
        if self.mode == 1:
            if self.index_SyncTime < len(self.Group_Note_Map_SyncTime) - 1:
                self.index_SyncTime += 1
                return True
            return False
        else:
            if self.index_SyncTime_Hard < len(self.Group_Note_Map_SyncTime_Hard) - 1:
                self.index_SyncTime_Hard += 1
                return True
            return False

    def move_index(self):
        if self.mode == 1:
            if self.index_map < len(self.Group_Note_Map) - 1:
                self.index_map += 1
        else:
            if self.index_map_Hard < len(self.Group_Note_Map_Hard) - 1:
                self.index_map_Hard += 1

    def get_note_count(self):
        # Last Note is Dummy Note
        if self.mode == 1:
            return self.Group_Note_Map.__len__() - 1
        else:
            return self.Group_Note_Map_Hard.__len__() - 1

    def init_index(self):
        self.index_SyncTime = 0
        self.index_map = 0
        self.index_LongNote = 0

        self.index_SyncTime_Hard = 0
        self.index_map_Hard = 0
        self.index_LongNote_Hard = 0


# Last Note is Dummy Note;
# =========================================================

song1.add_note(2, 3)
song1.add_note(3, 5)
song1.add_note(1, 7)
song1.add_note(2, 8)
song1.add_note(3, 9)
song1.add_note(1, 10)
song1.add_note(2, 11)
song1.add_note(3, 12)
song1.add_note(1, 13)
song1.add_note(2, 14)
song1.add_note(3, 15)
song1.add_note(1, 16)
song1.add_note(2, 17)
song1.add_note(3, 18)
song1.add_note(1, 19)
song1.add_note(2, 20)
song1.add_note(3, 21)
song1.add_note(1, 22)
song1.add_note(2, 23)
song1.add_note(3, 24)
song1.add_note(1, 25)
song1.add_note(2, 26)
song1.add_note(3, 27)
song1.add_note(1, 28)
song1.add_note(2, 28.5)
song1.add_note(3, 28.7)
song1.add_note(1, 29)
song1.add_note(2, 30.1)
song1.add_note(3, 31)
song1.add_note(1, 32)
song1.add_note(2, 33.5)
song1.add_note(3, 34)
song1.add_note(1, 36)
song1.add_note(2, 37)
song1.add_note(3, 39)
song1.add_note(1, 42)
song1.add_note(2, 43)
song1.add_note(3, 44)
song1.add_note(1, 45)
song1.add_note(2, 45.6)
song1.add_note(3, 46.3)
song1.add_note(1, 47)
song1.add_note(2, 48.5)
song1.add_note(3, 49)
song1.add_note(1, 51)
song1.add_note(2, 52)
song1.add_note(3, 55)

song1.add_note(3, 3)

song2.add_note(1, 5)
song2.add_note(3, 7)
song2.add_note(4, 9)

song2.add_note(1, 1)

# =================================== MAP End =========================================================================

# =================================== Game Start =========================================================================

# First
# UI with 3 buttons : MAIN_PAGE
# UI with 3 songs : SONG_PAGE
# UI FOR GAME : GAME_PAGE
MAIN_PAGE = True
SONG_PAGE = False
GAME_PAGE = False
SET_PAGE = False
MAIN_FADE_OUT_STATE = False
COMPLETE_STATE = False
GAME_READY_STATE = False
PAUSE = False
DIFFICULTY = False
selected = 1
NoteList = []
NoteList_Drawer = []
Note_Count = 0
MODE_NOTE_FALL = False
done = False
clock = pygame.time.Clock()
now_item = 0
start_time = 0
comp = 0
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            done = True

        if event.type == pygame.KEYDOWN and MAIN_FADE_OUT_STATE:
            if event.key == pygame.K_KP_ENTER:
                GAME_PAGE: True
                GAME_READY_STATE = True
                pygame.mixer.music.fadeout(1500)

        if event.type == pygame.KEYDOWN and SONG_PAGE == True:
            if event.key == pygame.K_UP:
                print("UP")
                song_list.update(True, False)

            if event.key == pygame.K_DOWN:
                print("DOWN")
                song_list.update(False, True)

            if event.key == pygame.K_RETURN:
                print("ENTER")
                song_list.update(False, False, False, False, True)
                start_time = time.time()
                GAME_PAGE = True
                GAME_READY_STATE = True
                SONG_PAGE = False
                MAIN_PAGE = False

            if event.key == pygame.K_ESCAPE:
                SONG_PAGE = False
                MAIN_PAGE = True
                pygame.mixer.music.stop()
                pygame.time.delay(300)
    # Main Page
    if MAIN_PAGE:
        play_screen.fill((255, 255, 255))
        play_screen.blit(background, [0, 0])
        buttons.draw(play_screen)

        if game_button.update(1) == 2:
            print("GAME START")
            MAIN_PAGE = False
            SONG_PAGE = True

        if setting_button.update(2) == 3:
            print("Setting")
            MAIN_PAGE = False
            SONG_PAGE = False
            SET_PAGE = True

        if exit_button.update(3) == 4:
            print("EXIT")
            pygame.mixer.music.fadeout(2700)
            pygame.time.delay(3000)
            pygame.mixer.music.pause()
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            exit()
        pygame.display.flip()
        clock.tick(60)

    elif SONG_PAGE:
        play_screen.fill((255, 255, 255))
        now_item = song_list.list_focus
        song_list.update()
        if back_button.update() and MAIN_FADE_OUT_STATE == False:
            MAIN_PAGE = True
            SONG_PAGE = False
            pygame.time.delay(100)
        if back_button.update() and MAIN_FADE_OUT_STATE:
            MAIN_FADE_OUT_STATE = False
            pygame.time.delay(100)
        difficulty.update(selected)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 > mouse[0] > 120 and 600 < mouse[1] < 680:
            if click[0] == 1:
                print("=======BEGINNER======")
                pygame.mixer.Sound("KEY_A_SOUND.wav").play()
                selected = 1
                difficulty.update(selected)
                pygame.time.delay(100)
        elif 320 > mouse[0] > 240 and 600 < mouse[1] < 680:
            if click[0] == 1:
                print("=======Advance======")
                pygame.mixer.Sound("KEY_A_SOUND.wav").play()
                selected = 2
                difficulty.update(selected)
                pygame.time.delay(100)
        pygame.display.flip()
        clock.tick(60)

    elif GAME_PAGE:
        while COMPLETE_STATE:
            print("=======end======")
            tmp.set_alpha(100)
            play_screen.blit(tmp, [0, 0])
            result_txt = main_font.render("Result", True, (0, 0, 0))
            score_txt = main_font.render("Score", True, (0, 0, 0))
            rank_txt = main_font.render("Rank", True, (0, 0, 0))

            play_screen.blit(result_txt, (450, 200))
            play_screen.blit(str(score(0)), (450, 400))

            if button_back.update():
                GAME_STATE = False
                MAIN_STATE = True
                COMPLETE_STATE = False

                pass

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.delay(200)
                        COMPLETE_STATE = False
                        GAME_READY_STATE = False

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

        tmp.set_alpha(0)
        play_screen.blit(tmp, [0, 0])

        while PAUSE:
            print("=======paused======")
            if button_back.update():
                pygame.mixer.unpause()
                song_list_list[now_item].sound.stop()
                GAME_STATE = False
                GAME_READY_STATE = False
                MAIN_STATE = True
                # Clear the NoteList When Game Finished
                for i in range(0, song_list_list[now_item].get_note_count()):
                    NoteList.pop()
                    NoteList_Drawer.pop()
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.delay(200)
                        pygame.mixer.unpause()
                        PAUSE = False
                        GAME_READY_STATE = False
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

        while GAME_READY_STATE:
            print("=======Play======")
            end_time = song_list_list[now_item].playtime

            # background
            play_screen.blit(background, [0, 0])
            pygame.draw.line(play_screen, (0, 0, 0), (0, 128),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 256),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 384),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 512),
                             (1200, 750), 2)

            play_screen.blit(main_font.render("combo", True, (255, 255, 255)), (830, 40))
            play_screen.blit(main_font.render("score", True, (255, 255, 255)), (1000, 40))
            play_screen.blit(main_font.render(str(combo(0)), True, (255, 255, 255)), (880, 70))
            play_screen.blit(main_font.render(str(score(0)), True, (255, 255, 255)), (1000, 70))
            nodes.draw(play_screen)
            tmp.set_alpha(0)
            play_screen.blit(tmp, [0, 0])
            gap = time.time() - start_time
            if gap < 2:
                title = main_font.render("Ready", True, (255, 255, 255))
                title = pygame.transform.rotate(title, math.sin(gap * 30))
            elif 2 <= gap < 4:
                title = main_font.render("Start", True, (255, 255, 255))
            else:
                for i in range(0, song_list_list[now_item].get_note_count()):
                    NoteList.append(
                        note(play_screen, 27, 128, song_list_list[now_item].get_note(), song_list_list[now_item].speed))
                    song_list_list[now_item].move_index()
                    NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))

                for i in range(0, song_list_list[now_item].get_note_count()):
                    NoteList[i].re_init()

                song_list_list[now_item].sound.play()
                Note_Count = 0
                comp = 1377 / (6 * 60)
                start_time = time.time()
                break
            play_screen.blit(title, (600, 375))

            pygame.display.flip()
            clock.tick(60)

        # When Game is Playing
        while pygame.mixer.get_busy() and not PAUSE:
            end_time = song_list_list[now_item].playtime

            if time.time() - start_time > end_time:
                pygame.mixer.quit()
                COMPLETE_STATE = True
                break
            play_screen.fill((0, 0, 0))

            # background
            play_screen.blit(background, [0, 0])
            pygame.draw.line(play_screen, (0, 0, 0), (0, 128),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 256),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 384),
                             (1200, 750), 2)
            pygame.draw.line(play_screen, (0, 0, 0), (0, 512),
                             (1200, 750), 2)

            play_screen.blit(tmp, [0, 0])

            pygame.draw.rect(play_screen, (106, 141, 246), [0, 500, 1500, 300])
            # play_screen.blit(drawer, Setting_Value.Display_Set.drawer)
            play_screen.blit(main_font.render("combo", True, (255, 255, 255)), (830, 40))
            play_screen.blit(main_font.render("score", True, (255, 255, 255)), (1000, 40))
            play_screen.blit(main_font.render(str(combo(0)), True, (255, 255, 255)), (880, 70))
            play_screen.blit(main_font.render(str(score(0)), True, (255, 255, 255)), (1000, 70))
            nodes.draw(play_screen)

            nodes.update(False, False)

            if time.time() - start_time >= song_list_list[now_item].get_sync() - comp:
                if song_list_list[now_item].move_sync_index():
                    MODE_NOTE_FALL = True
                    Note_Count += 1
                    song_list_list[now_item].move_index()

            if MODE_NOTE_FALL:
                for i in range(killed_note(0), Note_Count):
                    NoteList_Drawer[i].draw(play_screen)
                    NoteList_Drawer[i].update(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    GAME_STATE = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        # effect.note_anim1.play()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(1, True)
                        node1.update(True, False, 1)

                    if event.key == pygame.K_s:
                        # effect.note_anim2.play()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(2, True)
                        node2.update(True, False, 2)
                    if event.key == pygame.K_d:
                        # effect.note_anim3.play()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(3, True)
                        node3.update(True, False, 3)
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        PAUSE = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        # effect.note_anim1.stop()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(1, True, True)
                        node1.update(False, True, 1)
                    if event.key == pygame.K_s:
                        # effect.note_anim2.stop()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(2, True, True)
                        node2.update(False, True, 2)
                    if event.key == pygame.K_d:
                        # effect.note_anim3.stop()
                        for i in range(killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(3, True, True)
                        node3.update(False, True, 3)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)
