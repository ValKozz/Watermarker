from Painter import Painter
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from canvas import ImgCanvas, ImportImage
from buttons import Buttons
from propertyMaster import PropertyMasterPanel
from settings import *

ctk.set_appearance_mode('dark')

ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.painter = Painter()
        # Canvas
        self.image_width = 0
        self.image_height = 0
        self.canvas_height = 0
        self.canvas_width = 0

        # Images have to be defined this way, so they don't get garbage collected
        self.image_to_display = None
        self.last_saved = False
        self.init_params()
        self.init_window()

    def init_params(self):
        self.insert_text_value = DEFAULT_WATERMARK_TEXT
        self.draw_pos = (0, 0)
        self.wt_rotation = ctk.DoubleVar(self, ROTATION_DEFAULT)
        self.wt_size = ctk.IntVar(self, SIZE_DEFAULT)
        self.wt_opacity = ctk.IntVar(self, SLIDER_DEFAULT)
        self.preview_color = DEFAULT_COLOR
        self.img_rotation = ctk.DoubleVar(self, ROTATION_DEFAULT)

        self.img_rotation.trace('w', self.update_image)
        self.wt_rotation.trace('w', self.update_image)
        self.wt_size.trace('w', self.update_image)
        self.wt_opacity.trace('w', self.update_image)

    def update_image(self, *args):
        if self.check_if_img(to_display=False):
            self.painter.apply_changes(
                self.insert_text_value,
                self.draw_pos,
                self.wt_rotation.get(),
                self.wt_size.get(),
                self.wt_opacity.get(),
                self.preview_color,
                self.img_rotation.get())
            self.update_canvas()

    def init_window(self):
        self.title('Watermarker')
        self.minsize(width=1200, height=800)
        self.init_layout()

    def init_layout(self):
        inner_grid = ctk.CTkFrame(self)
        inner_grid.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Canvas
        self.import_image = ImportImage(inner_grid, self.open_image)
        self.canvas = ImgCanvas(parent=inner_grid)

        # Properties
        self.property_menu = PropertyMasterPanel(inner_grid, self.wt_size, self.wt_opacity, self.wt_rotation,
                                                 self.insert_text_value, self.img_rotation, self.update_text)

        # Buttons
        self.button_grid = Buttons(self)
        self.protocol('WM_DELETE_WINDOW', self.warn_on_close)

    def update_text(self, text):
        self.insert_text_value = text
        print(f'Call to main: {self.insert_text_value} ')

    def open_image(self, file_path=None):
        if file_path:
            # UI
            self.import_image.pack_forget()
            # Painter Image handling
            self.painter.image_path = file_path
            self.painter.load_image()
            # Get image to display on canvas
            self.image_to_display = self.painter.return_image()
            self.canvas.load_image(self, import_func=self.click_to_move)

    def resize_image(self, event=None):
        # Get ratios
        if event:
            self.canvas_height = event.height
            self.canvas_width = event.width

        image_ratio = self.painter.return_ratio()
        canvas_ratio = event.width / event.height
        # Resize
        if canvas_ratio > image_ratio:  # Canvas is wider
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * image_ratio)
        else:  # Canvas is taller
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / image_ratio)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete('all')
        self.resized_image = self.painter.resize_image(self.image_width, self.image_height)
        self.image_to_display = self.painter.return_image()
        self.canvas.create_image((self.canvas_width / 2, self.canvas_height / 2), image=self.resized_image)

    def pick_color(self):
        if self.check_if_img():
            self.preview_color = colorchooser.askcolor()
            self.button_grid.configure_preview(self)
            self.update_image()

    def click_to_move(self, event):
        self.draw_pos = (event.x / 2, event.y / 2)
        # print(f'Draw x and y: {self.draw_pos}')
        self.update_image()

    def save_image(self):
        # TODO
        if self.check_if_img():
            # VERY SLOPPY, TO-DO: Fix this mess
            io_wrapper = filedialog.asksaveasfile(filetypes=FILETYPES)
            if io_wrapper:
                path = str(io_wrapper).split(' ')[1]
                extension = path.split('.')[1].upper().strip("'")

                self.painter.save_image(extension, io_wrapper)
                self.last_saved = True

    def check_if_img(self, to_display=True):
        if not self.painter.edited_image and to_display:
            pop_up = messagebox
            pop_up.showwarning(title='File', message='No image provided.')
            return False
        return True

    def reset_image(self):
        if self.check_if_img():
            self.painter.reset_image()
            self.update_canvas()

    def warn_on_close(self):
        if self.painter.edited_image and not self.last_saved:
            response = messagebox.askyesnocancel('Exit', 'Are you sure you want to exit without saving?')

            if response:
                return self.destroy()
            elif response is None:
                return None
            elif response is False:
                self.save_image()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
