def resize_font_height(font, max_font_size, height_widget, height_max):
    height = height_widget.winfo_height()
    if height > height_max:
        while font['size'] > 1 and height > height_max:
            font['size'] -= 1
            height_widget.update_idletasks()
            height = height_widget.winfo_height()
    else:
        while font['size'] < max_font_size and height < height_max:
            font['size'] += 1
            height_widget.update_idletasks()
            height = height_widget.winfo_height()
        if font['size'] > 1 and height > height_max:
            font['size'] -= 1

def resize_font_width(text, font, frame_width, padding=0):
    font_width = 0
    for string in text.splitlines():
        font_width = max(font_width, font.measure(string))
    if font['size'] > 1 and font_width > frame_width - padding:
        font['size'] -= 1
        resize_font_width(text, font, frame_width, padding)