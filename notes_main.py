from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
import json

app = QApplication([])

pencerem = QWidget()
pencerem.setWindowTitle("Akıllı Notlar")
pencerem.resize(900,600)
pencerem.show()

list_notes_label= QLabel("Notların Listesi")
list_notes = QListWidget()

button_note_create=QPushButton("Not Oluştur")
button_note_del = QPushButton("Notu Sil")
button_not_save = QPushButton("Notu Kaydet")

list_tags_label = QLabel("Etiket Listesi")
list_tags = QListWidget()

field_tag = QLineEdit('')
field_tag.setPlaceholderText("Etiket adını giriniz...")

button_tag_add = QPushButton("Nota Ekle")
button_tag_del = QPushButton("Nottan Çıkar")
button_tag_search = QPushButton("Notları etikete göre ara")

field_text = QTextEdit()

# Widget Konumlandırma
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()

col_1.addWidget(field_text)
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_not_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)

pencerem.setLayout(layout_notes)

'''
key    : value
school : okul
'''

notes = {
    "Hoş geldiniz!" : {
        "metin" : "Bu dünyanın en iyi not alma uygulamasi!",
        "etiket" : ["iyilik", "talimat"]
    }
}

with open("notes_data.json", "w", encoding="utf-8") as file:
    json.dump(notes, file,ensure_ascii = False,indent=4)


with open ("notes_data.json","r",encoding="utf-8") as dosya_2:
    data = json.load(dosya_2)
#print(notes)
list_notes.addItems(data)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(data[key]["metin"])
    list_tags.clear()
    list_tags.addItems(data[key]["etiket"])
    
#Not ekleme Fonksiyonu
def add_note():
    note_name, result = QInputDialog.getText(pencerem,
        "Not Ekle","Not Başlığı :")
    if result == True and note_name !="":
        data[note_name] = {
            "metin" : "",
            "etiket" :[]
        }
        list_notes.addItem(note_name)
    else:
        print("Not Adı boş bırakılamaz")

# Notu kaydetme fonksiyonu
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        data[key]["metin"] = field_text.toPlainText()
        with open("notes_data.json","w",encoding="utf-8") as dosya:
            json.dump(data,dosya,ensure_ascii=False, indent=4)
    else:
        print("Kaydedilecek not seçili değil.")

# Notu silme Fpnkisyonu
def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del data[key]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(data)
        with open("notes_data.json","w",encoding="utf-8") as dosya:
            json.dump(data,dosya,ensure_ascii=False, indent=4)
    else:
        print("Silinecek not seçili değil.")

#Etiket Ekleme Fonk.
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        # key = Benim Notum
        etiket = field_tag.text()
        if not etiket in data[key]["etiket"]:
            data[key]["etiket"].append(etiket)
            list_tags.addItem(etiket)
            field_tag.clear()
            with open("notes_data.json","w",encoding="utf-8") as dosya:
                json.dump(data,dosya,ensure_ascii=False, indent=4)
    else:
        print("Etiket eklenecek not seçili değil !")
        
print("Değişiklik")

# Etiketleri silen fonskiyon
def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        silinecek_etiket = list_tags.selectedItems()[0].text()
        data[key]["etiket"].remove(silinecek_etiket)
        list_tags.clear()
        list_tags.addItems(data[key]["etiket"])
        with open("notes_data.json","w",encoding="utf-8") as dosya:
            json.dump(data,dosya,ensure_ascii=False, indent=4)
    else:
        print("Etiketi silincek not seçili değil !")

# etikete göre arama
def search_tag():
    aranacak_etiket = field_tag.text() 
    if aranacak_etiket != "" and button_tag_search.text() == "Notları etikete göre ara":
        
        aranan_not = {}
        for notlar in data:
            if aranacak_etiket in data[notlar]["etiket"]:
                aranan_not[notlar] = data[notlar]
        button_tag_search.setText("Aramayı Sıfırla")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(aranan_not)
    elif button_tag_search.text() == "Aramayı Sıfırla":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(data)
        button_tag_search.setText("Notları etikete göre ara")
    else:
        print("Lütfen aramak istediğiniz etiketin adını yazın.")


list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_not_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

app.exec_()
