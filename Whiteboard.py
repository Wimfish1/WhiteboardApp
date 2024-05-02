import pygame
import sys
import ctypes

# Get screen dimensions
user32 = ctypes.windll.user32
SCREEN_WIDTH, SCREEN_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 100  # Subtract 100 pixels for the taskbar

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Drawing App")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define button dimensions and positions
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
BUTTON_GAP = 10
MENU_Y = 10

# Set up drawing variables
drawing = False
last_pos = None
color = BLACK
line_thickness = 2
shape = "line"
shape_size = 0

# Function to draw buttons
def draw_button(text, x, y):
    pygame.draw.rect(screen, WHITE, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2))
    screen.blit(text_surface, text_rect)

# Function to draw the menu bar
def draw_menu_bar():
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, MENU_Y + BUTTON_HEIGHT + BUTTON_GAP))
    draw_button("Clear", BUTTON_GAP, MENU_Y)
    draw_button("Black", BUTTON_GAP * 2 + BUTTON_WIDTH, MENU_Y)
    draw_button("Red", BUTTON_GAP * 3 + BUTTON_WIDTH * 2, MENU_Y)
    draw_button("Green", BUTTON_GAP * 4 + BUTTON_WIDTH * 3, MENU_Y)
    draw_button("Blue", BUTTON_GAP * 5 + BUTTON_WIDTH * 4, MENU_Y)
    draw_button("White", BUTTON_GAP * 6 + BUTTON_WIDTH * 5, MENU_Y)
    draw_button("+", SCREEN_WIDTH - BUTTON_GAP - BUTTON_WIDTH, MENU_Y)
    draw_button("-", SCREEN_WIDTH - BUTTON_GAP * 2 - BUTTON_WIDTH * 2, MENU_Y)
    draw_button("Eraser", SCREEN_WIDTH - BUTTON_GAP * 3 - BUTTON_WIDTH * 3, MENU_Y)
    draw_button("Fill", SCREEN_WIDTH - BUTTON_GAP * 4 - BUTTON_WIDTH * 4, MENU_Y)
    draw_button("Circle", SCREEN_WIDTH - BUTTON_GAP * 5 - BUTTON_WIDTH * 5, MENU_Y)
    draw_button("Square", SCREEN_WIDTH - BUTTON_GAP * 6 - BUTTON_WIDTH * 6, MENU_Y)
    draw_button("Line", SCREEN_WIDTH - BUTTON_GAP * 7 - BUTTON_WIDTH * 7, MENU_Y)
    draw_button("Pen", SCREEN_WIDTH - BUTTON_GAP * 8 - BUTTON_WIDTH * 8, MENU_Y)

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if 0 <= event.pos[1] <= MENU_Y + BUTTON_HEIGHT + BUTTON_GAP:
                    if BUTTON_GAP <= event.pos[0] <= BUTTON_GAP + BUTTON_WIDTH:
                        screen.fill(WHITE)
                    elif BUTTON_GAP * 2 + BUTTON_WIDTH <= event.pos[0] <= BUTTON_GAP * 2 + BUTTON_WIDTH * 2:
                        color = BLACK
                    elif BUTTON_GAP * 3 + BUTTON_WIDTH * 2 <= event.pos[0] <= BUTTON_GAP * 3 + BUTTON_WIDTH * 3:
                        color = RED
                    elif BUTTON_GAP * 4 + BUTTON_WIDTH * 3 <= event.pos[0] <= BUTTON_GAP * 4 + BUTTON_WIDTH * 4:
                        color = GREEN
                    elif BUTTON_GAP * 5 + BUTTON_WIDTH * 4 <= event.pos[0] <= BUTTON_GAP * 5 + BUTTON_WIDTH * 5:
                        color = BLUE
                    elif BUTTON_GAP * 6 + BUTTON_WIDTH * 5 <= event.pos[0] <= BUTTON_GAP * 6 + BUTTON_WIDTH * 6:
                        color = WHITE
                    elif SCREEN_WIDTH - BUTTON_GAP - BUTTON_WIDTH <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP:
                        line_thickness += 1
                    elif SCREEN_WIDTH - BUTTON_GAP * 2 - BUTTON_WIDTH * 2 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 2:
                        line_thickness = max(1, line_thickness - 1)
                    elif SCREEN_WIDTH - BUTTON_GAP * 3 - BUTTON_WIDTH * 3 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 3:
                        color = WHITE  # Eraser
                        shape = "eraser"
                    elif SCREEN_WIDTH - BUTTON_GAP * 4 - BUTTON_WIDTH * 4 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 4:
                        color = WHITE  # Fill
                        shape = "fill"
                    elif SCREEN_WIDTH - BUTTON_GAP * 5 - BUTTON_WIDTH * 5 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 5:
                        color = WHITE  # Circle
                        shape = "circle"
                    elif SCREEN_WIDTH - BUTTON_GAP * 6 - BUTTON_WIDTH * 6 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 6:
                        color = WHITE  # Square
                        shape = "square"
                    elif SCREEN_WIDTH - BUTTON_GAP * 7 - BUTTON_WIDTH * 7 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 7:
                        color = WHITE  # Line
                        shape = "line"
                    elif SCREEN_WIDTH - BUTTON_GAP * 8 - BUTTON_WIDTH * 8 <= event.pos[0] <= SCREEN_WIDTH - BUTTON_GAP * 8:
                        color = BLACK  # Pen
                        shape = "pen"
                else:
                    drawing = True
                    last_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if shape == "pen":
                    pygame.draw.line(screen, color, last_pos, event.pos, line_thickness)
                    last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if shape == "square":
                    width = abs(event.pos[0] - last_pos[0])
                    height = abs(event.pos[1] - last_pos[1])
                    size = max(width, height)
                    pygame.draw.rect(screen, color, (min(event.pos[0], last_pos[0]), min(event.pos[1], last_pos[1]), size, size), line_thickness)
                elif shape == "circle":
                    radius = max(abs(event.pos[0] - last_pos[0]), abs(event.pos[1] - last_pos[1]))
                    pygame.draw.circle(screen, color, last_pos, radius, line_thickness)
                elif shape == "line":
                    pygame.draw.line(screen, color, last_pos, event.pos, line_thickness)
                elif shape == "eraser":
                    pygame.draw.line(screen, WHITE, last_pos, event.pos, line_thickness)
                elif shape == "fill":
                    screen.fill(color)
                drawing = False
    # Draw menu bar
    draw_menu_bar()
    # Update the display
    pygame.display.flip()
