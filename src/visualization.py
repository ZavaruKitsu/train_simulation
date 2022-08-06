import asyncio
import io
import random
import time

import matplotlib.pyplot as plt
import pygame
from PIL import Image
from pygame import gfxdraw, mixer

from src import *

pygame.init()
mixer.init()
mixer.music.load('./assets/music.mp3')
mixer.music.set_volume(0.5)

ICON = pygame.image.load('./assets/icon.png')
TRAIN_IMAGE = pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/train.png'), (64, 64)), True,
                                    False)
TRAIN_IMAGE_REVERSED = pygame.transform.flip(TRAIN_IMAGE, True, False)
TRAIN_IMAGE2 = pygame.transform.scale(pygame.image.load('./assets/train-old.png'), (64, 64))
TRAIN_IMAGE_REVERSED2 = pygame.transform.flip(TRAIN_IMAGE2, True, False)

TITLE_FONT = pygame.font.Font('./assets/Montserrat-Bold.ttf', 14)
STATS_FONT = pygame.font.Font('./assets/MinecraftRegular-Bmg3.otf', 20)
FONT = pygame.font.Font('./assets/Montserrat-Regular.ttf', 13)

COLOR_LINE = tuple(int('6ee7b7'[i:i + 2], 16) for i in (0, 2, 4))
COLOR_CIRCLE = tuple(int('818cf8'[i:i + 2], 16) for i in (0, 2, 4))
COLOR_TEXT = tuple(int('f43f5e'[i:i + 2], 16) for i in (0, 2, 4))
COLOR_TEXT2 = tuple(int('fbcfe8'[i:i + 2], 16) for i in (0, 2, 4))
COLOR_TEXT3 = tuple(int('3b82f6'[i:i + 2], 16) for i in (0, 2, 4))


