import customtkinter as ctk
from tkinter import filedialog
from settings import FILETYPES


class ImportImage(ctk.CTkFrame):
    def __init__(self, parent, import_img):
        super().__init__(master=parent)

        self.pack_configure(side='right', expand=True, fill='both', padx=15, pady=15)
        self.import_image = import_img

        btn_open = ctk.CTkButton(self, text='Open image', command=self.open_dialog)
        btn_open.pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfilename(filetypes=FILETYPES)
        self.import_image(path)


class ImgCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.configure(bg='#242424', background='#242424', bd=0, highlightthickness=0)

    def load_image(self, parent):
        self.pack(side='left', expand=True, padx=15, pady=15, fill='both')
        self.bind('<Configure>', parent.resize_image)