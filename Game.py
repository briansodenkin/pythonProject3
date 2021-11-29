import pygame
import node
import Setting_Value
import time
import map
screen = pygame.display.set_mode((1200, 750))

import MapList

main_font = pygame.font.Font("Azteca-Condensed.ttf", 35)
number_font = pygame.font.Font("Azteca-Condensed.ttf", 35)

node1 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node1_y, 40, 128, type=1, screen=screen)
node2 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node2_y, 40, 128, type=2, screen=screen)
node3 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node3_y, 40, 128, type=3, screen=screen)
node_group = pygame.sprite.RenderPlain([node1, node2, node3])
length = 0
MODE_NOTE_FALL = False
NoteList = []
NoteList_Drawer = []

Note_Count = 0
done = False
clock = pygame.time.Clock()

# Initializing the Notes
for i in range(0, MapList.MapList[0].get_note_count()):
    NoteList.append(map.note(screen, 27, 128, MapList.MapList[0].get_note(), speed=5, isLongNote=False))
    MapList.MapList[0].move_index()
    NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))

for i in range(0, MapList.MapList[0].get_note_count()):
    NoteList[i].re_init()

MapList.MapList[0].sound.play()
Note_Count = 0
MODE_NOTE_FALL = False

background = pygame.image.load("game_background.jpg").convert()

clock = pygame.time.Clock()
start_time = time.time()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(1, True)
            if event.key == pygame.K_s:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(2, True)
            if event.key == pygame.K_d:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(3, True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(1, True, True)
            if event.key == pygame.K_s:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(2, True, True)
            if event.key == pygame.K_d:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(3, True, True)

    # backround
    screen.blit(background, [0, 0])
    pygame.draw.line(screen, (0, 0, 0), (200, 128), (1200, 128), 2)
    pygame.draw.line(screen, (0, 0, 0), (200, 256), (1200, 256), 2)
    pygame.draw.line(screen, (0, 0, 0), (200, 384), (1200, 384), 2)
    length = 0.1

    screen.blit(main_font.render("Score", True, (255, 255, 255)), (600, 500))
    screen.blit(main_font.render("Combo", True, (255, 255, 255)), (400, 500))
    screen.blit(number_font.render(str(map.combo(0)), True, (255, 255, 255)), (400, 550))
    screen.blit(number_font.render(str(map.score(0)), True, (255, 255, 255)), (600, 550))
    node_group.draw(screen)
    node_group.update(0, 1)

    if True:
        if time.time() - start_time >= MapList.MapList[0].get_sync():
            if MapList.MapList[0].move_sync_index():
                MODE_NOTE_FALL = True
                Note_Count += 1
                MapList.MapList[0].move_index()
        if MODE_NOTE_FALL:
            for i in range(map.killed_note(0), Note_Count):
                NoteList_Drawer[i].draw(screen)
                NoteList_Drawer[i].update(0, False)
    pygame.display.flip()
    clock.tick(60)
