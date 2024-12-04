from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import test_code as pack
import ip_cam as ext_cam

def to_ip(values):
    x = [str(int(y,16)) for y in values]
    ip ='.'.join(x)
    return 'http://'+ip+':81/stream'

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
        self.setWindowTitle('MICE AI')
        self.setGeometry(0 , 0, 500, 450)  # x, y, width, height
        self.setStyleSheet('QWidget{ background:#000;color:#fff; }')
        
        self.center()
        self.v_layout = QVBoxLayout()
        # Setup the GIF animation
        self.gif_label = QLabel(self)
        self.movie = QMovie("assets/init.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        self.gif_label_small = QLabel(self)
        self.movie_small = QMovie("assets/small.gif")
        self.gif_label_small.setMovie(self.movie_small)
        





        # Create line edits for hex input
        self.entries = []

        self.h_layout = QHBoxLayout()
        for i in range(4):
            entry = QLineEdit(self)
            entry.setValidator(HexValidator())
            entry.setFixedWidth(80)
            entry.setStyleSheet("outline:none;border:none;border-bottom:2px solid #fff;text-align:center;align-items:center;")
            entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.entries.append(entry)
            self.h_layout.addWidget(entry)
        
        # Submit button
        self.submit_btn = QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.on_submit)
        # Close button
        self.close_btn = QPushButton('Terminate', self)
        self.close_btn.clicked.connect(self.close_grace)

        self.v_layout.addWidget(self.gif_label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.submit_btn)
        
        # Set layout
        self.setLayout(self.v_layout)


        # Bind the return key to the submit function
        self.submit_btn.setShortcut("Return")

        # Bind Ctrl+D to close the application
        self.shortcut_close = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcut_close.activated.connect(self.close_grace)
        self.show()

    def on_submit(self):
        values = [entry.text().upper() for entry in self.entries]
        if all([x for x in values]):
            # QMessageBox.information(self, 'Success', 'All values are valid hex: ' + ', '.join(values))
            try:
                ip_is_zero = sum([int(v,16) for v in values])==0 # it will definite give error for valid hex values of ff
            except ValueError:
                ip_is_zero = False
            ip = to_ip(values)
            print(ip)
            
            self.movie_small.start()
            self.v_layout.addWidget(self.gif_label_small)
            self.v_layout.addWidget(self.close_btn)
            self.submit_btn.close()
            for i in self.entries:
                print(i)
                i.close()
            self.gif_label.close()

            self.setGeometry(0,0,400,200)
            self.updateGeometry()
            self.center()

            if ip_is_zero:
                pack.do_the_thing()
            else:
                ext_cam.do_the_thing(ip)
            
        else:
            QMessageBox.warning(self, 'Error', 'All are not valid hex\nEnter only valid hex')

    
    def close_grace(self):
        reply = QMessageBox.question(self, 'Exit?', 'Do you really want to exit???', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            ext_cam.running = False  
            pack.running = False
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
