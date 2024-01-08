from PIL import Image, ImageFont, ImageDraw, ImageTk


class Painter:
    def __init__(self):
        self.image = None
        self.image_path = None
        self.color = ((255, 255, 255), '#FFFFFF')

    def draw_text(self, text, opacity, size, position):
        color_rgb = self.color[0]

        with Image.open(self.image_path).convert('RGBA') as base:
            # make a blank image for the text, initialized to transparent text color
            overlayed_image = Image.new("RGBA", base.size, (255, 255, 255, 0))

            # Get the font
            font = ImageFont.truetype(font='Pillow/Tests/FreeMono.ttf', size=size)
            # Get the context i.e. do what to what
            draw = ImageDraw.Draw(overlayed_image)
            # TO-DO: Find better way to retrieve rgb values outside the tuple
            draw.text(position, text, font=font, fill=(color_rgb[0], color_rgb[1], color_rgb[2], opacity))

            self.image = Image.alpha_composite(base, overlayed_image)
            return self.image

    def draw_image(self, path):
        pass

    def load_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path)
            return self.image
        return None

    def reset_image(self):
        self.image = Image.open(self.image_path)

    def save_image(self, extension, io_wrapper):
        if extension == 'JPEG':
            rgb_image = self.image.convert('RGB')
            rgb_image.save(io_wrapper)
        else:
            self.image.save(io_wrapper)

    def return_image(self):
        return ImageTk.PhotoImage(self.image)