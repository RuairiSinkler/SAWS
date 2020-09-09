def resize_font(text, font, frame_width):
        font_width = 0
        for string in text.splitlines():
            font_width = max(font_width, font.measure(string))
        if font_width > frame_width - 100:
            font['size'] -= 1
            resize_font(text, font, frame_width)