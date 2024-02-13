from PIL import Image, ImageFont, ImageDraw, ImageTk


class Painter:
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.edited_image = None

        self.image_path = None
        self.color = ((255, 255, 255), '#FFFFFF')
        self.history = []
        self.resized_image = None

    def apply_changes(self, text, draw_pos, wt_rotation, wt_size, wt_opacity, color, img_rotation):
        # TODO: Set Color, Draw text
        # Edit image first
        self.edited_image = self.original_image
        self.edited_image = self.edited_image.rotate(img_rotation)

        if text:
            self.draw_text(text, wt_opacity, wt_size, draw_pos)

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

            self.edited_image = Image.alpha_composite(base, overlayed_image)
            # self.resize_image(self.edited_image)
            return self.resized_image

    def load_image(self):
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.edited_image = self.original_image

    def return_ratio(self):
        ratio = self.edited_image.size[0] / self.edited_image.size[1]
        return ratio

    def reset_image(self):
        self.edited_image = self.original_image

    def save_image(self, extension, io_wrapper):
        if extension == 'JPEG':
            rgb_image = self.edited_image.convert('RGB')
            rgb_image.save(io_wrapper)
        else:
            self.edited_image.save(io_wrapper)

    def return_image(self):
        return ImageTk.PhotoImage(self.edited_image)

    def resize_image(self, width, height):
        self.resized_image = self.edited_image.resize((width, height))
        return ImageTk.PhotoImage(self.resized_image)
