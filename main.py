import sqlite3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import datetime

class Tracker():
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

    def log_intake(self, instance):
        kcal_entry = instance.kcal_entry
        self.totalKcal = self.totalKcal + int(kcal_entry.text)
        carbs_entry = instance.carbs_entry
        self.totalCarbs = self.totalCarbs + float(carbs_entry.text)
        proteins_entry = instance.proteins_entry
        self.totalProteins = self.totalProteins + float(proteins_entry.text)
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT INTO tracker VALUES (?, ?, ?, ?)", (today, self.totalCarbs, self.totalKcal, self.totalProteins))
        self.conn.commit()

    def retrieve_values(self):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM tracker WHERE date=?", (today,))
        result = self.cursor.fetchone()
        if result:
            self.totalCarbs += result[1]
            self.totalKcal += result[2]
            self.totalProteins += result[3]

    def undo_last_log(self, instance):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("DELETE FROM tracker WHERE date=? ORDER BY rowid DESC LIMIT 1", (today,))
        self.conn.commit()
        self.totalCarbs -= float(instance.carbs_entry.text)
        self.totalKcal -= int(instance.kcal_entry.text)
        self.totalProteins -= float(instance.proteins_entry.text)            

    def reset_values(self, instance):
        today = datetime.datetime.now().date().strftime("%Y-%m-%d")
        self.cursor.execute("DELETE FROM tracker WHERE date=?", (today,))
        self.conn.commit()
        self.totalCarbs = 0.0
        self.totalKcal = 0
        self.totalProteins = 0.0

    def show_totals(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Carbs: " + str(self.totalCarbs)))
        content.add_widget(Label(text="Proteins: " + str(self.totalProteins)))
        content.add_widget(Label(text="Kcal: " + str(self.totalKcal)))
        popup = Popup(title="Total", content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

        
    
class TrackerApp(App):
    def build(self):
        self.tracker = Tracker()
        self.tracker.retrieve_values()
        grid = GridLayout(cols=2)
        self.kcal_label = Label(text='Enter calories:')
        self.kcal_entry = TextInput(multiline=False)
        self.carbs_label = Label(text='Enter carbs:')
        self.carbs_entry = TextInput(multiline=False)
        self.proteins_label = Label(text='Enter proteins:')
        self.proteins_entry = TextInput(multiline=False)
        self.log_button = Button(text='Log', on_press=lambda x: self.tracker.log_intake(self))
        self.totals_button = Button(text="Show totals", on_press=self.tracker.show_totals)
        self.reset_button = Button(text='Reset Totals', on_press=self.tracker.reset_values)


        grid.add_widget(self.kcal_label)
        grid.add_widget(self.kcal_entry)
        grid.add_widget(self.carbs_label)
        grid.add_widget(self.carbs_entry)
        grid.add_widget(self.proteins_label)
        grid.add_widget(self.proteins_entry)
        grid.add_widget(self.log_button)
        grid.add_widget(self.totals_button)
        grid.add_widget(self.reset_button)

        return grid
    def on_start(self):
        self.tracker.retrieve_values()

    def on_stop(self):
        self.tracker.conn.close()
    

TrackerApp().run()