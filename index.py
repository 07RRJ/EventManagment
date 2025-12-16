import customtkinter as ctk
import csv

# -------------------------------------
# INITZ
# -------------------------------------

def load_data(filename): 
    products = []
    with open(filename, 'r') as file:       #öppnar en fil med read-rättighet
        reader = csv.DictReader(file)
        for row in reader:
            id_ = row["id"]
            name = row['name']
            desc = row['desc']
            available = row['available']
            lvl10 = row['lvl10']
            min_buff = row['min_buff']
            max_buff = row['max_buff']
            
            products.append(
                {
                    "id": int(id_),
                    "name": name,
                    "desc": desc,
                    "available": available,
                    "lvl10": lvl10,
                    "min_buff": min_buff,
                    "max_buff": max_buff
                }
            )
    return products

FileName = "DbPeople.csv"
people = load_data(FileName)

# -------------------------------------
# CLASSES
# -------------------------------------

class MyFrame(ctk.CTkScrollableFrame): # the list
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.next_row = 1
        self.current_total_width = master.winfo_width()

    def update_column_widths(self, total_width):
        proportions = [0.05, 0.15, 0.35, 0.1, 0.1, 0.1, 0.15]
        widths = [int(total_width * p) for p in proportions]

        for col, width in enumerate(widths): # scale the column
            self.grid_columnconfigure(col, minsize=width)
        for child in self.winfo_children(): # fix the rest
            if isinstance(child, ctk.CTkFrame):
                for col, width in enumerate(widths):
                    child.grid_columnconfigure(col, minsize=width)

    def show_edit_window(self, person, person_index): # when person clicked on show this
        win = ctk.CTkToplevel(self)
        win.title(f"Edit Details for {person['name']}")

        # edit data v
        name_entry = ctk.CTkEntry(win, placeholder_text="Name")
        name_entry.insert(0, person['name'])
        name_entry.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        desc_entry = ctk.CTkEntry(win, placeholder_text="Description")
        desc_entry.insert(0, person['desc'])
        desc_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        available_entry = ctk.CTkEntry(win, placeholder_text="Available")
        available_entry.insert(0, person['available'])
        available_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        lvl10_entry = ctk.CTkEntry(win, placeholder_text="Lvl 10%")
        lvl10_entry.insert(0, person['lvl10'])
        lvl10_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        min_buff_entry = ctk.CTkEntry(win, placeholder_text="Min Buff")
        min_buff_entry.insert(0, person['min_buff'])
        min_buff_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        max_buff_entry = ctk.CTkEntry(win, placeholder_text="Max Buff")
        max_buff_entry.insert(0, person['max_buff'])
        max_buff_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        for i in range(2):
            win.grid_columnconfigure(i, weight=1)

        def save_changes(): # if save change the og list
            person['name'] = name_entry.get()
            person['desc'] = desc_entry.get()
            person['available'] = available_entry.get()
            person['lvl10'] = lvl10_entry.get()
            person['min_buff'] = min_buff_entry.get()
            person['max_buff'] = max_buff_entry.get()

            people[person_index] = person
            win.destroy()
            app.my_frame.list_data_ctk()
            app.set_editing(False)

        def delete_person(): # remove from list
            del people[person_index]
            win.destroy()
            app.my_frame.list_data_ctk()
            app.set_editing(False)

        save_button = ctk.CTkButton(win, text="Save Changes", command=save_changes)
        save_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        delete_button = ctk.CTkButton(win, text="Delete", fg_color="red", hover_color="#aa0000", command=delete_person)
        delete_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        app.set_editing(True, person_index)

    def add_person(self, person, person_index=None): # add to the list
        display_values = [
            f"{self.next_row:>2}",
            person["name"][:12] + "..." if len(person["name"]) > 15 else person["name"],
            person["desc"][:42] + "..." if len(person["desc"]) > 45 else person["desc"],
            person["available"][:7] + "..." if len(person["available"]) > 10 else person["available"],
            person["lvl10"][:7] + "..." if len(person["lvl10"]) > 10 else person["lvl10"],
            person["min_buff"][:7] + "..." if len(person["min_buff"]) > 10 else person["min_buff"],
            person["max_buff"][:7] + "..." if len(person["max_buff"]) > 10 else person["max_buff"]
        ]

        for col, value in enumerate(display_values):
            label = ctk.CTkLabel(self, text=value, anchor="w")
            label.grid(row=self.next_row, column=col, sticky="w", padx=3, pady=2)
            label.bind("<Button-1>",
                    lambda event, p=person, idx=person_index: self.show_edit_window(p, idx))
        self.next_row += 1

    def list_data_ctk(self): # dissplay current data
        for widget in self.winfo_children():
            widget.destroy()
        self.next_row = 1

        # headers
        headers = ["Id", "Name", "Description", "Available", "Lvl 10%", "Min Buff", "Max Buff"]
        widths = [5, 20, 60, 20, 20, 20, 40]

        # create headers
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self, text=text, anchor="w")
            lbl.grid(row=0, column=col, sticky="w", padx=3, pady=2)
            self.grid_columnconfigure(col, minsize=widths[col] * 6)

        # display rows
        for row, item in enumerate(people, start=1):
            self.add_person(item, person_index=row - 1)

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

        self.bind("<Configure>", self.on_resize)

        self._last_size = (self.winfo_width(), self.winfo_height())
        
        # entry fields to add new person v
        self.name_ent = ctk.CTkEntry(self, placeholder_text="Name")
        self.name_ent.grid(row=1, column=0, sticky="nsew")

        self.desc_ent = ctk.CTkEntry(self, placeholder_text="Description")
        self.desc_ent.grid(row=1, column=1, sticky="nsew")

        self.available_ent = ctk.CTkEntry(self, placeholder_text="Available")
        self.available_ent.grid(row=1, column=2, sticky="nsew")

        self.lvl_entry = ctk.CTkEntry(self, placeholder_text="Lvl 10")
        self.lvl_entry.grid(row=1, column=3, sticky="nsew")

        self.minimum_buff_entry = ctk.CTkEntry(self, placeholder_text="Min Buff Lvl")
        self.minimum_buff_entry.grid(row=1, column=4, sticky="nsew")

        self.max_buff_entry = ctk.CTkEntry(self, placeholder_text="Max Buff Lvl")
        self.max_buff_entry.grid(row=1, column=5, sticky="nsew")

        button = ctk.CTkButton(self, text="Add Person", command=self.add_person)
        button.grid(row=1, column=6, sticky="nsew")

        self.save_button = ctk.CTkButton(self, text="Save to CSV", command=self.save_to_csv)
        self.save_button.grid(row=1, column=7, sticky="nsew")

        self.is_editing = False
        self.editing_person_index = None

        self.my_frame.list_data_ctk()

    def on_resize(self, event): # check if need to resize
        new_size = (self.winfo_width(), self.winfo_height())
        if new_size == getattr(self, "_last_size", None):
            return  # no size change, ignore
        self._last_size = new_size

        if hasattr(self, "_resize_timer"): # debounce
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(250, self._handle_resize)

    def _handle_resize(self): # resize
        new_width = self.winfo_width()
        self.my_frame.update_column_widths(new_width)

    def set_editing(self, is_editing, person_index=None): # keep the order
        self.is_editing = is_editing
        self.editing_person_index = person_index

    def add_person(self):
        if self.is_editing:
            return  # prevent adding if currently editing an existing person

        # get values from entry fields v
        name = self.name_ent.get()
        desc = self.desc_ent.get()
        available = self.available_ent.get()
        lvl10 = self.lvl_entry.get()
        min_buff = self.minimum_buff_entry.get()
        max_buff = self.max_buff_entry.get()

        if people:
            new_id = max(p["id"] for p in people) + 1
        else:
            new_id = 1

        # shove it in a dictionary
        person = {
            "id": new_id,
            "name": name,
            "desc": desc,
            "available": available,
            "lvl10": lvl10,
            "min_buff": min_buff,
            "max_buff": max_buff
        }
        people.append(person)

        # clear input fields after adding v
        self.name_ent.delete(0, ctk.END)
        self.desc_ent.delete(0, ctk.END)
        self.available_ent.delete(0, ctk.END)
        self.lvl_entry.delete(0, ctk.END)
        self.minimum_buff_entry.delete(0, ctk.END)
        self.max_buff_entry.delete(0, ctk.END)

        self.my_frame.list_data_ctk()

    def save_to_csv(self):
        fieldnames = ["id", "name", "desc", "available", "lvl10", "min_buff", "max_buff"]
        with open(FileName, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(people)

# -------------------------------------
# PROGRAM
# -------------------------------------

app = App()
app.minsize(800, 400)
app.title("Event Management")

app.my_frame.list_data_ctk()

app.mainloop()