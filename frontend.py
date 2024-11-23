from typing import Literal, TypedDict, Union
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QCheckBox,
)
import sys
from images import write_script
from functools import reduce
from replacements import REPLACEMENTS, CLOCKTOWER_CON_REPLACEMENTS


class GlobalState(TypedDict):
    json: str | None
    png: str | None
    chosenArea: str
    replacements: dict[str, list[str]]
    replacementsClicked: bool


STATE: GlobalState = {
    "json": None,
    "png": None,
    "chosenArea": "./",
    "replacements": REPLACEMENTS,
    "replacementsClicked": False,
}


class FileButton(QPushButton):
    def dialog(self):
        value = QFileDialog.getOpenFileName(
            self.parentWidget(),
            "TEST",
            STATE["chosenArea"],
            f"{self.file_type} (*.{self.file_type})",
        )
        STATE[self.file_type] = value[0]
        STATE["chosenArea"] = reduce(
            lambda a, b: a + "/" + b, value[0].split("/")[0:-1]
        )
        self.setText(f"{self.file_type}: {value[0]}")
        print(STATE)

    def __init__(
        self,
        parent: QWidget | None,
        file_type: Literal["png", "json"] = "png",
        y: int = 0,
    ) -> None:
        super().__init__(parent)
        self.setGeometry(50, y, 500, 40)
        self.file_type: Literal["png", "json"] = file_type
        self.setText(f"Please select {file_type}")
        self.clicked.connect(self.dialog)


def toggleReplacements(b: bool):
    global STATE
    if STATE["replacementsClicked"]:
        STATE["replacements"] = REPLACEMENTS
        STATE["replacementsClicked"] = False
    else:
        STATE["replacements"] = CLOCKTOWER_CON_REPLACEMENTS
        STATE["replacementsClicked"] = True
    print(STATE)


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400, 400, 700, 300)
    win.setWindowTitle("Clocktower Replacements")
    layout = QVBoxLayout()

    jsonButton = FileButton(None, "json", y=20)
    pngButton = FileButton(None, "png", y=70)
    replacementTypeButton = QCheckBox(None, y=10, x=50)
    replacementTypeButton.clicked.connect(toggleReplacements)
    replacementTypeButton.setText("Use only Clocktower Con onwards replacements?")
    submitButton = QPushButton(win)
    submitButton.setText("SUBMIT")
    submitButton.setGeometry(200, 150, 100, 30)
    submitButton.clicked.connect(
        lambda x: write_script(STATE["json"], STATE["png"], REPLACEMENTS)
    )

    layout.addWidget(jsonButton)
    layout.addWidget(pngButton)
    layout.addWidget(submitButton)
    layout.addWidget(replacementTypeButton)

    widget = QWidget()
    widget.setLayout(layout)
    win.setCentralWidget(widget)
    win.show()
    sys.exit(app.exec_())


window()
