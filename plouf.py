
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QAction, QLineEdit, QTextEdit, QLabel, QComboBox, QMessageBox,
                              QWidget, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QDialog, QSplitter )
from PyQt5.QtCore import Qt
from sys import argv, exit
import requests


def ErrorMessage(msg: str):
    QMessageBox.critical(window.w, 'Error', msg)


def StrToDict(string: str):
    pairs = string.split('\n')
    dic = {}
    for pair in pairs:
        key, value = pair.split(':')
        key = key.strip()
        value = value.strip()
        dic[key] = value
    return dic


def DictToStr(dic: dict):
    string = ''
    for key in dic:
        string += str(key) + ': ' + str(dic[key]) + '\n'
    return string


class Response(QDialog):
    def __init__(self, headers: str, text: str):
        super().__init__(window)
        self.setWindowTitle('Response')
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |Qt.WindowSystemMenuHint |
                            Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setMinimumSize(600, 450)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel('Response headers', self))
        
        self.headers = QTextEdit(self)
        self.headers.setReadOnly(True)
        self.headers.setText(headers)
        layout.addWidget(self.headers)
        
        layout.addWidget(QLabel('Response text', self))
        
        self.text = QTextEdit(self)
        self.text.setAcceptRichText(False)
        self.text.setReadOnly(True)
        self.text.setPlainText(text)
        layout.addWidget(self.text)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close = QPushButton('Close', self)
        close.clicked.connect(self.accept)
        btn_layout.addWidget(close)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel('Url', self))
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Url address')
        self.url_input.setText('https://google.com')
        url_layout.addWidget(self.url_input)
        
        url_layout.addSpacing(20)
        
        self.method_menu = QComboBox(self)
        self.method_menu.setMinimumWidth(85)
        self.method_menu.addItems(['GET', 'POST'])
        url_layout.addWidget(QLabel('Method', self))
        url_layout.addWidget(self.method_menu)
        
        layout.addLayout(url_layout)
        
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(QLabel('Payload'))
        
        self.payload_input = QLineEdit(self)
        self.payload_input.setPlaceholderText('POST request payload')
        payload_layout.addWidget(self.payload_input)
        
        layout.addSpacing(8)
        layout.addLayout(payload_layout)
        
        layout.addWidget(QLabel('Headers', self))
        
        self.headers_input = QTextEdit(self)
        self.headers_input.setAcceptRichText(False)
        layout.addWidget(self.headers_input)
        
        self.send_btn = QPushButton('Send', self)
        self.send_btn.clicked.connect(self.Send)
        layout.addWidget(self.send_btn)
        
        self.setLayout(layout)
    
    def Send(self):
        url = self.url_input.text()
        if not url:
            ErrorMessage('Url field is empty.')
            return
        if url == '127.0.0.1':
            url = 'http://' + url
        
        headers = self.headers_input.toPlainText()
        if headers:
            headers = StrToDict(headers)
        else:
            headers = {}
        
        method = self.method_menu.currentText()
        
        try:
            if method == 'GET':
                request = requests.get(url, headers=headers)
            
        except Exception as error:
            ErrorMessage('An error occured during the request :\n'+str(error))
            return
        
        response = Response(DictToStr(request.headers), request.text)
        response.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Plouf 2.0')
        w, h = 650, 400
        self.setGeometry(int(SCREEN_SIZE[0]/2 - w/2), int(SCREEN_SIZE[1]/2 - h/2), w, h)
        self.setupActions()
        self.setupToolbar()
        
        self.w = MainWidget(self)
        self.setCentralWidget(self.w)
    
    def setupActions(self):
        self.ac_about = QAction('&About', shortcut='Alt+a')
    
    def setupToolbar(self):
        toolbar = self.addToolBar('toolbar')
        toolbar.setMovable(False)
        toolbar.addAction(self.ac_about)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(argv)
    app.setStyleSheet("QLabel, QPushButton, QAction, QLineEdit, QTextEdit, QComboBox, QToolBar { font-size: 9pt; }")
    
    screen = QDesktopWidget().screenGeometry()
    SCREEN_SIZE = (screen.width(), screen.height())
    
    window = Window()
    window.show()
    
    exit(app.exec())
