from customtkinter import CTkTabview

class Tabs(CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.add('Tab1')