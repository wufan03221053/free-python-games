"""Paint, for drawing shapes using pygame.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.
"""

import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)

# Color list with new colors
colors = [BLACK, WHITE, GREEN, BLUE, RED, PINK, BROWN, GRAY]
color_names = ['black', 'white', 'green', 'blue', 'red', 'pink', 'brown', 'gray']
color_index = 0
pen_width = 1

# State variables
state = {
    'start_pos': None,
    'shape': 'line',
    'dashed': False,
    'spray': False
}

# Font for status display
font = pygame.font.Font(None, 24)


def draw_line(start, end, color, width, dashed=False):
    """Draw line from start to end."""
    if dashed:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        segments = int(distance / 10)
        for i in range(segments):
            segment_start = (start[0] + dx * i / segments, start[1] + dy * i / segments)
            segment_end = (start[0] + dx * (i + 0.5) / segments, start[1] + dy * (i + 0.5) / segments)
            pygame.draw.line(screen, color, segment_start, segment_end, width)
    else:
        pygame.draw.line(screen, color, start, end, width)


def draw_square(start, end, color, width):
    """Draw square from start to end."""
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    size = abs(end[0] - start[0])
    pygame.draw.rect(screen, color, (x, y, size, size), width)


def draw_circle(start, end, color, width):
    """Draw circle from start to end."""
    x = (start[0] + end[0]) // 2
    y = (start[1] + end[1]) // 2
    radius = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5 // 2
    pygame.draw.circle(screen, color, (x, y), radius, width)


def draw_rectangle(start, end, color, width):
    """Draw rectangle from start to end."""
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    width_rect = abs(end[0] - start[0])
    height_rect = abs(end[1] - start[1])
    pygame.draw.rect(screen, color, (x, y, width_rect, height_rect), width)


def draw_triangle(start, end, color, width):
    """Draw triangle from start to end."""
    points = [start, (end[0], start[1]), end]
    pygame.draw.polygon(screen, color, points, width)


def draw_spray(pos, color, width):
    """Draw spray effect."""
    for _ in range(20):
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        spray_pos = (pos[0] + offset_x, pos[1] + offset_y)
        pygame.draw.circle(screen, color, spray_pos, width // 2)


def update_status():
    """Update status display."""
    # Clear previous status text with a white rectangle
    pygame.draw.rect(screen, WHITE, (0, 0, 500, 30))
    
    status_text = f"Color: {color_names[color_index]} | Width: {pen_width} | Shape: {state['shape']} | Mode: {'Dashed' if state['dashed'] else 'Solid'} | Spray: {'On' if state['spray'] else 'Off'}"
    text_surface = font.render(status_text, True, BLACK)
    screen.blit(text_surface, (10, 10))


def show_help():
    """Show help instructions."""
    help_text = [
        "Paint Controls:",
        "- Space: Change color",
        "- +/=: Increase pen width",
        "- -: Decrease pen width",
        "- D: Toggle dashed mode",
        "- P: Toggle spray effect",
        "- L: Line tool",
        "- S: Square tool",
        "- C: Circle tool",
        "- R: Rectangle tool",
        "- T: Triangle tool",
        "- C: Clear canvas",
        "- H: Show help",
        "- U: Undo",
        "Hold left mouse button to draw"
    ]
    
    screen.fill(WHITE)
    y_offset = 50
    for line in help_text:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 30
    pygame.display.flip()


def main():
    """Main game loop."""
    global color_index, pen_width
    
    # Fill background
    screen.fill(WHITE)
    update_status()
    pygame.display.flip()
    
    # History for undo
    history = [screen.copy()]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    color_index = (color_index + 1) % len(colors)
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    pen_width = min(pen_width + 1, 20)
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_MINUS:
                    pen_width = max(pen_width - 1, 1)
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_d or event.key == pygame.K_D:
                    state['dashed'] = not state['dashed']
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_p or event.key == pygame.K_P:
                    state['spray'] = not state['spray']
                    state['shape'] = 'spray' if state['spray'] else 'line'
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_l or event.key == pygame.K_L:
                    state['shape'] = 'line'
                    state['spray'] = False
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_s or event.key == pygame.K_S:
                    state['shape'] = 'square'
                    state['spray'] = False
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_c or event.key == pygame.K_C:
                    state['shape'] = 'circle'
                    state['spray'] = False
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_r or event.key == pygame.K_R:
                    state['shape'] = 'rectangle'
                    state['spray'] = False
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_t or event.key == pygame.K_T:
                    state['shape'] = 'triangle'
                    state['spray'] = False
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_BACKQUOTE:  # Use backtick for clear canvas
                    history.append(screen.copy())
                    screen.fill(WHITE)
                    update_status()
                    pygame.display.flip()
                elif event.key == pygame.K_h or event.key == pygame.K_H:
                    show_help()
                elif event.key == pygame.K_u or event.key == pygame.K_U:
                    # Undo last action
                    if len(history) > 1:
                        history.pop()
                        screen.blit(history[-1], (0, 0))
                        update_status()
                        pygame.display.flip()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    state['start_pos'] = pygame.mouse.get_pos()
            
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button is held down
                    current_pos = pygame.mouse.get_pos()
                    if state['start_pos']:
                        if state['shape'] == 'line':
                            draw_line(state['start_pos'], current_pos, colors[color_index], pen_width, state['dashed'])
                            state['start_pos'] = current_pos
                        elif state['shape'] == 'spray':
                            draw_spray(current_pos, colors[color_index], pen_width)
                    pygame.display.flip()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    end_pos = pygame.mouse.get_pos()
                    if state['shape'] == 'square':
                        draw_square(state['start_pos'], end_pos, colors[color_index], pen_width)
                    elif state['shape'] == 'circle':
                        draw_circle(state['start_pos'], end_pos, colors[color_index], pen_width)
                    elif state['shape'] == 'rectangle':
                        draw_rectangle(state['start_pos'], end_pos, colors[color_index], pen_width)
                    elif state['shape'] == 'triangle':
                        draw_triangle(state['start_pos'], end_pos, colors[color_index], pen_width)
                    state['start_pos'] = None
                    # Save to history
                    history.append(screen.copy())
                    pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()