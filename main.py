import random

import pygame
import eyed3
import time

# UI
# screen initialise
pygame.display.init()
pygame.mixer.init()
play_screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption("AIST2010")

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
                print("BACKKKK")
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

    def add_note(self, type, sync_time, length=None):
        self.Group_Note_Map.append(type)
        self.Group_Note_Map_SyncTime.append(sync_time)
        if length is not None:
            self.Group_LongNote_Map_Length.append(length)
        else:
            self.Group_LongNote_Map_Length.append(0)

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


song1 = Song("Cash_Cash_-_Overtime.ogg", "Overtime", "Cash Cash", 5)
song2 = Song("Zedd - Find You ft. Matthew Koma & Miriam Bryant (TAK Remix).ogg", "Find You", "Zedd", 2)
song3 = Song("Clarity_Zedd_Union_Mix_Zedd_320k_mp3.ogg", "Clarity(zedd union remix)", "Zedd", 1)
song_list_list = [song1, song2, song3]

class gensonglist(pygame.sprite.Sprite):
    List = []
    List_map = []
    List_font = []
    List_Background = []
    list_focus = 0
    list_count = 0
    start = 200
    margin = 50
    margin_background = 600
    MODE_FADE_OUT = False
    MODE_SCROLL_DOWN = False
    MODE_SCROLL_UP = False
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

    def append(self, title, background_image, artist, d, songs=None):
        self.List.append(title)
        self.List_font.append(self.main_font.render(title, True, (0, 0, 0)))
        self.List_Background.append(background_image)
        self.List_map.append(songs)
        self.list_count += 1

    def update(self, up=False, down=False, Sort_A=False, Sort_B=False, enter=False, SpeedUp=False, SpeedDown=False):
        global list_focus
        self.margin = 50
        self.screen.blit(self.background, [0, self.pos])
        selected = pygame.Surface([1600, 70])
        selected.fill((0, 0, 0))

        if up and self.list_focus > 0:
            if self.MODE_SCROLL_UP:
                return False
            self.list_focus -= 1
            print(self.list_focus)
            self.start += 60
            sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
            sound.play()
            self.MODE_SCROLL_UP = True

        if down and self.list_focus < self.list_count - 1:
            if self.MODE_SCROLL_DOWN:
                return False
            self.list_focus += 1
            print(self.list_focus)
            self.start -= 60
            sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
            sound.play()
            self.MODE_SCROLL_DOWN = True

        if enter:
            self.MODE_FADE_OUT = True
            self.cover = pygame.Surface((200, 400))
            self.start_time = time.time()
            self.cover.fill((255, 255, 255))
            pygame.mixer.Sound("KEY_A_SOUND.wav").play()

        if 1600 > self.mouse[0] > 400 and 300 > self.mouse[1] > 230:
            if self.click[0] == 1:
                pygame.time.delay(100)
                self.MODE_FADE_OUT = True
                self.cover = pygame.Surface((200, 400))
                self.start_time = time.time()
                self.cover.fill((255, 255, 255))
                pygame.mixer.Sound("KEY_A_SOUND.wav").play()

        self.margin_background = 0
        for image in self.List_Background:
            self.screen.blit(image, [0, self.pos + self.margin_background])
            self.margin_background += 750

        self.margin_background = 0
        if self.MODE_SCROLL_UP:
            self.pos += self.speed
            self.speed += 120
            self.alpha_value -= self.alpha_value_change_speed
            self.alpha_value_change_speed += 9
            if self.alpha_value > 0:
                self.alpha_value -= 1
            for image in self.List_Background:
                self.screen.blit(image, [0, self.pos + self.margin_background])
                self.margin_background += 750
            if self.pos == -750 * self.list_focus:
                self.MODE_SCROLL_UP = False
                self.speed = 0
                self.alpha_value = 180
                pygame.mixer.music.fadeout(1200)

        # When Scroll down
        if self.MODE_SCROLL_DOWN:
            self.pos -= self.speed
            self.speed += 120
            self.alpha_value -= self.alpha_value_change_speed
            self.alpha_value_change_speed += 9
            for image in self.List_Background:
                self.screen.blit(image, [0, self.pos + self.margin_background])
                self.margin_background += 750
            if self.pos == -750 * self.list_focus:
                self.MODE_SCROLL_DOWN = False
                self.speed = 0
                self.alpha_value = 180
                pygame.mixer.music.fadeout(1200)

        # BGM
        if not pygame.mixer.music.get_busy():
            pygame.time.delay(50)
            pygame.mixer.music.load(song_list_list[self.list_focus].file)
            pygame.mixer.music.play(0, song_list_list[self.list_focus].highlight + 0.01)
            pygame.mixer.music.set_volume(0.5)

        selected.set_alpha(self.alpha_value)
        self.screen.blit(selected, (400, 230))

        i = 0
        for title in self.List:
            self.List_font[i] = (self.main_font.render(title, True, (0, 0, 0)))
            i += 1
        # only focused item Set Font with WHITE color
        self.List_font[self.list_focus] = self.main_font.render(self.List[self.list_focus], True, (0, 0, 0))

        # OUTPUT PART
        for i in self.List_font:
            if i == self.List_font[self.list_focus]:
                self.screen.blit(i, [405, self.start + self.margin])
                self.margin += 60
                continue
            self.screen.blit(i, [450, self.start + self.margin])
            self.margin += 60

        SongsList_txt = self.main_font.render('Song List', True, (0, 0, 0))
        self.screen.blit(SongsList_txt, (150, 130))

        # COUNT Of Songs
        s = "(%d / %d)" % (self.list_focus + 1, self.list_count)
        self.screen.blit(self.main_font.render(s, True, (0, 0, 0)), (190, 80))

        # Back Button
        if 75 > self.mouse[0] > 25 and 25 < self.mouse[1] < 50:
            if self.click[0] == 1:
                self.MODE_FADE_OUT = False

        # Set The Speed Of Song
        if self.MODE_FADE_OUT:
            gap = (self.end_time - self.start_time)
            if gap < 1:
                self.cover.set_alpha(gap * 215)
                self.screen.blit(self.cover, [0, 0])
            else:
                self.screen.blit(self.cover, [0, 0])
                self.screen.blit(self.main_font.render("Set The Speed", True, (0, 0, 0)), (600, 345))
                self.screen.blit(self.main_font.render(str(self.SongSpeed), True, (0, 0, 0)), (630, 375))
                self.screen.blit(self.main_font.render("-", True, (0, 0, 0)), (610, 375))
                self.screen.blit(self.main_font.render("+", True, (0, 0, 0)), (650, 375))
                if 650 + 65 > self.mouse[0] > 650 and 375 < self.mouse[1] < 375 + 55:
                    if self.click[0]:
                        if self.SongSpeed < 9:
                            self.SongSpeed += 1
                        pygame.time.delay(100)
                if 610 + 65 > self.mouse[0] > 610 and 375 < self.mouse[1] < 375 + 55:
                    if self.click[0]:
                        if self.SongSpeed > 1:
                            self.SongSpeed -= 1
                        pygame.time.delay(100)


