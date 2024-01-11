from Painter import Painter
from Toplevel_properties import ToplevelWindow
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image
import Pmw
from CTkMenuBar import *

ctk.set_appearance_mode('dark')

ctk.set_default_color_theme('blue')

brush_image = ctk.CTkImage(Image.open('../icons/brush.png'))
image_image = ctk.CTkImage(Image.open('../icons/image.png'))
switches_image = ctk.CTkImage(Image.open('../icons/switches.png'))
clear_layer_image = ctk.CTkImage(Image.open('../icons/layers_clear.png'))
color_palette_image = ctk.CTkImage(Image.open('../icons/palette.png'))
text_image = ctk.CTkImage(Image.open('../icons/text_enter.png'))


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Watermarker')
        self.minsize(width=960, height=540)
        self.painter = Painter()
        self.draw_pos = (0, 0)
        self.file_types = (('JPEG files', '*.jpeg *.jpg'),
                           ('PNG files', '*.png'),
                           ('All files', '*.*'))
        # Images have to be defined this way, so they don't get garbage collected
        self.image_to_display = None
        self.top_level = None
        self.last_saved = False

        def open_sliders():
            if self.top_level is None or not self.top_level.winfo_exists():
                self.top_level = ToplevelWindow()
                self.top_level.show_sliders()
            elif self.top_level.sliders_visible:
                self.top_level.lift()
                self.top_level.focus()

        def open_textbox():
            if self.top_level is None or not self.top_level.winfo_exists():
                self.top_level = ToplevelWindow()
                self.top_level.show_text()
            elif self.top_level.text_visible:
                self.top_level.lift()
                self.top_level.focus()
            else:
                self.top_level.show_text()
                self.top_level.lift()

        def select_file():
            file_path = filedialog.askopenfilename(filetypes=self.file_types)

            if file_path:
                self.painter.image_path = file_path
                self.painter.load_image()
                update_canvas()

        def update_canvas():
            self.last_saved = False
            # TO-DO: Dynamic resize

            raw_image = self.painter.image
            self.image_to_display = self.painter.return_image()

            new_width = raw_image.size[0]
            new_height = raw_image.size[1]

            self.canvas.configure(width=new_width, height=new_height)
            self.canvas.pack(expand=False, padx=15, pady=15)
            self.canvas.create_image((new_width/2, new_height/2), image=self.image_to_display, anchor='center')

        self.draw_value_buffer = None

        def paint_image():
            if check_for_img():
                if self.top_level:
                    self.draw_value_buffer = self.top_level.return_values()
                print(self.draw_value_buffer)
                # TODODODODODODODODODODOD
                self.painter.draw_text(
                    text=self.draw_value_buffer['text'],
                    opacity=self.draw_value_buffer['opacity'],
                    size=self.draw_value_buffer['size'],
                    position=self.draw_pos)

                update_canvas()

        def pick_color():
            if check_for_img():
                self.painter.color = colorchooser.askcolor()
                self.color_preview.configure(background=self.painter.color[1])
                update_canvas()
                # TO-DO: Make this more efficient and less clunky
                refresh_on_event(None)

        def click_to_move(event):
            self.draw_pos = (event.x, event.y)
            print(self.draw_pos)
            paint_image()

        def save_image():
            if check_for_img():
                # VERY SLOPPY, TO-DO: Fix this mess
                io_wrapper = filedialog.asksaveasfile(filetypes=self.file_types)
                if io_wrapper:
                    path = str(io_wrapper).split(' ')[1]
                    extension = path.split('.')[1].upper().strip("'")

                    self.painter.save_image(extension, io_wrapper)
                    self.last_saved = True

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
            if check_for_img():
                self.painter.reset_image()
                update_canvas()

        def warn_on_close():
            if self.painter.image and not self.last_saved:
                response = messagebox.askyesnocancel('Exit', 'Are you sure you want to exit without saving?')
                print(response)
                if response:
                    self.destroy()
                elif response is None:
                    return None
                elif response is False:
                    save_image()
                    self.destroy()
            self.destroy()

        # Dropdown menu Setup
        self.dropdown_menu = CTkMenuBar(master=self)
        file_menu = self.dropdown_menu.add_cascade('File')

        file_dropdown = CustomDropdownMenu(widget=file_menu)
        file_dropdown.add_option(option='Open...', command=select_file)
        save_menu = file_dropdown.add_submenu('Save...')
        save_menu.add_option(option='Save', command=lambda: print('test'))
        save_menu.add_option(option='Save as...', command=save_image)

        # Canvas
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(side='right', expand=True, fill='both', padx=15, pady=15)
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg='#121212', background='#121212')
        self.canvas.bind('<B1-Motion>', click_to_move)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(side='left', fill='y')

        # TO-DO: implement painting on image
        self.button_paint = ctk.CTkButton(self.button_frame, image=brush_image, text=None, height=22, width=22)
        self.button_paint.pack(side='top', pady=10)
        self.paint_tooltip = Pmw.Balloon(self)
        self.paint_tooltip.bind(self.button_paint, 'Paint on image(TO BE IMPLEMENTED)')

        self.button_chose_color = ctk.CTkButton(self.button_frame, image=color_palette_image, text=None, height=22,
                                                width=22, command=pick_color)
        self.button_chose_color.pack(side='top', pady=10)
        self.palette_tooltip = Pmw.Balloon(self)
        self.palette_tooltip.bind(self.button_chose_color, 'Change watermark color')

        self.button_image = ctk.CTkButton(self.button_frame, image=image_image, text=None, height=22, width=22,
                                          command=None)
        self.button_image.pack(side='top', pady=10)
        self.image_tooltip = Pmw.Balloon(self)
        self.image_tooltip.bind(self.button_image, 'Transpose image(TO BE IMPLEMENTED)')

        self.text_edit_button = ctk.CTkButton(self.button_frame, image=text_image, text=None, height=22, width=22,
                                              command=open_textbox)
        self.text_edit_button.pack(side='top', pady=10)
        self.text_tooltip = Pmw.Balloon(self)
        self.text_tooltip.bind(self.text_edit_button, 'Enter text')

        self.button_switches = ctk.CTkButton(self.button_frame, image=switches_image, text=None, height=22, width=22,
                                             command=open_sliders)
        self.button_switches.pack(side='top', pady=10)
        self.switches_tooltip = Pmw.Balloon(self)
        self.switches_tooltip.bind(self.button_switches, 'Edit size and opacity')

        self.button_clear_layer = ctk.CTkButton(self.button_frame, image=clear_layer_image, text=None, height=22,
                                                width=22, command=reset_image)

        self.button_clear_layer.pack(side='top', pady=10)
        self.clear_tooltip = Pmw.Balloon(self)
        self.clear_tooltip.bind(self.button_clear_layer, 'Clear Edit layer')

        self.color_preview = ctk.CTkCanvas(self.button_frame, width=22, height=22, background=self.painter.color[1])
        self.color_preview.pack(side='bottom', pady=10)

        self.protocol('WM_DELETE_WINDOW', warn_on_close)


if __name__ == '__main__':
    app = App()
    app.mainloop()
