import customtkinter
# LIST = []
# def truncate(word, length=20):
#     if len(word) > length:
#         return word[:length] + "..."
#     return word

# def display():
#     for i in LIST:
#         f"{truncate(i['#'])} {truncate(i["person"], 30)} {truncate(i['available_day'])}"

class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="Initial text")
        self.label.grid(row=0, column=0, padx=20)
        self.next_row = 1
        
    def set_label_text(self, text):
        self.label.configure(text=text)
        
    def add_item(self, text):
        item = customtkinter.CTkLabel(self, text=text)
        item.grid(row=self.next_row, column=0, sticky="w", padx=20)
        self.next_row += 1

    def clear_content(self):
        for widget in self.winfo_children():
            if widget != self.label:
                widget.destroy()
        self.next_row = 1

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=1000, height=200)
        # self.textbox = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.my_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.list_items = 1  # instance variable

    def add_list_item(self):
        text = entry.get()
        self.my_frame.add_item(f"{self.list_items:}) {text}\n")
        self.list_items += 1

app = App()

button = customtkinter.CTkButton(app, text="CTkButton", command=app.add_list_item)
button.grid(row=1, column=1)

entry = customtkinter.CTkEntry(app, placeholder_text="CTkEntry")
entry.grid(row=1, column=0)

app.mainloop()
