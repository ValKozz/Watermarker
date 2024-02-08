from customtkinter import CTkTabview
from customtkinter import CTkButton, CTkSlider, CTkLabel
from button_icons import close_icon
from tkinter import Text, END


class ImgProperties(CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(width=150)

        self.show_sliders = False
        self.show_text = False
        self.text_value = 'Watermark'

    def init_sliders_layout(self):
        # Sliders

        self.slider_close_btn = CTkButton(self.sliders_tab, image=close_icon, height=10, width=10, text=None,
                                          anchor='ne',
                                          fg_color='transparent', command=self.show_sliders_)
        self.slider_close_btn.grid(row=0, column=2)

        self.opacity_label = CTkLabel(self.sliders_tab, text='Opacity')
        self.opacity_label.grid(row=0, column=0)

        self.opacity_slider = CTkSlider(self.sliders_tab, from_=0, to=255, orientation='vertical',
                                        number_of_steps=255)
        self.opacity_slider.grid(row=1, column=0)

        self.size_label = CTkLabel(self.sliders_tab, text='Size')
        self.size_label.grid(row=0, column=1)

        self.size_slider = CTkSlider(self.sliders_tab, from_=1, to=255, orientation='vertical',
                                     number_of_steps=255)
        self.size_slider.grid(row=1, column=1, padx=20, pady=5)

    def init_text_layout(self):
        # Text box

        self.text_close_btn = CTkButton(self.text_tab, image=close_icon, height=10, width=10, text=None,
                                        anchor='ne',
                                        fg_color='transparent', command=self.show_text_)
        self.text_close_btn.grid(row=0, column=1)

        self.text_label = CTkLabel(self.text_tab, text='Enter Text:')
        self.text_label.grid(row=1, column=0, pady=10, padx=10)

        self.text_box = Text(self.text_tab, width=20, height=5)
        self.text_box.grid(row=2, column=0, columnspan=2, rowspan=2, pady=10, padx=10)
        self.text_box.bind('<KeyRelease>', self.print_event)

    def show_sliders_(self):
        if self.show_sliders:
            self.show_sliders = False
            self.delete('Sliders')
        else:
            self.show_sliders = True
            self.sliders_tab = self.add('Sliders')

            self.init_sliders_layout()
        self.is_populated()

    def show_text_(self):
        if self.show_text:
            self.show_text = False
            self.delete('Text_box')

        else:
            self.show_text = True
            self.text_tab = self.add('Text_box')

            self.init_text_layout()
        self.is_populated()

    def is_populated(self):
        if not self.show_sliders and not self.show_text:
            self.pack_forget()
        else:
            self.pack(side='left', fill='y')

    def print_event(self, event):
        self.text_value = self.text_box.get(0.0, END)