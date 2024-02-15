from PIL import Image, ImageFont, ImageDraw, ImageTk


class Painter:
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.edited_image = None

        self.image_path = None
        self.history = []
        self.resized_image = None

    def apply_changes(self, text, draw_pos, wt_rotation, wt_size, wt_opacity, color, img_rotation, flip_options):
        # Edit image first
        self.edited_image = self.original_image
        self.apply_flip(flip_options)
        self.edited_image = self.edited_image.rotate(img_rotation)

        if text and wt_size > 0:
            self.draw_text(text, wt_opacity, wt_size, wt_rotation, draw_pos, color)

    def apply_flip(self, flip_options):
        to_apply = None
        for option in flip_options:
            if flip_options[option]:
                to_apply = option

        condition = to_apply.split('_')[1]

        if condition == 'M':
            self.edited_image = self.edited_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        else:
            self.edited_image = self.edited_image.rotate(int(condition))

    def draw_text(self, text, opacity, size, rotation, position, color):
        # TODO: Change method to paste
        color_rgb = color[0]
        # Have to convert so alpha composite works
        self.edited_image = self.edited_image.convert('RGBA')

        overlay_image = Image.new(self.edited_image.mode, self.edited_image.size, (255, 255, 255, 0))

        # Get the font
        font = ImageFont.truetype(font='Pillow/Tests/FreeMono.ttf', size=size)
        # Center Text based on the size

        # Magic to center the text on clicked coordinates.
        position = (position[0] - round(font.getlength(text) / 2), position[1] - round(font.getmetrics()[1]))

        # print(f'Position: {position}')
        # print(f'Font geom: {font.getmetrics()}')

        draw = ImageDraw.Draw(overlay_image)
        draw.text(position, text, font=font, fill=(color_rgb[0], color_rgb[1], color_rgb[2], opacity), align='center')
        self.edited_image = Image.alpha_composite(self.edited_image, overlay_image.rotate(rotation))

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
