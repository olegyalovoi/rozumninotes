from ui import Ui_MainWindow

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

import json

app = QApplication([])
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

notes = {}

def add_note():
    note_name, ok = QInputDialog.getText(MainWindow, "Додати замітку", "Назва замітки: ")
    if ok and note_name !="":
        notes[note_name] = {"текст":"", "теги":[]}
        ui.listWidget.addItem(note_name)
        ui.listWidget_2.clear()
        print(notes)

def show_note():
    key = ui.listWidget.selectedItems()[0].text()
    ui.textEdit.setText(notes[key]["текст"])
    ui.listWidget_2.clear()
    ui.listWidget_2.addItems(notes[key]["теги"])


def save_note():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        notes[key]["text"] = ui.textEdit.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii = False)
        print("Замітка для збереження не вибрана!")


def del_note():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        del notes[key]
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.textEdit.clear()
        ui.listWidget.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes,file,sort_keys = True, ensure_ascii=False)
        print(notes)
    else:
        print("Неправильно,ви не вибрали текст")


def add_tag():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        tag = ui.lineEdit.text()
        if tag and tag not in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            ui.listWidget_2.addItem(tag)
            ui.lineEdit.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Не вибрали замітку")

def del_tag():
    if ui.listWidget_2.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        tag = ui.listWidget_2.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        ui.listWidget_2.clear()
        ui.lineWidget_2.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Тег не обраний!")

def search_tag():
    tag = ui.lineEdit.text()
    if ui.pushButton_6.text() == "Шукати по тегу" and tag:
        notes_filtered = {note: notes[note] for note in notes
                          if tag in notes[note]["теги"]} 
           
        ui.pushButton_6.setText("Скинути пошук")
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.listWidget.addItems(notes_filtered)
    elif ui.pushButton_6.text() == "Скинути пошук":
        ui.lineEdit.clear()
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.listWidget.addItems(notes)
        ui.pushButton_6.setText("Шукати по тегу")



ui.pushButton.clicked.connect(add_note)
ui.listWidget.itemClicked.connect(show_note)
ui.pushButton_2.clicked.connect(del_note)
ui.pushButton_3.clicked.connect(save_note)

ui.pushButton_4.clicked.connect(add_tag)
ui.pushButton_5.clicked.connect(del_tag)
ui.pushButton_6.clicked.connect(search_tag)
try:
    with open("notes_data.json","r") as file:
        notes = json.load(file)
        ui.listWidget.addItems(notes)
except FileNotFoundError:
    notes = {}

MainWindow.show()
app.exec()



