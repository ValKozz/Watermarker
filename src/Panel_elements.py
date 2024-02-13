from customtkinter import CTkSlider, CTkLabel, CTkFrame, CTkButton
from tkinter import END, Text


class TextFrame(CTkFrame):
    # TO-DO: Dynamic text update, all the way to main
    def __init__(self, parent, text_value):
        super().__init__(master=parent)
        self.text_value = text_value
        self.init_text_layout(text_value)

    def init_text_layout(self, text_value):
        text_label = CTkLabel(self, text='Enter Text:')
        text_label.grid(row=1, column=0, pady=5, padx=10, sticky='W')

        self.text_box = Text(self, width=20, height=5)
        self.text_box.grid(row=2, column=0, columnspan=2, rowspan=2, pady=10, padx=10)
        self.text_box.insert(0.0, text_value)

        self.text_box.bind('<KeyRelease>', self.get_text)

    def get_text(self, event):
        self.text_value = self.text_box.get(0.0, END)


class Sliders(CTkFrame):
    def __init__(self, parent, text, value, min, max):
        super().__init__(master=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.name_label = CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.value_label = CTkLabel(self, text=value.get())
        self.value_label.grid(column=1, row=0, sticky='E', padx=5)
        self.slider = CTkSlider(self,
                                from_=min,
                                to=max,
                                variable=value,
                                command=self.update_value_label
                                ).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def update_value_label(self, value):
        self.value_label.configure(text=f'{round(value)}')


class PropertyButtons(CTkFrame):
    def __init__(self, parent, text, options):
        super().__init__(master=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        self.name_label = CTkLabel(self, text=text).grid(row=0, column=0, sticky='W', padx=5)
