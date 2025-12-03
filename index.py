import customtkinter as ctk

# -------------------------------------
# INITZ
# -------------------------------------

people = []

# -------------------------------------
# CLASSES
# -------------------------------------

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def add_person(self, person):
        def show_description():
            win = ctk.CTkToplevel(self)
            win.title("Description")
            label = ctk.CTkLabel(win, text=person["desc"], width=300, height=100)
            label.pack(padx=10, pady=10)

        item_button = ctk.CTkButton(self, text=person["name"], command=show_description)
        item_button.grid(row=self.next_row, column=0, sticky="w", padx=20)
        self.next_row += 1

    def list_data_ctk(self):
        # Headers
        headers = ["Id", "Name", "Description", "available", "lvl10%", "min buff", "max buff"]
        widths = [5, 20, 60, 20, 20, 20, 40, 40, 40] # = 265

        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self, text=text, anchor="w")
            lbl.grid(row=0, column=col, sticky="w", padx=3, pady=2)
            self.grid_columnconfigure(col, minsize=widths[col] * 6)

        # Rows
        for row, item in enumerate(people, start=1):
            name_display = item["name"][:12] + "..." if len(item["name"]) > 15 else item["name"]
            desc_display = item["desc"][:42] + "..." if len(item["desc"]) > 45 else item["desc"]
            available_display = item["available"][:7] + "..." if len(item["available"]) > 10 else item["available"]
            lvl10_display = item["lvl10"][:7] + "..." if len(item["lvl10"]) > 10 else item["lvl10"]
            min_buff_display = item["min_buff"][:7] + "..." if len(item["min_buff"]) > 10 else item["min_buff"]
            max_buff_display = item["max_buff"][:7] + "..." if len(item["max_buff"]) > 10 else item["max_buff"]

            ctk.CTkLabel(self, text=f"{row:>2}", anchor="w").grid(row=row, column=0, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=name_display, anchor="w").grid(row=row, column=1, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=desc_display, anchor="w").grid(row=row, column=2, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=available_display, anchor="w").grid(row=row, column=3, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=lvl10_display, anchor="w").grid(row=row, column=4, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=min_buff_display, anchor="w").grid(row=row, column=5, sticky="w", padx=3, pady=1)
            ctk.CTkLabel(self, text=max_buff_display, anchor="w").grid(row=row, column=6, sticky="w", padx=3, pady=1)

# -------------------------------------
# CTK
# -------------------------------------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        for i in range(8):
            self.grid_columnconfigure(i, weight=1)

        self.my_frame = MyFrame(master=self, width=1000, height=6)
        self.my_frame.grid(row=0, column=0, columnspan=100, sticky="nsew")

        # Entry fields to add new person
        self.name_ent = ctk.CTkEntry(self, placeholder_text="Name")
        self.name_ent.grid(row=1, column=0, sticky="nsew")

        self.desc_ent = ctk.CTkEntry(self, placeholder_text="Description")
        self.desc_ent.grid(row=1, column=1, sticky="nsew")

        self.available_ent = ctk.CTkEntry(self, placeholder_text="Available")
        self.available_ent.grid(row=1, column=2, sticky="nsew")

        self.lvl_entry = ctk.CTkEntry(self, placeholder_text="lvl 10")
        self.lvl_entry.grid(row=1, column=3, sticky="nsew")

        self.minimum_buff_entry = ctk.CTkEntry(self, placeholder_text="min buff lvl")
        self.minimum_buff_entry.grid(row=1, column=4, sticky="nsew")

        self.max_buff_entry = ctk.CTkEntry(self, placeholder_text="max buff lvl")
        self.max_buff_entry.grid(row=1, column=5, sticky="nsew")

        button = ctk.CTkButton(self, text="Add Person", command=self.add_person)
        button.grid(row=1, column=6, sticky="nsew")

    def add_person(self):
        # Get values from entry fields
        name = self.name_ent.get()
        desc = self.desc_ent.get()
        available = self.available_ent.get()
        lvl10 = self.lvl_entry.get()
        min_buff = self.minimum_buff_entry.get()
        max_buff = self.max_buff_entry.get()

        person = {"name": name, "desc": desc, "available": available, "lvl10": lvl10, "min_buff": min_buff, "max_buff": max_buff}
        people.append(person)

        # Clear input fields after adding
        self.name_ent.delete(0, ctk.END)
        self.desc_ent.delete(0, ctk.END)
        self.available_ent.delete(0, ctk.END)
        self.lvl_entry.delete(0, ctk.END)
        self.minimum_buff_entry.delete(0, ctk.END)
        self.max_buff_entry.delete(0, ctk.END)

        self.my_frame.list_data_ctk()

# -------------------------------------
# PROGRAM
# -------------------------------------

app = App()
app.minsize(800, 400)
app.title("EventManagment")

app.mainloop()