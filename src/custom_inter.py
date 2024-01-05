import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, END, colorchooser
from PIL import Image, ImageTk, ImageFont, ImageDraw

ctk.set_appearance_mode('dark')

ctk.set_default_color_theme('blue')


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Watermarker'
        self.minsize(width=400, height=360)
        self.painter = Painter()
        self.draw_pos = (0, 0)
        self.file_types = (('JPEG files', '*.jpeg *.jpg'),
                          ('PNG files', '*.png'),
                          ('All files', '*.*'))
        # Images have to be defined this way, so they don't get garbage collected
        self.image_to_display = None
        self.raw_image = None

        # Buttons
        def select_file():
            filetypes = (('JPEG files', '*.jpeg *.jpg'),
                         ('PNG files', '*.png'),
                         ('All files', '*.*'))

            file_path = filedialog.askopenfilename(filetypes=filetypes)
            if file_path:
                self.painter.image_path = file_path
                update_canvas(self.painter.load_image())

        def update_canvas(raw_image):
            self.raw_image = raw_image
            self.image_to_display = ImageTk.PhotoImage(raw_image)

            new_width = raw_image.size[0]
            new_height = raw_image.size[1]

            self.image_canvas.configure(width=new_width, height=new_height)
            self.image_canvas.create_image((0, 0), image=self.image_to_display, anchor='nw')

        def paint_image():
            if check_for_img():
                opacity = int(self.opacity_slider.get())
                size = int(self.size_slider.get())

                text_to_paint = self.text_box.get(0.0, END)
                raw_image = self.painter.draw_text(
                    text=text_to_paint,
                    opacity=opacity,
                    size=size,
                    position=self.draw_pos)

                update_canvas(raw_image)

        def pick_color():
            if check_for_img():
                self.painter.color = colorchooser.askcolor()
                update_canvas(self.raw_image)
                # TO-DO: Make this more efficient and less clunky
                self.color_preview.configure(background=self.painter.color[1])
                refresh_on_event(None)

        def click_to_move(event):
            self.draw_pos = (event.x, event.y)
            paint_image()

        def save_image():
            if check_for_img():
                # VERY SLOPPY, TO-DO: Fix this mess
                io_wrapper = filedialog.asksaveasfile(filetypes=self.file_types)

                path = str(io_wrapper).split(' ')[1]
                extension = path.split('.')[1].upper().strip("'")
                if extension == 'JPEG':
                    rgb_image = self.raw_image.convert('RGB')
                    rgb_image.save(io_wrapper)
                else:
                    self.raw_image.save(io_wrapper)

            else:
                return messagebox.showwarning(title='File', message='No image provided.')

        def check_for_img():
            if not self.painter.image:
                pop_up = messagebox
                pop_up.showwarning(title='File', message='No image provided.')
                return False
            return True

        def refresh_on_event(event):
            if check_for_img():
                paint_image()

        def reset_image():
            update_canvas(self.painter.load_image())

        def text_checkbox():
            if self.text_input_checkbox.get():
                # Text frame and box move
                self.text_frame.grid(row=1, column=2, padx=10, pady=10)
                self.text_input_checkbox.configure(self.text_frame)
                self.text_input_checkbox.grid(column=3, sticky='n')

            else:
                # Text Box remove and reset of elements
                self.text_frame.grid_forget()
                self.text_input_checkbox.configure(self)
                self.text_input_checkbox.grid(row=1, column=2)

        def transpose_image():
            if check_for_img():
                file_path = filedialog.askopenfilename(filetypes=self.file_types)
                if file_path:
                    image_transpose = Image.open(file_path)




        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(column=0, row=1, sticky='nw', padx=20)

        self.select_file_btn = ctk.CTkButton(self.button_frame, text='Select File', command=select_file)
        self.select_file_btn.grid(pady=5)

        self.save_btn = ctk.CTkButton(self.button_frame, text='Save', command=save_image)
        self.save_btn.grid(pady=5)

        self.reset_image_btn = ctk.CTkButton(self.button_frame, text='Reset', command=reset_image)
        self.reset_image_btn.grid(pady=5, row=3)

        # Sliders
        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.grid(row=1, column=1, rowspan=2)

        self.opacity_label = ctk.CTkLabel(self.slider_frame, text='Opacity')
        self.opacity_label.grid(row=0, column=0)

        self.opacity_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, orientation='vertical',
                                            number_of_steps=255, command=refresh_on_event)
        self.opacity_slider.grid(row=1, column=0)

        self.size_label = ctk.CTkLabel(self.slider_frame, text='Size')
        self.size_label.grid(row=0, column=1)

        self.size_slider = ctk.CTkSlider(self.slider_frame, from_=1, to=255, orientation='vertical',
                                         number_of_steps=255, command=refresh_on_event)
        self.size_slider.grid(row=1, column=1, padx=20)

        # Color select
        self.color_frame = ctk.CTkFrame(self.button_frame)
        self.color_frame.grid(row=2, column=0, sticky='nw', padx=20)

        self.color_preview = ctk.CTkCanvas(self.color_frame, width=20, height=20, background=self.painter.color[1])
        self.color_preview.grid(pady=10)

        self.pick_color_btn = ctk.CTkButton(self.color_frame, text='Pick Color', command=pick_color)
        self.pick_color_btn.grid(pady=5, row=2, column=0)

        # Testing textbox
        self.text_frame = ctk.CTkFrame(self)

        self.text_input_checkbox = ctk.CTkCheckBox(self, text='Input text', command=text_checkbox)
        self.text_input_checkbox.grid(row=1, column=2)

        self.text_label = ctk.CTkLabel(self.text_frame, text='Enter Text:')
        self.text_label.grid(padx=15, pady=5, row=0, sticky='w')

        self.text_box = tk.Text(self.text_frame, width=50, height=10)
        self.text_box.grid(row=1, pady=20, padx=20)

        self.apply_btn = ctk.CTkButton(self.text_frame, text='Apply', command=paint_image)
        self.apply_btn.grid(pady=5, sticky='e', padx=10)

        # Transpose image button
        self.add_image_btn = ctk.CTkButton(self.button_frame, text='Add image', command=transpose_image)
        self.add_image_btn.grid(pady=5)

        # Image canvas
        self.image_canvas = ctk.CTkCanvas(self, height=400, width=600)
        self.image_canvas.grid(row=0, column=0, columnspan=5, pady=20, padx=20)
        self.image_canvas.bind('<B1-Motion>', click_to_move)


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

            out = Image.alpha_composite(base, overlayed_image)
            return out

    def draw_image(self):
        """TO-DO: Add ability to transpose images, will probably need rework"""
        pass

    def load_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path)
            return self.image
        return None


if __name__ == '__main__':
    app = App()

    app.mainloop()
