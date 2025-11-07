"""Paint, for drawing shapes.

Exercises

1. Add a color.
2. Complete circle.
3. Complete rectangle.
4. Complete triangle.
5. Add width parameter.

New Features:
1. Spacebar to cycle through colors
2. More colors: pink, brown, gray, orange, purple, yellow
3. + or = to increase brush width
4. - to decrease brush width
5. Real-time display of current width and color
6. D key for dashed mode
7. P key for spray effect
8. R key to draw rectangle
9. C key to clear canvas
10. Hold left mouse button to draw line
11. Larger canvas size (800x600)
"""

from turtle import *
import random
from freegames import vector


def line(start, end):
    """Draw line from start to end."""
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)


def square(start, end):
    """Draw square from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(4):
        forward(end.x - start.x)
        left(90)

    end_fill()


def circle(start, end):
    """Draw circle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()
    radius = ((end.x - start.x) ** 2 + (end.y - start.y) ** 2) ** 0.5
    circle(radius)
    end_fill()


def rectangle(start, end):
    """Draw rectangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    for count in range(2):
        forward(end.x - start.x)
        left(90)
        forward(end.y - start.y)
        left(90)

    end_fill()


def triangle(start, end):
    """Draw triangle from start to end."""
    up()
    goto(start.x, start.y)
    down()
    begin_fill()

    # Draw triangle with start as one vertex and end as another
    dx = end.x - start.x
    dy = end.y - start.y
    
    # First side: start to end
    goto(end.x, end.y)
    
    # Second side: end to third vertex
    # Calculate third vertex at 60 degrees from end
    third_x = end.x - dx / 2 - dy * (3**0.5) / 2
    third_y = end.y - dy / 2 + dx * (3**0.5) / 2
    goto(third_x, third_y)
    
    # Third side: third vertex back to start
    goto(start.x, start.y)

    end_fill()


def store(key, value):
    """Store value in state at key."""
    state[key] = value


# Initialize state
state = {
    'start': None,
    'shape': line,
    'width': 1,
    'color_index': 0,
    'dashed': False,
    'spray': False
}

# Color list with new colors
colors = ['black', 'white', 'green', 'blue', 'red', 'pink', 'brown', 'gray', 'orange', 'purple', 'yellow']

# Set initial color and pen size
color(colors[0])
pensize(state['width'])

# Setup larger canvas
setup(800, 600, 370, 0)
def draw_status():
    """Draw current status (color and width) on screen."""
    clearstamp()  # Clear previous status
    up()
    goto(0, -290)  # Position at bottom center
    color('black')
    write(f"Color: {colors[state['color_index']]} | Width: {state['width']}", align='center', font=('Arial', 12, 'normal'))
    stamp()

def cycle_color():
    """Cycle through colors when spacebar is pressed."""
    state['color_index'] = (state['color_index'] + 1) % len(colors)
    color(colors[state['color_index']])
    draw_status()

def increase_width():
    """Increase brush width."""
    state['width'] = min(state['width'] + 1, 20)
    pensize(state['width'])
    draw_status()

def decrease_width():
    """Decrease brush width."""
    state['width'] = max(state['width'] - 1, 1)
    pensize(state['width'])
    draw_status()

def toggle_dashed():
    """Toggle dashed mode."""
    state['dashed'] = not state['dashed']
    if state['dashed']:
        # Set dashed line pattern
        pencolor(colors[state['color_index']])
        up()  # Lift pen when toggling
    else:
        # Set solid line pattern
        pencolor(colors[state['color_index']])
        up()  # Lift pen when toggling

def spray(x, y):
    """Draw spray effect."""
    if state['spray']:
        for _ in range(20):
            up()
            goto(x + random.randint(-10, 10), y + random.randint(-10, 10))
            down()
            dot(state['width'], colors[state['color_index']])

def clear_canvas():
    """Clear the entire canvas."""
    clear()
    draw_status()

def start_drawing(x, y):
    """Start drawing when mouse is pressed."""
    state['start'] = vector(x, y)
    if state['shape'] == line:
        # For line, start drawing immediately
        up()
        goto(x, y)
        down()

def draw_shape(x, y):
    """Draw shape when mouse is released."""
    start = state['start']
    if start is None:
        return
    
    shape = state['shape']
    end = vector(x, y)
    
    if shape == line:
        # Line is drawn continuously while dragging
        if state['dashed']:
            # Dashed line implementation using turtle's pencolor and pensize
            # Calculate distance and number of dashes
            dx = end.x - start.x
            dy = end.y - start.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dash_length = 15
            gap_length = 10
            total_length = dash_length + gap_length
            
            if distance > 0:
                # Calculate number of full dashes
                num_dashes = int(distance / total_length)
                
                # Calculate unit vector
                unit_x = dx / distance
                unit_y = dy / distance
                
                current_pos = vector(start.x, start.y)
                
                for i in range(num_dashes):
                    # Draw dash
                    up()
                    goto(current_pos.x, current_pos.y)
                    down()
                    
                    dash_end_x = current_pos.x + unit_x * dash_length
                    dash_end_y = current_pos.y + unit_y * dash_length
                    goto(dash_end_x, dash_end_y)
                    
                    # Move to next gap
                    current_pos.x = dash_end_x + unit_x * gap_length
                    current_pos.y = dash_end_y + unit_y * gap_length
                
                # Draw remaining dash if needed
                remaining = distance - num_dashes * total_length
                if remaining > 0:
                    up()
                    goto(current_pos.x, current_pos.y)
                    down()
                    
                    dash_end_x = current_pos.x + unit_x * remaining
                    dash_end_y = current_pos.y + unit_y * remaining
                    goto(dash_end_x, dash_end_y)
        else:
            # Solid line
            goto(end.x, end.y)
        
        # Update start for continuous line drawing
        state['start'] = vector(x, y)

def end_drawing(x, y):
    """End drawing when mouse is released."""
    start = state['start']
    if start is not None:
        shape = state['shape']
        end = vector(x, y)
        
        # Draw non-line shapes on release
        if shape != line:
            shape(start, end)
    
    state['start'] = None

# Update tap function to handle continuous line drawing
def tap(x, y):
    """Handle mouse events."""
    if state['spray']:
        spray(x, y)
    else:
        start = state['start']
        if start is None:
            state['start'] = vector(x, y)
        else:
            shape = state['shape']
            end = vector(x, y)
            shape(start, end)
            state['start'] = None

# Setup event listeners
onmousedown(start_drawing)
onmousemove(draw_shape)
onmouseup(end_drawing)

listen()
onkey(undo, 'u')
onkey(cycle_color, 'space')  # Spacebar to cycle colors
onkey(increase_width, 'plus')
onkey(increase_width, 'equal')  # Both + and = keys
onkey(decrease_width, 'minus')
onkey(toggle_dashed, 'd')
onkey(toggle_dashed, 'D')
onkey(lambda: state.update({'spray': True}), 'p')
onkey(lambda: state.update({'spray': True}), 'P')
onkey(lambda: state.update({'spray': False}), 'n')  # N for normal mode
onkey(lambda: state.update({'spray': False}), 'N')
onkey(clear_canvas, 'c')
onkey(clear_canvas, 'C')
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', circle), 'o')  # O for circle (changed from c to avoid conflict with clear)
onkey(lambda: store('shape', circle), 'O')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')

# Draw initial status
draw_status()

done()
