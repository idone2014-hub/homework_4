import os
import subprocess
import sys
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

GITHUB_URL = "https://github.com/idone2014-hub/homework_4/blob/master/main.py"


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
            f'<a href="{GITHUB_URL}">Visit the GitHub repository</a>')
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
        self.resize(980, 650)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
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
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 280)
        self.table.setColumnWidth(2, 280)

        for row in range(50):
            self.table.setRowHeight(row, 38)

        self.table.setFixedWidth(828)

        table_layout = QHBoxLayout()
        table_layout.addStretch()
        table_layout.addWidget(self.table)
        table_layout.addStretch()
        main_layout.addLayout(table_layout)

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
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

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
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []

        with open(file_path, "r") as f:
            lines = f.readlines()

        self.file_header = lines[0]

        for line in lines[1:]:
            parts = line.strip().split(",")
            student_id = parts[0]
            grade = int(parts[1])  # אם הציונים בקובץ עשרוניים (כמו 85.5), החלף int ב-float

            self.student_ids.append(student_id)
            self.original_grades.append(grade)
            self.corrected_grades.append(grade)

        self.update_table()

    def update_table(self):
        for row in range(len(self.student_ids)):
            self.table.setItem(row, 0, QTableWidgetItem(str(self.student_ids[row])))
            self.table.setItem(row, 1, QTableWidgetItem(str(self.original_grades[row])))
            self.table.setItem(row, 2, QTableWidgetItem(str(self.corrected_grades[row])))

    def apply_bonus(self):
        bonus = self.bonus_input.value()
        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if self.selected_file == '':
            return

        with open(self.selected_file, "w") as f:
            f.write(self.file_header)
            for i in range(len(self.student_ids)):
                f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

        open_file_cross_platform(self.selected_file)

def main():
    app = QApplication(sys.argv)
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()