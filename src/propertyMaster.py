from customtkinter import CTkButton, CTkFrame, CTkTabview
from button_icons import open_panel, close_panel
from Panel_elements import TextFrame, Sliders, PropertyButtons
from settings import *


class PropertyMasterPanel(CTkFrame):
    def __init__(self, parent, size, opacity, wt_rotation, text, img_rotation, text_updater):
        super().__init__(parent)
        self.pack(side='right', fill='y', expand=False)
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=6, uniform='a')

        self.is_open = False
        self.button = None
        self.init_button()
        self.tabs = PropTabs(self, size, opacity, wt_rotation, text, img_rotation, text_updater)

    def init_button(self):
        self.button = CTkButton(self, text='', image=open_panel, height=BUTTON_HEIGHT, width=BUTTON_WIDTH,
                                fg_color='transparent', command=self.button_logic)
        self.button.grid(row=0, column=0, sticky='N')

    def button_logic(self):
        if self.is_open:
            self.is_open = False
            self.button.configure(image=open_panel)
            self.tabs.grid_forget()  # Forget Tab View

        else:
            self.button.configure(image=close_panel)
            self.is_open = True
            self.init_tabs()  # init Tab view

    def init_tabs(self):
        self.tabs.grid(row=0, column=1, padx=5, rowspan=10, sticky='N')


class PropTabs(CTkTabview):
    def __init__(self, parent, size, opacity, wt_rotation, text, img_rotation, text_updater):
        super().__init__(master=parent)

        self.wt_props = self.add('Watermark Options')
        self.image_props = self.add('Image Properties')
        self.export_img = self.add('Export/Save')

        self.init_wt_props(size, opacity, wt_rotation, text, text_updater)
        self.init_img_props(img_rotation)

    def init_wt_props(self, size, opacity, wt_rotation, text, text_updater):

        self.wt_props.rowconfigure((0, 1, 2, 3), weight=1)
        self.wt_props.columnconfigure((0, 1), weight=1)

        text_fr = TextFrame(self.wt_props, text, text_updater).grid(row=0, column=0, columnspan=2)
        size_slider = Sliders(self.wt_props, 'Size', size, 0, 255).grid(row=1, column=0, columnspan=2, pady=20)
        opacity_slider = Sliders(self.wt_props, 'Opacity', opacity, 0, 255).grid(row=2, column=0, columnspan=2, pady=20)
        rotation = Sliders(self.wt_props, 'Rotation', wt_rotation, 0, 360).grid(row=3, column=0, columnspan=2, pady=20)

    def init_img_props(self, rotation):
        self.image_props.rowconfigure((0, 1, 2, 3), weight=1)
        self.image_props.columnconfigure((0, 1), weight=1)

        rotation = Sliders(self.image_props, 'Rotation', rotation, 0, 360).grid(row=0, column=0, columnspan=2, pady=20)
        test_panel = PropertyButtons(self.image_props, 'Test Flip', 0).grid(row=1, column=0, columnspan=2, pady=20)