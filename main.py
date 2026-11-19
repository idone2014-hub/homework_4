import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


GITHUB_URL = "https://github.com/idone2014-hub/python-ex2"


def open_file_cross_platform(file_path):
    """Open a file using the operating system's default application."""
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", file_path])
    else:
        subprocess.Popen(["xdg-open", file_path])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.setWindowTitle("Student Grade Correction")
        self.resize(1000, 700)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        heading = QLabel("Student Grade Correction")
        heading.setObjectName("heading")
        subtitle = QLabel("Load a grades file, apply bonus points, and update it.")
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(heading)
        main_layout.addWidget(subtitle)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.load_button = QPushButton("Load Grades File")
        self.load_button.setObjectName("loadButton")
        self.load_button.clicked.connect(self.open_grades_file)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.show_about)

        toolbar.addWidget(self.load_button)
        toolbar.addStretch()
        toolbar.addWidget(self.about_button)
        main_layout.addLayout(toolbar)

        self.table = QTableWidget(50, 3)
        self.table.setObjectName("gradeTable")
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            0, self.table.horizontalHeader().ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, self.table.horizontalHeader().ResizeMode.Stretch
        )
        main_layout.addWidget(self.table, stretch=1)

        footer = QHBoxLayout()
        footer.setSpacing(10)

        bonus_label = QLabel("Bonus points")
        self.bonus_input = QSpinBox()
        self.bonus_input.setRange(0, 99)
        self.bonus_input.setObjectName("bonusInput")
        self.bonus_input.editingFinished.connect(self.apply_bonus)

        self.update_button = QPushButton("Update File")
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.update_file)

        footer.addWidget(bonus_label)
        footer.addWidget(self.bonus_input)
        footer.addStretch()
        footer.addWidget(self.update_button)
        main_layout.addLayout(footer)

    def open_grades_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Grades File",
            "",
            "CSV files (*.csv)",
        )
        if file_path:
            self.selected_file = file_path
            self.load_file(file_path)

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About")
        dialog.setObjectName("aboutDialog")
        dialog.setFixedWidth(420)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Student Grade Correction")
        title.setObjectName("aboutTitle")

        description = QLabel(
            "A desktop tool for correcting student grades.\n"
            f'<a href="{GITHUB_URL}">Visit the GitHub repository</a>'
        )
        description.setObjectName("aboutDescription")
        description.setOpenExternalLinks(True)
        description.setTextFormat(Qt.TextFormat.RichText)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

        dialog.exec()

    def load_file(self, file_path):
        """Load a grades file."""
        pass

    def update_table(self):
        """Refresh the grades table."""
        pass

    def apply_bonus(self):
        """Apply bonus points to grades."""
        pass

    def update_file(self):
        """Save the corrected grades to the selected file."""
        pass


def main():
    app = QApplication(sys.argv)
    stylesheet_path = Path(__file__).with_name("style.qss")
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()