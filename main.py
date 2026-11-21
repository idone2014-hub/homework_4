import os
import subprocess
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

GITHUB_URL = "https://github.com/idone2014-hub/python-ex2"


def open_file_cross_platform(file_path):
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", file_path])
    else:
        subprocess.Popen(["xdg-open", file_path])


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        title = QLabel("Student Grade Correction")
        title.setObjectName("aboutTitle")

        description = QLabel(
            f'A tool for correcting student grades.<br>'
            f'<a href="{GITHUB_URL}">Visit the GitHub repository</a>'
        )
        description.setOpenExternalLinks(True)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(close_button)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.setWindowTitle("Student Grade Correction")
        self.resize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        heading = QLabel("Student Grade Correction")
        heading.setObjectName("heading")
        subtitle = QLabel("Load a grades file, apply bonus points, and update it.")
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(heading)
        main_layout.addWidget(subtitle)

        toolbar = QHBoxLayout()
        self.load_button = QPushButton("Load Grades File")
        self.load_button.setObjectName("loadButton")
        self.load_button.clicked.connect(self.open_grades_file)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)

        toolbar.addWidget(self.load_button)
        toolbar.addStretch()
        toolbar.addWidget(self.about_button)
        main_layout.addLayout(toolbar)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        main_layout.addWidget(self.table)

        footer = QHBoxLayout()
        bonus_label = QLabel("Bonus points:")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 100)
        self.bonus_input.editingFinished.connect(self.apply_bonus)

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.update_file)

        footer.addWidget(bonus_label)
        footer.addWidget(self.bonus_input)
        footer.addStretch()
        footer.addWidget(self.update_button)
        main_layout.addLayout(footer)

        central_widget.setLayout(main_layout)

    def open_grades_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Grades File",
            "",
            "CSV files (*.csv)"
        )
        if file_path:
            self.selected_file = file_path
            self.load_file(file_path)

    def show_about(self):
        dialog = AboutDialog()
        dialog.exec()

    def load_file(self, file_path):
        pass

    def update_table(self):
        pass

    def apply_bonus(self):
        pass

    def update_file(self):
        pass


def main():
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()