from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class HexValidator(QRegExpValidator):
    def __init__(self):
        super().__init__(QRegExp(r'^([0-9A-Fa-f]{0,2})?$'))
def load_custom_font():
    # Load custom font
    fontId = QFontDatabase.addApplicationFont("assets/fonts/NeueMachina-Ultrabold.otf")
    if fontId == -1:
        print("Failed to load font. Check the font path.")
        return None

    fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
    return QFont(fontFamilies[0], 12)  # Use the first family font and set size

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def center(self):
        qr = self.frameGeometry()  # Get the frame geometry of the main window
        cp = QDesktopWidget().availableGeometry().center()  # Find the center point of the screen
        qr.moveCenter(cp)  # Set the center of the frame to the center of the screen
        self.move(qr.topLeft())  # Move the top-left point of the window to the top-left of the qr rectangle

    
    def initUI(self):
        self.setWindowTitle('mice ai')
        self.setGeometry(0 , 0, 500, 450)  # x, y, width, height
        self.setStyleSheet('QWidget{ background:#000;color:#fff; }')
        
        self.center()
        v_layout = QVBoxLayout()
        # Setup the GIF animation
        self.gif_label = QLabel(self)
        self.movie = QMovie("assets/init.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Create line edits for hex input
        self.entries = []

        h_layout = QHBoxLayout()
        for i in range(4):
            entry = QLineEdit(self)
            entry.setValidator(HexValidator())
            entry.setFixedWidth(80)
            entry.setStyleSheet("outline:none;border:none;border-bottom:2px solid #fff;text-align:center;align-items:center;")
            entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.entries.append(entry)
            h_layout.addWidget(entry)
        
        # Submit button
        self.submit_btn = QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.on_submit)

        v_layout.addWidget(self.gif_label)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.submit_btn)
        
        # Set layout
        self.setLayout(v_layout)

        # Bind the return key to the submit function
        self.submit_btn.setShortcut("Return")

        # Bind Ctrl+D to close the application
        self.shortcut_close = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut_close.activated.connect(self.close_grace)
    
    def on_submit(self):
        values = [entry.text().upper() for entry in self.entries]
        if all([x for x in values]):
            QMessageBox.information(self, 'Success', 'All values are valid hex: ' + ', '.join(values))
        else:
            QMessageBox.warning(self, 'Error', 'All are not valid hex\nEnter only valid hex')
    
    def close_grace(self):
        reply = QMessageBox.question(self, 'Exit?', 'Do you really want to exit???', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    customFont = load_custom_font()
    if customFont:
        app.setFont(customFont)
    else:
        sys.exit("Failed to load the custom font.")  # Exit if no font is loaded

    ex = App()
    ex.show()
    sys.exit(app.exec_())
