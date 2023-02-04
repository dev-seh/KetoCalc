import sqlite3
import tkinter as tk
from tkinter import messagebox
import datetime

class Tracker:
    def __init__(self):
        self.totalCarbs = 0.0
        self.totalKcal = 0
        self.totalProteins = 0.0
        self.conn = sqlite3.connect("tracker.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tracker (
                            date text,
                            totalCarbs real,
                            totalKcal integer,
                            totalProteins real
                        )""")

        self.conn.commit()

    def log_intake(self):
        self.kcal = self.totalKcal + int(self.kcal_entry.get())
        self.carbs = self.totalCarbs + float(self.carbs_entry.get())
        self.proteins = self.totalProteins + float(self.proteins_entry.get())
        self.totalCarbs = self.carbs
        self.totalKcal = self.kcal
        self.totalProteins = self.proteins
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO tracker VALUES (?, ?, ?, ?)", (today, self.totalCarbs, self.totalKcal, self.totalProteins))
        self.conn.commit()

    def retrieve_values(self):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM tracker WHERE date=?", (today,))
        result = self.cursor.fetchone()
        if result:
            self.totalCarbs = result[1]
            self.totalKcal = result[2]
            self.totalProteins = result[3]

    def undo_last_log(self):
        self.cursor.execute("DELETE FROM tracker WHERE date=? ORDER BY rowid DESC LIMIT 1", (today,))
        self.conn.commit()
        self.totalCarbs -= float(self.carbs_entry.get())
        self.totalKcal -= int(self.kcal_entry.get())
        self.totalProteins -= float(self.proteins_entry.get())        

    def reset_values(self):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("DELETE FROM tracker WHERE date=?", (today,))
        self.conn.commit()
        self.totalCarbs = 0.0
        self.totalKcal = 0
        self.totalProteins = 0.0

    def show_totals(self):
        messagebox.showinfo("Total", "Carbs: " + str(self.totalCarbs) + "\nProteins: " + str(self.totalProteins) + "\nKcal: " + str(self.totalKcal))

    def create_ui(self):
        self.retrieve_values()
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

        self.undo_button = tk.Button(self.root, text="Undo Last Log", command=self.undo_last_log)
        self.undo_button.grid(row=4, column=0)

        self.reset_button = tk.Button(self.root, text="Reset Totals", command=self.reset_values)
        self.reset_button.grid(row=4, column=1)

        self.root.mainloop()

tracker = Tracker()
tracker.create_ui()