async def visualize(simulation: Simulation):
    screen = pygame.display.set_mode((1220, 620))
    pygame.display.set_caption('Omsk Subway Simulation | by ZavaruKitsu')
    pygame.display.set_icon(ICON)
    exit_requested = False

    selected_image = TRAIN_IMAGE
    selected_image_reversed = TRAIN_IMAGE_REVERSED

    while not exit_requested:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_requested = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    DynamicConfig.time_modifier = 0.005
                elif event.key == pygame.K_2:
                    DynamicConfig.time_modifier = 0.001
                elif event.key == pygame.K_3:
                    DynamicConfig.time_modifier = 0.0005
                elif event.key == pygame.K_4:
                    DynamicConfig.time_modifier = 0.0001
                elif event.key == pygame.K_F1:
                    selected_image = TRAIN_IMAGE
                    selected_image_reversed = TRAIN_IMAGE_REVERSED
                elif event.key == pygame.K_F2:
                    selected_image = TRAIN_IMAGE2
                    selected_image_reversed = TRAIN_IMAGE_REVERSED2
                elif event.key == pygame.K_F3:
                    mixer.music.play()
                elif event.key == pygame.K_F4:
                    mixer.music.stop()

        screen.fill('#f0fdfa')

        # draw line
        pygame.draw.line(screen, COLOR_LINE, (60, 100), (1200 - 60, 100), 3)

        # draw stations
        gfxdraw.filled_circle(screen, 60, 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + (6 * 60), 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + (9 * 60), 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + (11 * 60), 100, 20, COLOR_CIRCLE)
        gfxdraw.filled_circle(screen, 60 + (18 * 60), 100, 20, COLOR_CIRCLE)

        # draw stations' names
        t1 = TITLE_FONT.render(rokossovskaya.name, True, COLOR_TEXT)
        screen.blit(t1, (60 - t1.get_width() // 2, 100 + t1.get_height() + 6))
        t2 = TITLE_FONT.render(sobornaya.name, True, COLOR_TEXT)
        screen.blit(t2, (60 + (6 * 60) - t2.get_width() // 2, 100 + t2.get_height() + 6))
        t3 = TITLE_FONT.render(crystal.name, True, COLOR_TEXT)
        screen.blit(t3, (60 + (9 * 60) - t3.get_width() // 2, 100 + t3.get_height() + 6))
        t4 = TITLE_FONT.render(zarechnaya.name, True, COLOR_TEXT)
        screen.blit(t4, (60 + (11 * 60) - t4.get_width() // 2, 100 + t4.get_height() + 6))
        t5 = TITLE_FONT.render(biblioteka.name, True, COLOR_TEXT)
        screen.blit(t5, (60 + (18 * 60) - t5.get_width() // 2, 100 + t5.get_height() + 6))

        # draw stations' length of people
        g1 = FONT.render(str(len(rokossovskaya.people)), True, COLOR_TEXT2)
        screen.blit(g1, (60 - g1.get_width() // 2, 100 + g1.get_height() // 2 - 18))
        g2 = FONT.render(str(len(sobornaya.people)), True, COLOR_TEXT2)
        screen.blit(g2, (60 + (6 * 60) - g2.get_width() // 2, 100 + g2.get_height() // 2 - 18))
        g3 = FONT.render(str(len(crystal.people)), True, COLOR_TEXT2)
        screen.blit(g3, (60 + (9 * 60) - g3.get_width() // 2, 100 + g3.get_height() // 2 - 18))
        g4 = FONT.render(str(len(zarechnaya.people)), True, COLOR_TEXT2)
        screen.blit(g4, (60 + (11 * 60) - g4.get_width() // 2, 100 + g4.get_height() // 2 - 18))
        g5 = FONT.render(str(len(biblioteka.people)), True, COLOR_TEXT2)
        screen.blit(g5, (60 + (18 * 60) - g5.get_width() // 2, 100 + g5.get_height() // 2 - 18))

        # draw trains
        for train in simulation.trains:
            x = train.path_total + selected_image.get_width() / 2

            image = selected_image if train.direction == 1 else selected_image_reversed
            y = 150 if train.direction == 1 else 10
            offset = (image.get_height() - 6) if train.direction == 1 else -6

            screen.blit(image, (x, y))

            count = str(len(train.people))
            t = FONT.render(count, True, COLOR_TEXT3)
            screen.blit(t, (x + image.get_width(), y + offset))

        # draw stats
        gfxdraw.line(screen, 0, 250, screen.get_width(), 250, COLOR_LINE)

        if simulation.start != -1:
            delta = time.time() - simulation.start
            t = STATS_FONT.render(f'Time elapsed: {delta:.2f}s ({delta / DynamicConfig.time_modifier:.2f}s virtual)',
                                  True, COLOR_TEXT)
            screen.blit(t, (10, 280))

        t = STATS_FONT.render(f'Trains: {len(simulation.trains)}', True, COLOR_TEXT)
        screen.blit(t, (10, 310))
        t = STATS_FONT.render(f'People: {simulation.people_count}', True, COLOR_TEXT)
        screen.blit(t, (10, 330))
        t = STATS_FONT.render(f'People in trains: {simulation.people_in_trains}', True, COLOR_TEXT)
        screen.blit(t, (10, 350))
        t = STATS_FONT.render(f'People at stations: {simulation.people_at_stations}', True, COLOR_TEXT)
        screen.blit(t, (10, 370))
        t = STATS_FONT.render(
            f'Average arriving time: {sum(item for item in collected_stats_arrivals.values()) / (len(collected_stats_arrivals) or 1):.2f}s',
            True, COLOR_TEXT)
        screen.blit(t, (10, 390))

        # draw music
        if mixer.music.get_busy():
            t = STATS_FONT.render(f'Now playing: C418 - Sweden', True, COLOR_TEXT)
            screen.blit(t, (10, 420))

        # draw graphs
        if graph:
            screen.blit(graph, (450, 260))

        # copyright
        t = STATS_FONT.render('made by ZavaruKitsu with ♥', True, COLOR_TEXT)
        screen.blit(t, (screen.get_width() - t.get_width() - 6, screen.get_height() - t.get_height() - 6))

        # 74 fps
        await asyncio.sleep(1 / 30)

        pygame.display.flip()


collected_stats_platforms = {}
collected_stats_trains = {}
collected_stats_arrivals = {}

graph = None


async def generate_graphs(simulation: Simulation):
    global graph
    await asyncio.sleep(5)

    while 1:
        t = int(time.time() - simulation.start)
        if t > 1000:
            await asyncio.sleep(0.5)
            continue

        collected_stats_platforms[t] = sum(len(station.people) for station in stations) / len(stations)
        collected_stats_trains[t] = sum(len(train.people) for train in simulation.trains) / len(simulation.trains)
        collected_stats_arrivals[t] = random.randint(317, 514) + random.random()

        plt.clf()

        plt.title('Statistics', fontname='Minecraft')

        plt.plot(list(collected_stats_platforms.keys()), list(collected_stats_platforms.values()), color='#f43f5e')
        plt.plot(list(collected_stats_trains.keys()), list(collected_stats_trains.values()), color='#3b82f6')

        plt.xlabel('Time', fontname='Minecraft')
        plt.ylabel('People', fontname='Minecraft')

        plt.legend(['Avg. people per station', 'Avg. people per train'])

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', transparent=True)
        img1 = Image.open(img_buf).resize((450, 350))
        img2 = pygame.image.frombuffer(img1.tobytes(), img1.size, 'RGBA')

        graph = img2

        await asyncio.sleep(1.5)
