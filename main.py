import tkinter as tk
from tkinter import messagebox

class Tracker:
    def __init__(self):
        self.totalCarbs = 0.0
        self.totalKcal = 0
        self.totalProteins = 0.0

    def log_intake(self):
        self.kcal = self.totalKcal + int(self.kcal_entry.get())
        self.carbs = self.totalCarbs + float(self.carbs_entry.get())
        self.proteins = self.totalProteins + float(self.proteins_entry.get())
        self.totalCarbs = self.carbs
        self.totalKcal = self.kcal
        self.totalProteins = self.proteins

    def show_totals(self):
        messagebox.showinfo("Total", "Carbs: " + str(self.totalCarbs) + "\nProteins: " + str(self.totalProteins) + "\nKcal: " + str(self.totalKcal))

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("Keto Calc by devSeh")

        self.kcal_label = tk.Label(self.root, text="Enter calories:")
        self.kcal_label.grid(row=0, column=0)
        self.kcal_entry = tk.Entry(self.root)
        self.kcal_entry.grid(row=0, column=1)

        self.carbs_label = tk.Label(self.root, text="Enter carbs:")
        self.carbs_label.grid(row=1, column=0)
        self.carbs_entry = tk.Entry(self.root)
        self.carbs_entry.grid(row=1, column=1)

        self.proteins_label = tk.Label(self.root, text="Enter proteins:")
        self.proteins_label.grid(row=2, column=0)
        self.proteins_entry = tk.Entry(self.root)
        self.proteins_entry.grid(row=2, column=1)

        self.log_button = tk.Button(self.root, text="Log", command=self.log_intake)
        self.log_button.grid(row=3, column=0)

        self.totals_button = tk.Button(self.root, text="Show Totals", command=self.show_totals)
        self.totals_button.grid(row=3, column=1)

        self.root.mainloop()

tracker = Tracker()
tracker.create_ui()
