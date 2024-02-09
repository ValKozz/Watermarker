from Painter import Painter
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from canvas import ImgCanvas, ImportImage
from buttons import Buttons
# from property_panel import ImgProperties, ImgPropFrame
from propertyMaster import PropertyMasterPanel
from settings import *

ctk.set_appearance_mode('dark')

ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.painter = Painter()

        # Images have to be defined this way, so they don't get garbage collected
        self.image_to_display = None
        self.last_saved = False
        self.init_params()
        self.init_window()

    def init_params(self):
        self.insert_text_value = DEFAULT_WATERMARK_TEXT
        self.draw_pos = (0, 0)
        self.wt_rotation = ctk.DoubleVar(self, ROTATION_DEFAULT)
        self.wt_size = ctk.IntVar(self, SLIDER_DEFAULT)
        self.wt_opacity = ctk.IntVar(self, SLIDER_DEFAULT)
        self.preview_color = ctk.StringVar(self, DEFAULT_COLOR)

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
                                                 self.insert_text_value)

        # Buttons
        self.button_grid = Buttons(self)
        self.protocol('WM_DELETE_WINDOW', self.warn_on_close)

    def open_image(self, file_path=None):
        if file_path:
            self.import_image.pack_forget()
            self.painter.image_path = file_path
            self.painter.load_image()
            self.image_to_display = self.painter.return_image()
            self.canvas.load_image(self)

    def update_canvas(self):
        self.canvas.delete('all')
        self.last_saved = False
        self.image_to_display = self.painter.return_image()
        self.canvas.load_image(self)

    def resize_image(self, event):
        # Get ratios
        image_ratio = self.painter.return_ratio()
        canvas_ratio = event.width / event.height
        # Resize
        if canvas_ratio > image_ratio:  # Canvas is wider
            image_height = int(event.height)
            image_width = int(image_height * image_ratio)
        else:  # Canvas is taller
            image_width = int(event.width)
            image_height = int(image_width / image_ratio)

        self.canvas.delete('all')
        self.resized_image = self.painter.resize_image(image_width, image_height)
        self.image_to_display = self.painter.return_image()
        self.canvas.create_image((event.width / 2, event.height / 2), image=self.resized_image)

    def paint_image(self):
        if self.check_if_img():
            if self.top_level:
                pass
                # self.draw_value_buffer = self.top_level.return_values()

            print(self.draw_value_buffer)
            self.painter.draw_text(
                text=self.draw_value_buffer['text'],
                opacity=self.draw_value_buffer['opacity'],
                size=self.draw_value_buffer['size'],
                position=self.draw_pos)

            self.update_canvas()

    def pick_color(self):
        if self.check_if_img():
            self.painter.color = colorchooser.askcolor()
            self.button_grid.configure_preview(self)
            self.update_canvas()
            # TO-DO: Make this more efficient and less clunky

    def click_to_move(self, event):
        if self.check_if_img() and self.draw_value_buffer:
            to_center = self.draw_value_buffer['size'] / 2
            self.draw_pos = (event.x - to_center, event.y - to_center)
            print(self.draw_pos)
            self.paint_image()

    def save_image(self):
        if self.check_if_img():
            # VERY SLOPPY, TO-DO: Fix this mess
            io_wrapper = filedialog.asksaveasfile(filetypes=FILETYPES)
            if io_wrapper:
                path = str(io_wrapper).split(' ')[1]
                extension = path.split('.')[1].upper().strip("'")

                self.painter.save_image(extension, io_wrapper)
                self.last_saved = True

    def check_if_img(self):
        if not self.painter.image:
            pop_up = messagebox
            pop_up.showwarning(title='File', message='No image provided.')
            return False
        return True

    def refresh_on_event(self, event):
        if self.check_if_img():
            self.paint_image()

    def reset_image(self):
        if self.check_if_img():
            self.painter.reset_image()
            self.update_canvas()

    def warn_on_close(self):
        if self.painter.image and not self.last_saved:
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
