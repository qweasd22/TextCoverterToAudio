import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtMultimedia import QSound
import requests
import pyttsx3
from bs4 import BeautifulSoup

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текст конвертер")
        self.resize(800, 600)
        self.create_ui()

    def create_ui(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        self.text_input = QtWidgets.QLineEdit()
        layout.addWidget(self.text_input)

        load_local_doc_button = QtWidgets.QPushButton("Загрузить документ с компьютера")
        load_remote_doc_button = QtWidgets.QPushButton("Загрузить документ по ссылке")
        convert_button = QtWidgets.QPushButton("Конвертировать")
        save_button = QtWidgets.QPushButton("Сохранить в файл")
        cancel_button = QtWidgets.QPushButton("Закончить конвертацию")
        layout.addWidget(load_local_doc_button)
        layout.addWidget(load_remote_doc_button)
        layout.addWidget(convert_button)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
        load_local_doc_button.clicked.connect(self.load_local_document)
        load_remote_doc_button.clicked.connect(self.load_remote_document)
        convert_button.clicked.connect(self.convert_text_to_speech)
        save_button.clicked.connect(self.save_text_to_file)
        cancel_button.clicked.connect(self.cancel_conversion)
        

        self.setCentralWidget(central_widget)

    
    def load_local_document(self):
        file_dialog = QtWidgets.QFileDialog(self)
        selected_files = file_dialog.getOpenFileNames(
            directory="", filter="All files (*)"
        )[0]
        if len(selected_files) > 0:
            with open(selected_files[0], "r", encoding='utf-8') as f:
                content = f.read()
                self.text_input.setText(content)

    def load_remote_document(self):
        url = QtWidgets.QInputDialog.getText(self, "Enter URL", "URL:")[0]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.find_all(string=True)
                cleaned_text = []
                for t in text:
                    if t.parent.name not in ['style', 'script', '[document]', 'head', 'title']:
                        cleaned_text.append(t)
                self.text_input.setText('\n'.join(cleaned_text))
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to load document.")

    def convert_text_to_speech(self,):
        engine = pyttsx3.init()
        text = self.text_input.text()
        engine.say(text)
        engine.runAndWait()

    def cancel_conversion(self):
        engine = pyttsx3.init()
        engine.stop()

    def save_text_to_file(self, text):
        engeine = pyttsx3.init()
        text = self.text_input.text()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        engeine.save_to_file(text, f'{directory}/audio.mp3')
        engeine.runAndWait()
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())