song_list = gensonglist(play_screen)
for song in song_list_list:
    song_list.append(song.song_title, pygame.image.load("image" + str(random.randrange(2, 5)) + ".jpg").convert(),
                     song.artist, song.level)


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
            self.image = pygame.image.load("block.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
        elif type == 2:
            self.image = pygame.image.load("block.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")
        elif type == 3:
            self.image = pygame.image.load("block.jpg").convert()
            self.image = pygame.transform.scale(self.image, (width, height))
            self.sound = pygame.mixer.Sound("KEY_A_SOUND.wav")

        self.rect = self.image.get_rect()
        self.rect.center = (X, Y)
        self.sound.set_volume(1.5)

    def update(self, Keypressed, KeyUp, type=0):

        if Keypressed:
            self.image = pygame.image.load("block.jpg").convert()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.sound.play()
        elif KeyUp:
            if type == 1:
                self.image = pygame.image.load("block.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif type == 2:
                self.image = pygame.image.load("block.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            elif type == 3:
                self.image = pygame.image.load("block.jpg").convert()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))


node1 = node(110, 192, 47, 128, 1, play_screen)
node2 = node(110, 320, 47, 128, 2, play_screen)
node3 = node(110, 448, 47, 128, 3, play_screen)
nodes = pygame.sprite.RenderPlain([node1, node2, node3])
# =================================== Node End =========================================================================

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

DIFFICULTY = False
selected = 1
NoteList = []
NoteList_Drawer = []
Note_Count = 0
MODE_NOTE_FALL = False
done = False
clock = pygame.time.Clock()
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            done = True

        if event.type == pygame.KEYDOWN and MAIN_FADE_OUT_STATE:
            if event.key == pygame.K_KP_ENTER:
                GAME_READY_STATE = True
                pygame.mixer.music.fadeout(1500)
                start_time = time.time()

        if event.type == pygame.KEYDOWN and SONG_PAGE == True and (MAIN_FADE_OUT_STATE == False):
            if event.key == pygame.K_UP:
                print("UP")
                song_list.update(True, False)
            if event.key == pygame.K_DOWN:
                print("DOWN")
                song_list.update(False, True)
            if event.key == pygame.K_KP_ENTER:
                song_list.update(False, False, False, False, True)
                MAIN_FADE_OUT_STATE = True
            if event.key == pygame.K_ESCAPE:
                SONG_PAGE = False
                MAIN_PAGE = True
                pygame.mixer.music.stop()
                pygame.time.delay(300)
        if event.type == pygame.MOUSEBUTTONDOWN and SONG_PAGE and MAIN_FADE_OUT_STATE == False:
            if event.button == 5:
                song_list.update(False, True)
        if event.type == pygame.MOUSEBUTTONUP and SONG_PAGE and MAIN_FADE_OUT_STATE == False:
            if event.button == 4:
                song_list.update(True, False)
        if event.type == pygame.MOUSEBUTTONUP and MAIN_FADE_OUT_STATE:
            if event.button == 4:
                song_list.update()
        if event.type == pygame.MOUSEBUTTONDOWN and MAIN_FADE_OUT_STATE:
            if event.button == 5:
                song_list.update()
    # Intro Scene
    if MAIN_PAGE:
        play_screen.fill((0, 0, 0))
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
        play_screen.fill((0, 0, 0))
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

