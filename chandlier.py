import pygame
import math
import random
import sys

# --- Setup Full Screen ---
pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
# The pygame.FULLSCREEN flag makes it take up the whole monitor
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Luxury Chandelier")
clock = pygame.time.Clock()

# Colors
BG_COLOR = (10, 16, 30)        # Deep Navy Blue
CEILING_COLOR = (45, 35, 25)   # Dark Bronze/Wood for the top
STRING_COLOR = (160, 180, 210) # Silvery-blue strings

# Physics Settings
GRAVITY = 0.4
FRICTION = 0.97        
MOUSE_RADIUS = 40      
SEGMENT_LENGTH = 12    

# We scale the string length to the height of your screen
BASE_SEGMENTS = int(HEIGHT / 30) 

class Point:
    def __init__(self, x, y, pinned=False):
        self.x = x
        self.y = y
        self.old_x = x 
        self.old_y = y
        self.pinned = pinned 

    def update(self, mouse_pos):
        if self.pinned:
            return

        vx = (self.x - self.old_x) * FRICTION
        vy = (self.y - self.old_y) * FRICTION
        
        self.old_x = self.x
        self.old_y = self.y
        
        self.x += vx
        self.y += vy + GRAVITY

        # Mouse Interaction
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        dist = math.hypot(dx, dy)

        if dist > 0 and dist < MOUSE_RADIUS:
            force = (MOUSE_RADIUS - dist) / MOUSE_RADIUS
            push_dir_x = -dx / dist
            push_dir_y = -dy / dist
            
            self.x += push_dir_x * force * 15
            self.y += push_dir_y * force * 15

class String:
    def __init__(self, x, extra_length):
        self.points = []
        y = 30 # Start just below the ceiling bar
        num_segments = BASE_SEGMENTS + extra_length 
        
        for i in range(num_segments):
            p = Point(x, y, pinned=(i == 0))
            self.points.append(p)
            y += SEGMENT_LENGTH

    def update(self, mouse_pos):
        for p in self.points:
            p.update(mouse_pos)
            
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist = math.hypot(dx, dy)
            
            if dist > 0:
                difference = SEGMENT_LENGTH - dist
                percent = difference / dist / 2
                offset_x = dx * percent
                offset_y = dy * percent
                
                if not p1.pinned:
                    p1.x -= offset_x
                    p1.y -= offset_y
                if not p2.pinned:
                    p2.x += offset_x
                    p2.y += offset_y

    def draw(self, surface):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            pygame.draw.aaline(surface, STRING_COLOR, (p1.x, p1.y), (p2.x, p2.y))
            
        end_p = self.points[-1]
        ex, ey = int(end_p.x), int(end_p.y)
        
        # Glow effect
        glow_surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 240, 150, 30), (12, 12), 12) 
        pygame.draw.circle(glow_surf, (255, 245, 180, 90), (12, 12), 7)  
        pygame.draw.circle(glow_surf, (255, 255, 255, 255), (12, 12), 3) 
        
        surface.blit(glow_surf, (ex - 12, ey - 12))

# --- Create the Chandelier ---
strings = []
# Increased the number of strings so a wider screen doesn't look empty
for i in range(120): 
    start_x = random.randint(30, WIDTH - 30)
    extra_len = random.randint(-10, 15) 
    strings.append(String(start_x, extra_len))

# --- Main Game Loop ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # NEW: Press ESC to quit full screen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    for s in strings:
        s.update(mouse_pos)

    screen.fill(BG_COLOR) 
    
    # Draw the ceiling bar
    pygame.draw.rect(screen, CEILING_COLOR, (0, 0, WIDTH, 30))
    
    for s in strings:
        s.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()