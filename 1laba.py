import pygame
import math
pygame.init()
shir, vis = 600, 600
window = pygame.display.set_mode((shir, vis))
white = (255, 255, 255)
blue = (0, 0, 255)
center = (shir // 2, vis // 2)
radius = 200
angle = 0
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill(white)
    pygame.draw.circle(window, blue, center, radius, 2)
    x = center[0] + radius * math.cos(math.radians(angle))
    y = center[1] + radius * math.sin(math.radians(angle))
    pygame.draw.circle(window, (255, 0, 0), (int(x), int(y)), 5)
    angle += 1
    if angle >= 360:
        angle = 0
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
