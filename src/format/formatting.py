# Function to format text color
def format_text_color(text, color):
    return f"[color={color}]{text}[/color]"

# Function to format text size
def format_text_size(text, size):
    return f"[size={size}]{text}[/size]"

# Function to format text with color, size, and font
def format_text(text, color=None, size=None, font_name=None):
    formatted_text = text
    if color:
        formatted_text = format_text_color(formatted_text, color)
    if size:
        formatted_text = format_text_size(formatted_text, size)
    if font_name:
        formatted_text = f"[font={font_name}]{formatted_text}[/font]"
    return formatted_text

# Variables for text colors
BLACK = '#000000'
RED = '#FF0000'
GREEN = '#90EE90'
BLUE = '#ADD8E6'
WHITE = '#FFFFFF'

# Variables for text sizes
SMALL_SIZE = '14sp'
MEDIUM_SIZE = '18sp'
LARGE_SIZE = '30sp'

def format_button(button, text, size=(200, 50), background_color=(0.6, 0.8, 1, 1)):
    button.text = text
    button.size_hint = (None, None)
    button.size = size
    button.background_color = background_color
    return button
