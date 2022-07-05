import tkinter as tk
from tkinter import ttk
from typing import Callable

from user_interface.ScrollingListFrame import ScrollingListFrame


class ProjectFrame(tk.LabelFrame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent)

        project_name_label = tk.Label(self, text="Name")
        self.project_name = tk.Entry(self)

        project_type_label = tk.Label(self, text="Type")
        self.project_type = tk.Entry(self)

        project_description_label = tk.Label(self, text="Description")
        self.project_description = tk.Text(self, width=30, height=3)

        self.frame = ScrollingListFrame(self)
        self.frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        self.equipment_frames_list = []

        self.add_equipment()

        add_equipment_button = tk.Button(self, text="Add Another Equipment", command=self.add_equipment)

        project_name_label.grid(row=0, column=0, sticky=tk.E)
        self.project_name.grid(row=0, column=1, sticky=tk.W)

        project_type_label.grid(row=0, column=2, sticky=tk.E)
        self.project_type.grid(row=0, column=3, sticky=tk.W)

        project_description_label.grid(row=1, column=0, sticky=tk.E)
        self.project_description.grid(row=1, column=1, sticky=tk.W)

        add_equipment_button.grid(row=3, column=1, padx=10, pady=10)

    def add_equipment(self):
        """
        Dynamically adds equipment frames to the UI so projects can have multiple pieces of equipment used.
        :return: none
        """
        equipment = EquipmentFrame(self.frame.interior)
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


class EquipmentFrame(tk.Frame):

    def __init__(self, parent):
        """
        Frame containing all the fields needed for the Equipment Record Object.
        :param parent: Parent widget in which this frame is placed
        """
        tk.Frame.__init__(self, parent)

        self.on_remove_callback = None
        machine_label = tk.Label(self, text="Equipment: ")
        machine = ttk.Combobox(self)

        time_used_label = tk.Label(self, text="Time: ")
        time_used = tk.Label(self, relief="sunken", width=30)

        material_used_label = tk.Label(self, text="Material: ")
        material_used = ttk.Combobox(self)

        amount_used_label = tk.Label(self, text="Amount: ")
        amount_used = tk.Entry(self, width=30)

        remove_item_button = tk.Button(self, text="Remove", command=lambda: self.on_remove_callback())

        machine_label.grid(row=0, column=0, sticky=tk.E)
        machine.grid(row=0, column=1, sticky=tk.W)

        time_used_label.grid(row=0, column=2, sticky=tk.E)
        time_used.grid(row=0, column=3, sticky=tk.W)

        material_used_label.grid(row=1, column=0, sticky=tk.E)
        material_used.grid(row=1, column=1, sticky=tk.W)

        amount_used_label.grid(row=1, column=2, sticky=tk.E)
        amount_used.grid(row=1, column=3, sticky=tk.W)

        remove_item_button.grid(row=1, column=4, rowspan=2)

    def on_remove(self, callback: Callable):
        self.on_remove_callback = callback
