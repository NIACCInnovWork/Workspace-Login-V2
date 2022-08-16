import tkinter as tk
from tkinter import ttk
from typing import Callable

from database.class_equipment import Equipment
from database.class_material import Material
from database.initialize_database import start_workspace_database
from user_interface.ScrollingListFrame import ScrollingListFrame


class ProjectFrame(tk.LabelFrame):
    # @Todo - Need to handle default values in some way

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent)

        self.on_remove_callback = None

        project_name_label = tk.Label(self, text="Name: ")
        self.project_name = tk.Entry(self)

        project_type_label = tk.Label(self, text="Type: ")
        self.project_type_variable = tk.StringVar(self)
        # project_type_variable.set('Personal')  # Set default value
        self.project_type = ttk.Combobox(self, textvariable=self.project_type_variable)
        self.project_type['values'] = ('Personal', 'Class', 'Entrepreneurial', 'Business')
        self.project_type['state'] = 'readonly'

        project_description_label = tk.Label(self, text="Description: ")
        self.project_description = tk.Entry(self, width=60)

        self.equipment_list_frame = ScrollingListFrame(self, height=115)
        self.equipment_list_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        self.equipment_frames_list = []

        self.add_equipment()

        add_equipment_button = tk.Button(self, text="Add Another Equipment", command=self.add_equipment)
        remove_project_button = tk.Button(self, text="Remove Project", command=lambda: self.on_remove_callback())

        project_name_label.grid(row=0, column=0, sticky=tk.E)
        self.project_name.grid(row=0, column=1, sticky=tk.W)

        project_type_label.grid(row=0, column=2, sticky=tk.E)
        self.project_type.grid(row=0, column=3, sticky=tk.W)

        project_description_label.grid(row=1, column=0, sticky=tk.E)
        self.project_description.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        add_equipment_button.grid(row=3, column=1, padx=10, pady=10)
        remove_project_button.grid(row=0, column=4, padx=4, pady=4)

    def add_equipment(self):
        """
        Dynamically adds equipment frames to the UI so projects can have multiple pieces of equipment used.
        :return: none
        """
        equipment = EquipmentFrame(self.equipment_list_frame.interior)
        equipment.on_remove(lambda: self.remove_equipment(equipment))
        self.equipment_frames_list.append(equipment)
        self.equipment_frames_list[-1].pack(padx=4, pady=4)

    def remove_equipment(self, equipment: 'EquipmentFrame'):
        """
        Dynamically removes equipment frames from the UI.
        Will throw a list index out of range error if there are no equipment elements, but this doesn't impact
        the rest of the application at this point.
        :return: none
        """
        self.equipment_frames_list.remove(equipment)
        equipment.destroy()

    def on_remove(self, callback: Callable):
        self.on_remove_callback = callback


class EquipmentFrame(tk.Frame):

    def __init__(self, parent):
        """
        Frame containing all the fields needed for the Equipment Record Object.
        :param parent: Parent widget in which this frame is placed
        """
        tk.Frame.__init__(self, parent)

        self.on_remove_callback = None

        def set_materials(event):
            equipment_name = event.widget.get()
            equipment_index = self.equipment_names.index(equipment_name)
            self.material_names_ids = Material.get_material_names_for_equipment(database,
                                                                                self.equipment_names_ids[
                                                                                    equipment_index][1])
            self.material_list = []
            for material in self.material_names_ids:
                self.material_list.append(material[0])

            self.material_used['values'] = self.material_list

        def set_unit(event):
            material_name = event.widget.get()
            material_unit = Material.get_unit(database, material_name)
            self.amount_used_unit.config(text=material_unit)

        # Data Validation to ensure time and amount entries are integers only
        def validate_int(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        validate_command = (self.register(validate_int))

        database = start_workspace_database()

        equipment_label = tk.Label(self, text="Equipment: ")

        self.equipment_names_ids = Equipment.get_all_equipment_names(database)
        self.equipment_names = []
        for equipment in self.equipment_names_ids:
            self.equipment_names.append(equipment[0])

        self.equipment_variable = tk.StringVar(self)
        self.equipment = ttk.Combobox(self, textvariable=self.equipment_variable)
        self.equipment['values'] = self.equipment_names
        self.equipment['state'] = 'readonly'
        self.equipment.bind("<<ComboboxSelected>>", set_materials)

        time_used_label = tk.Label(self, text="Time: ")
        self.time_used_hours = tk.Entry(self, width=5, validate='all', validatecommand=(validate_command, '%P'))
        hours_label = tk.Label(self, text="hr.")
        self.time_used_minutes = tk.Entry(self, width=5, validate='all', validatecommand=(validate_command, '%P'))
        minutes_label = tk.Label(self, text="min.")

        self.material_names_ids = []
        self.material_list = []
        material_used_label = tk.Label(self, text="Material: ")
        self.material_used_variable = tk.StringVar(self)
        self.material_used = ttk.Combobox(self, textvariable=self.material_used_variable)
        self.material_used['state'] = 'readonly'
        self.material_used.bind("<<ComboboxSelected>>", set_unit)

        amount_used_label = tk.Label(self, text="Amount: ")
        self.amount_used = tk.Entry(self, width=10, validate='all', validatecommand=(validate_command, '%P'))
        self.amount_used_unit = tk.Label(self, text="Unit", justify=tk.RIGHT)

        remove_item_button = tk.Button(self, text="Remove", command=lambda: self.on_remove_callback())

        equipment_label.grid(row=0, column=0, sticky=tk.E)
        self.equipment.grid(row=0, column=1, sticky=tk.W)

        time_used_label.grid(row=0, column=2, sticky=tk.E)
        self.time_used_hours.grid(row=0, column=3, sticky=tk.E)
        hours_label.grid(row=0, column=4, sticky=tk.W)
        self.time_used_minutes.grid(row=0, column=5, sticky=tk.E)
        minutes_label.grid(row=0, column=6, sticky=tk.W)

        material_used_label.grid(row=1, column=0, sticky=tk.E)
        self.material_used.grid(row=1, column=1, sticky=tk.W)

        amount_used_label.grid(row=1, column=2, sticky=tk.E)
        self.amount_used.grid(row=1, column=3, columnspan=2, sticky=tk.W)
        self.amount_used_unit.grid(row=1, column=5, sticky=tk.E)

        remove_item_button.grid(row=0, column=7, rowspan=2)

    def on_remove(self, callback: Callable):
        self.on_remove_callback = callback

    def get_equipment_id(self):
        equipment_name = self.equipment_variable.get()
        equipment_index = self.equipment_names.index(equipment_name)
        equipment_id = self.equipment_names_ids[equipment_index][1]
        return equipment_id

    def get_material_id(self):
        material_name = self.material_used_variable.get()
        material_index = self.material_list.index(material_name)
        material_id = self.material_names_ids[material_index][1]
        return material_id
