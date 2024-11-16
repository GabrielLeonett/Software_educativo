import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QPushButton, QLineEdit, QMessageBox, QRadioButton, QButtonGroup, QListWidget
)
from PyQt6.QtGui import QPixmap
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aprende Redes Básicas")
        self.setGeometry(100, 100, 400, 500)  # Aumentamos el tamaño de la ventana para acomodar la lista de puntuaciones

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLabel {
                color: #000000;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
                font-family: Arial;
                font-size: 14px;
                border: 1px solid #000000;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-family: Arial;
                font-size: 14px;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QRadioButton {
                color: #000000;
                font-family: Arial;
                font-size: 14px;
            }
        """)

        self.score = 0
        self.high_scores = []

        # Cargar puntuaciones más altas del archivo
        self.load_high_scores()

        self.current_question = 0
        self.questions = [
            {"image": os.path.join(self.base_path, "WAN.png"), "correct": "WAN", "options": ["LAN", "WAN", "MAN"]},
            {"image": os.path.join(self.base_path, "LAN.png"), "correct": "LAN", "options": ["LAN", "WAN", "MAN"]},
            {"image": os.path.join(self.base_path, "IPV4.jpg"), "correct": "IPv4", "options": ["IPv4", "IPv6"]},
            {"image": os.path.join(self.base_path, "IPV6.jpg"), "correct": "IPv6", "options": ["IPv4", "IPv6"]},
            {"image": os.path.join(self.base_path, "HARDWARE.jpg"), "correct": "Hardware", "options": ["Hardware", "Software"]},
            {"image": os.path.join(self.base_path, "SOFTWARE.jpg"), "correct": "Software", "options": ["Hardware", "Software"]},
            {"image": os.path.join(self.base_path, "REDES.png"), "correct": "Redes", "options": ["Redes", "Base de Datos"]},
            {"image": os.path.join(self.base_path, "OS.jpg"), "correct": "Sistema Operativo", "options": ["Sistema Operativo", "Aplicación"]},
            {"image": os.path.join(self.base_path, "NUBE.png"), "correct": "Nube", "options": ["Nube", "Almacenamiento Local"]},
            {"image": os.path.join(self.base_path, "DB.png"), "correct": "Base de Datos", "options": ["Base de Datos", "Archivo"]},
            {"image": os.path.join(self.base_path, "IPV4.jpg"), "correct": "IP", "options": ["IP", "MAC"]},
            {"image": os.path.join(self.base_path, "ALGORITMO.png"), "correct": "Algoritmo", "options": ["Algoritmo", "Programa"]},
            {"image": os.path.join(self.base_path, "CYBER_SEGURITY.jpg"), "correct": "Seguridad Informática", "options": ["Seguridad Informática", "Desarrollo Web"]},
            {"image": os.path.join(self.base_path, "CODIGO_FUENTE.png"), "correct": "Código Fuente", "options": ["Código Fuente", "Lenguaje de Máquina"]}
        ]

        self.label = QLabel("Por favor, ingrese su nombre:")
        self.name_input = QLineEdit(self)
        self.submit_name_button = QPushButton("Enviar Nombre", self)
        self.submit_name_button.clicked.connect(self.submit_name)

        self.image_label = QLabel()
        self.image_label.setVisible(False)

        self.question_label = QLabel("¿Qué se muestra en la imagen?")
        self.question_label.setVisible(False)

        self.option1 = QRadioButton()
        self.option2 = QRadioButton()
        self.option3 = QRadioButton()

        self.option1.setVisible(False)
        self.option2.setVisible(False)
        self.option3.setVisible(False)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.option1)
        self.button_group.addButton(self.option2)
        self.button_group.addButton(self.option3)

        self.submit_answer_button = QPushButton("Enviar Respuesta", self)
        self.submit_answer_button.setVisible(False)
        self.submit_answer_button.clicked.connect(self.check_answer)

        self.score_list = QListWidget()
        self.score_list.setVisible(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.submit_name_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.option1)
        self.layout.addWidget(self.option2)
        self.layout.addWidget(self.option3)
        self.layout.addWidget(self.submit_answer_button)
        self.layout.addWidget(self.score_list)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def submit_name(self):
        self.name = self.name_input.text()
        if self.name:
            QMessageBox.information(self, "Hola", f"¡Hola, {self.name}! Bienvenido a Aprende Redes Básicas.")
            self.label.setVisible(False)
            self.name_input.setVisible(False)
            self.submit_name_button.setVisible(False)
            self.show_quiz()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese su nombre.")

    def show_quiz(self):
        # Mostrar la imagen y las preguntas
        question = self.questions[self.current_question]
        self.image_label.setPixmap(QPixmap(question["image"]))
        self.question_label.setVisible(True)
        self.image_label.setVisible(True)

        self.option1.setText(question["options"][0])
        self.option2.setText(question["options"][1])
        if len(question["options"]) > 2:
            self.option3.setText(question["options"][2])
            self.option3.setVisible(True)
        else:
            self.option3.setVisible(False)

        self.option1.setVisible(True)
        self.option2.setVisible(True)
        self.submit_answer_button.setVisible(True)

    def check_answer(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            answer = selected_button.text()
            question = self.questions[self.current_question]
            if answer == question["correct"]:
                self.score += 1
                QMessageBox.information(self, "Correcto", "¡Respuesta correcta!")
            else:
                QMessageBox.warning(self, "Incorrecto", "Respuesta incorrecta. Pasando a la siguiente pregunta.")
            self.clear_quiz()
            self.current_question += 1
            if self.current_question < len(self.questions):
                self.show_quiz()
            else:
                self.show_final_message()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una opción.")

    def clear_quiz(self):
        # Ocultar la imagen y las preguntas anteriores
        self.image_label.setVisible(False)
        self.question_label.setVisible(False)
        self.option1.setVisible(False)
        self.option2.setVisible(False)
        self.option3.setVisible(False)
        self.submit_answer_button.setVisible(False)

    def show_final_message(self):
        self.high_scores.append((self.name, self.score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)  # Ordenar por puntuación, de mayor a menor
        self.save_high_scores()
        self.update_score_list()
        QMessageBox.information(self, "Felicitaciones", f"¡Felicidades por completar el programa! Puntuación total: {self.score} preguntas correctas.")
        self.close()  # Cerrar el programa

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                for line in file:
                    name, score = line.strip().split(", ")
                    self.high_scores.append((name, int(score)))
        except FileNotFoundError:
            pass

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for name, score in self.high_scores:
                file.write(f"{name}, {score}\n")

    def update_score_list(self):
        self.score_list.clear()
        for name, score in self.high_scores:
            self.score_list.addItem(f"{name}: {score} preguntas correctas")

def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
