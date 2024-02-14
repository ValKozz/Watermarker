from button_icons import *
import customtkinter as ctk
from CTkMenuBar import *
import Pmw
from settings import *


class Buttons(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.init_buttons(parent)
        # self.init_dropdown(parent)

    def init_buttons(self, parent):
        self.pack(side='left', fill='y')

        self.btn_pick_color = ctk.CTkButton(self, image= color_palette_icon, text='', height=BUTTON_HEIGHT,
                                            width=BUTTON_WIDTH, command=parent.pick_color)
        self.btn_pick_color.pack(side='top', pady=10)

        self.pick_color_tooltip = Pmw.Balloon(self)
        self.pick_color_tooltip.bind(self.btn_pick_color, 'Change watermark color')

        # self.btn_pan = ctk.CTkButton(self, image=pan_icon, text='', height=BUTTON_HEIGHT, width=BUTTON_WIDTH,
        #                              command=None)
        # self.btn_pan.pack(side='top', pady=10)
        # self.pan_tooltip = Pmw.Balloon(self)
        # self.pan_tooltip.bind(self.btn_pan, 'Pan and zoom')
        #
        # self.btn_insert_text = ctk.CTkButton(self, image=text_icon, text='', height=BUTTON_HEIGHT, width=BUTTON_WIDTH,
        #                                      command=None)
        # self.btn_insert_text.pack(side='top', pady=10)
        # self.insert_text_tooltip = Pmw.Balloon(self)
        # self.insert_text_tooltip.bind(self.btn_insert_text, 'Insert text')
        #
        # self.btn_size_opacity = ctk.CTkButton(self, image=switch_icon, text='', height=BUTTON_HEIGHT,
        #                                       width=BUTTON_WIDTH,
        #                                       command=None)
        # self.btn_size_opacity.pack(side='top', pady=10)
        # self.size_opc_tooltip = Pmw.Balloon(self)
        # self.size_opc_tooltip.bind(self.btn_size_opacity, 'Edit size and opacity')

        self.btn_clear_layer = ctk.CTkButton(self, image=clear_layer_icon, text='', height=BUTTON_HEIGHT,
                                             width=BUTTON_WIDTH, command=parent.reset_image)

        self.btn_clear_layer.pack(side='top', pady=10)
        self.clear_tooltip = Pmw.Balloon(self)
        self.clear_tooltip.bind(self.btn_clear_layer, 'Reset Image')

        self.color_preview = ctk.CTkCanvas(self, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, background=parent.preview_color[1])
        self.color_preview.pack(side='bottom', pady=10)

    def configure_preview(self, parent):
        self.color_preview.configure(background=parent.preview_color[1])

    # def init_dropdown(self, parent):
    #     # Dropdown menu Setup
    #
    #     self.dropdown_menu = CTkMenuBar(master=parent)
    #     file_menu = self.dropdown_menu.add_cascade('File')
    #
    #     file_dropdown = CustomDropdownMenu(widget=file_menu)
    #     file_dropdown.add_option(option='Open...', command=parent.open_image)
    #     save_menu = file_dropdown.add_submenu('Save...')
    #     save_menu.add_option(option='Save', command=lambda: print('test'))
    #     save_menu.add_option(option='Save as...', command=parent.save_image)
