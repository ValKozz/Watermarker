import PIL
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, END
from PIL import Image, ImageTk, ImageFont, ImageDraw
import numpy as np

ctk.set_appearance_mode('dark')

ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Watermarker'
        self.minsize(width=400, height=300)
        self.painter = Painter()
        self.image_to_display = None
        self.raw_image = None
        self.draw_pos = (0, 0)

        # Buttons
        def select_file():
            filetypes = (('JPEG files', '*.jpeg *.jpg'),
                         ('PNG files', '*.png'),
                         ('All files', '*.*'))

            path = filedialog.askopenfilename(filetypes=filetypes)
            if path:
                self.painter.image_path = path
                update_canvas(self.painter.load_image())

        def update_canvas(raw_image):
            self.raw_image = raw_image
            self.image_to_display = ImageTk.PhotoImage(raw_image)
            new_width = raw_image.size[0]
            new_height = raw_image.size[1]

            self.image_canvas.configure(width=new_width, height=new_height)
            self.image_canvas.create_image((0, 0), image=self.image_to_display, anchor='nw')

        def draw_text():
            opacity = int(self.opacity_slider.get())
            size = int(self.size_slider.get())
            text_to_paint = self.text_box.get(0.0, END)
            raw_image = self.painter.draw_text(text=text_to_paint, opacity=opacity, size=size, position=self.draw_pos)
            update_canvas(raw_image)

        def click_to_move(event):
            self.draw_pos = (event.x, event.y)
            draw_text()

        def save_image():
            file_types = (('JPEG files', '*.jpeg *.jpg'),
                         ('PNG files', '*.png'),
                         ('All files', '*.*'))

            # VERY SLOPPY, TO-DO: Fix this mess
            if self.image_to_display:

                io_wrapper = filedialog.asksaveasfile(filetypes=file_types)

                path = str(io_wrapper).split(' ')[1]
                extension = path.split('.')[1].upper().strip("'")
                if extension == 'JPEG':
                    rgb_image = self.raw_image.convert('RGB')
                    rgb_image.save(io_wrapper)
                else:
                    self.raw_image.save(io_wrapper)

            else:
                return messagebox.showwarning(title='File', message='No image provided.')




        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(column=0, row=1)

        self.select_file_btn = ctk.CTkButton(self.button_frame, text='Select File', command=select_file)
        self.select_file_btn.grid(pady=5)

        self.apply_btn = ctk.CTkButton(self.button_frame, text='Apply', command=draw_text)
        self.apply_btn.grid(pady=5)

        self.save_btn = ctk.CTkButton(self.button_frame, text='Save', command=save_image)
        self.save_btn.grid(pady=5)

        # Sliders
        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.grid(row=1, column=1, rowspan=2)

        self.opacity_label = ctk.CTkLabel(self.slider_frame, text='Opacity')
        self.opacity_label.grid(row=1, column=0)

        self.opacity_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=100, orientation='vertical',
                                            number_of_steps=100)
        self.opacity_slider.grid(row=2, column=0)

        self.size_label = ctk.CTkLabel(self.slider_frame, text='Size')
        self.size_label.grid(row=1, column=1)

        self.size_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, orientation='vertical', number_of_steps=255)
        self.size_slider.grid(row=2, column=1, padx=20)

        # image canvas
        self.image_canvas = ctk.CTkCanvas(self, height=400, width=600)
        self.image_canvas.grid(row=0, column=0, columnspan=5, pady=20, padx=20)
        self.image_canvas.bind('<B1-Motion>', click_to_move)

        # Testing textbox
        self.text_box = tk.Text(self, width=50, height=10)
        self.text_box.grid(column=0, row=2, pady=20, padx=20)


class Painter:
    def __init__(self):
        self.image = None
        self.image_path = None

    def draw_text(self, text, opacity, size, position):
        try:
            with Image.open(self.image_path).convert('RGBA') as base:
                # make a blank image for the text, initialized to transparent text color
                overlay_image = Image.new("RGBA", base.size, (255, 255, 255, 0))

                # Get the font
                font = ImageFont.truetype(font='Pillow/Tests/FreeMono.ttf', size=size)
                # Get the context i.e. do what to what
                draw = ImageDraw.Draw(overlay_image)
                draw.text(position, text, font=font, fill=(255, 255, 255, opacity))

                out = Image.alpha_composite(base, overlay_image)
                # self.image = out
                return out

        except AttributeError:
            pop_up = messagebox
            pop_up.showwarning(title='File', message='No image provided.')

    def load_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path)
            return self.image
        return None


if __name__ == '__main__':
    app = App()

    app.mainloop()
