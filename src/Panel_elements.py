from customtkinter import CTkSlider, CTkLabel, CTkFrame, CTkButton
from tkinter import END, Text, filedialog
from settings import *


class TextFrame(CTkFrame):
    def __init__(self, parent, text_value, text_updater):
        super().__init__(master=parent)
        self.text_value = text_value
        self.init_text_layout(text_value, text_updater)

    def init_text_layout(self, text_value, text_updater):
        text_label = CTkLabel(self, text='Enter Text:')
        text_label.grid(row=1, column=0, pady=5, padx=10, sticky='W')

        self.text_box = Text(self, width=20, height=5)
        self.text_box.grid(row=2, column=0, columnspan=2, rowspan=2, pady=10, padx=10)
        if text_value:
            self.text_box.insert(0.0, text_value)
        else:
            self.text_box.insert(0.0, 'Sample Text')

        def get_text(event):
            if self.text_box.get(0.0, END):
                text_updater(text=self.text_box.get(0.0, END))
            else:
                text_updater(text='')

        self.text_box.bind('<KeyRelease>', get_text)


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
                                command=self.update_value_label,
                                ).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def update_value_label(self, value):
        self.value_label.configure(text=f'{round(value)}')


class FlipButtons(CTkFrame):
    def __init__(self, parent, text, options_updater):
        super().__init__(master=parent)
        options = FLIP_OPT
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

        def button_check():
            for button in self.buttons:
                if button.state == 'disabled':
                    button.configure(state='normal')
            for option in options:
                if option:
                    options[option] = False

        def click_0():
            button_check()
            self.none_btn.configure(state='disabled')
            options['FLIP_0'] = True
            options_updater(options)

        def click_m90():
            button_check()
            self.flip_m90_btn.configure(state='disabled')
            options['FLIP_-90'] = True
            options_updater(options)

        def click_90():
            button_check()
            self.flip90_btn.configure(state='disabled')
            options['FLIP_90'] = True
            options_updater(options)

        def click_180():
            button_check()
            self.flip180_btn.configure(state='disabled')
            options['FLIP_180'] = True
            options_updater(options)

        def click_mirror():
            button_check()
            self.flip_mirror.configure(state='disabled')
            options['FLIP_M'] = True
            options_updater(options)

        self.name_label = CTkLabel(self, text=text).grid(row=0, column=0, sticky='W', padx=5, columnspan=5)

        self.none_btn = CTkButton(self, text='0', width=PANEL_BUTTON_SIZE, height=PANEL_BUTTON_SIZE,
                                  command=click_0)
        self.none_btn.grid(row=1, column=0, padx=5)

        self.flip_m90_btn = CTkButton(self, text='-90', width=PANEL_BUTTON_SIZE, height=PANEL_BUTTON_SIZE,
                                      command=click_m90)
        self.flip_m90_btn.grid(row=1, column=1, padx=5)

        self.flip90_btn = CTkButton(self, text='90', width=PANEL_BUTTON_SIZE, height=PANEL_BUTTON_SIZE,
                                    command=click_90)
        self.flip90_btn.grid(row=1, column=2, padx=5)

        self.flip180_btn = CTkButton(self, text='180', width=PANEL_BUTTON_SIZE, height=PANEL_BUTTON_SIZE,
                                     command=click_180)
        self.flip180_btn.grid(row=1, column=3, padx=5)

        self.flip_mirror = CTkButton(self, text='Mirror', width=PANEL_BUTTON_SIZE, height=PANEL_BUTTON_SIZE,
                                     command=click_mirror)
        self.flip_mirror.grid(row=1, column=4, padx=5)

        self.buttons = [self.none_btn, self.flip90_btn, self.flip_m90_btn, self.flip180_btn, self.flip_mirror]


class ExportButtons(CTkFrame):
    def __init__(self, parent, save_func, open_func):
        super().__init__(master=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.init_layout(save_func, open_func)

    def init_layout(self, save_func, open_func):
        def save_as():
            save_btn.configure(state='normal', command=save_over_old)
            save_func()

        def save_over_old():
            # TODO
            save_func(saved=True)

        def open_new():
            path = filedialog.askopenfilename(filetypes=FILETYPES)
            open_func(path)

        save_label = CTkLabel(self, text='Save Image').grid(row=0, column=0, columnspan=2, pady=10)
        save_btn = CTkButton(self, text='Save', state='disabled')
        save_btn.grid(row=1, column=0, padx=10)

        saveas_btn = CTkButton(self, text='Save as.../Export', command=save_as)
        saveas_btn.grid(row=1, column=1, padx=10)

        reset_label = CTkLabel(self, text='Reset Image').grid(row=4, column=0, columnspan=2, pady=10)
        reset_btn = CTkButton(self, text='Reset')
        reset_btn.grid(row=5, column=0, columnspan=2)

        open_label = CTkLabel(self, text='Open New...').grid(row=6, column=0, columnspan=2, pady=10)
        open_btn = CTkButton(self, text='Open', command=open_new)
        open_btn.grid(row=7, column=0, columnspan=2)
