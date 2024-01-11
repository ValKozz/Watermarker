import customtkinter as ctk
from tkinter import END
from PIL import Image

close_image = ctk.CTkImage(Image.open('../icons/close.png'))


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Properties')
        self.text_visible = False
        self.sliders_visible = False

        # Sliders
        self.slider_frame = ctk.CTkFrame(self)

        self.slider_close_btn = ctk.CTkButton(self.slider_frame, image=close_image, height=10, width=10, text=None,
                                              anchor='ne',
                                              fg_color='transparent', command=self.show_sliders)
        self.slider_close_btn.grid(row=0, column=2)

        self.opacity_label = ctk.CTkLabel(self.slider_frame, text='Opacity')
        self.opacity_label.grid(row=0, column=0)

        self.opacity_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=255, orientation='vertical',
                                            number_of_steps=255)
        self.opacity_slider.grid(row=1, column=0)

        self.size_label = ctk.CTkLabel(self.slider_frame, text='Size')
        self.size_label.grid(row=0, column=1)

        self.size_slider = ctk.CTkSlider(self.slider_frame, from_=1, to=255, orientation='vertical',
                                         number_of_steps=255)
        self.size_slider.grid(row=1, column=1, padx=20)

        # Text
        self.text_frame = ctk.CTkFrame(self)

        self.text_close_btn = ctk.CTkButton(self.text_frame, image=close_image, height=10, width=10, text=None,
                                            anchor='ne',
                                            fg_color='transparent', command=self.show_text)
        self.text_close_btn.grid(row=0, column=2)

        self.text_label = ctk.CTkLabel(self.text_frame, text='Enter Text:')
        self.text_label.grid(row=0, column=0, pady=10, padx=10)

        self.text_box = tk.Text(self.text_frame, width=50, height=10)
        self.text_box.grid(row=1, column=0, columnspan=2, rowspan=2, pady=10, padx=10)

        self.apply_btn = ctk.CTkButton(self.text_frame, text='Apply')
        self.apply_btn.grid(row=3, column=1, padx=0, pady=10, sticky='e')

    def show_sliders(self):
        if not self.sliders_visible:
            self.sliders_visible = True
            self.slider_frame.pack(pady=10, padx=20, side='top', expand=True)
        else:
            self.sliders_visible = False
            self.slider_frame.pack_forget()
            self.is_populated()

    def show_text(self):
        if not self.text_visible:
            self.text_visible = True
            self.text_frame.pack(side='top', expand=True, pady=10)
        else:
            self.text_visible = False
            self.text_frame.pack_forget()
            self.is_populated()

    def is_populated(self):
        if self.text_visible or self.sliders_visible:
            pass
        else:
            self.destroy()

    def return_values(self):
        size = int(self.size_slider.get())
        opacity = int(self.opacity_slider.get())
        text = self.text_box.get(0.0, END)

        values = {
            'size': size,
            'opacity': opacity,
            'text': text
        }

        return values
