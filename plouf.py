
from PyQt5.QtWidgets import ( QApplication, QMainWindow, QAction, QLineEdit, QTextEdit, QLabel, QWidget, QDialog, QSplitter,
                              QComboBox, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QMessageBox, QFileDialog )
from PyQt5.QtCore import Qt
from sys import argv, exit
import requests


def ErrorMessage(msg: str):
    QMessageBox.critical(window.w, 'Error', msg)


def StrToDict(string: str):
    pairs = string.split('\n')
    dic = {}
    for pair in pairs:
        if not ':' in pair:
            ErrorMessage('Syntax Error : '+pair)
            continue
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
    def __init__(self, headers, text):
        super().__init__(window)
        self.setWindowTitle('Response')
        self.setWindowFlags( Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |Qt.WindowSystemMenuHint |
                             Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint )
        self.setMinimumSize(600, 475)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        splitter = QSplitter(Qt.Vertical, self)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self.newWidget('Headers', headers))
        splitter.addWidget(self.newWidget('Response', text))
        layout.addWidget(splitter)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_headers = QPushButton('Save Headers', self)
        save_headers.setMinimumWidth(125)
        save_headers.clicked.connect(lambda: self.toFile(headers))
        btn_layout.addWidget(save_headers)
        
        save_text = QPushButton('Save Response', self)
        save_text.setMinimumWidth(135)
        save_text.clicked.connect(lambda: self.toFile(text))
        btn_layout.addWidget(save_text)
        
        close = QPushButton('Close', self)
        close.clicked.connect(self.accept)
        close.setFocus(True)
        btn_layout.addWidget(close)
        
        layout.addLayout(btn_layout)
    
    def newWidget(self, title, text):
        widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title, widget))
        edit = QTextEdit(widget)
        edit.setReadOnly(True)
        edit.setLineWrapMode(False)
        edit.setPlainText(text)
        layout.addWidget(edit)
        widget.setLayout(layout)
        return widget
    
    def toFile(self, text):
        path = QFileDialog.getSaveFileName(self, None, None, 'Text files (*.txt);;All Files (*)')[0]
        if path:
            with open(path, 'w') as file:
                file.write(text)


class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
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
        
        splitter = QSplitter(Qt.Vertical, self)
        splitter.setChildrenCollapsible(False)
        
        widget1, self.payload_input = self.newTextEdit('Data', 'data to send')
        splitter.addWidget(widget1)
        
        widget2, self.headers_input = self.newTextEdit('Headers', 'http request headers')
        splitter.addWidget(widget2)
        self.headers_input.setPlainText('User-Agent: Mozilla/5.0 Gecko/41.0 Firefox/41.0\nAccept: */*')
        
        splitter.setSizes((0, 300))
        layout.addWidget(splitter)
        
        self.send_btn = QPushButton('Send', self)
        self.send_btn.clicked.connect(self.Send)
        layout.addWidget(self.send_btn)
    
    def newTextEdit(self, title, placeholder):
        widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title, widget))
        edit = QTextEdit(widget)
        edit.setAcceptRichText(False)
        edit.setLineWrapMode(False)
        edit.setPlaceholderText(placeholder)
        layout.addWidget(edit)
        widget.setLayout(layout)
        return widget, edit
    
    def get(self, edit):
        data = edit.toPlainText()
        if data:
            return StrToDict(data)
        else:
            return {}
    
    def Send(self):
        url = self.url_input.text()
        if not url:
            ErrorMessage('Url field is empty.')
            return
        if url == '127.0.0.1':
            url = 'http://' + url
        
        method = self.method_menu.currentText()
        redirect = window.ac_redirect.isChecked()
        headers = self.get(self.headers_input)
        
        if method != 'GET':
            data = self.get(self.payload_input)
        
        try:
            if method == 'GET':
                request = requests.get(url, headers=headers, allow_redirects=redirect)
            elif method == 'POST':
                request = requests.post(url, data=data, headers=headers, allow_redirects=redirect)
            
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
        self.ac_redirect = QAction('&Redirect requests', shortcut='Ctrl+r', checkable=True, checked=True)
        self.ac_about = QAction('&About', shortcut='Alt+a')
        self.ac_doc = QAction('&Documentation', shortcut='Alt+d')
    
    def setupToolbar(self):
        toolbar = self.menuBar()
        options = toolbar.addMenu('&Options')
        options.addAction(self.ac_redirect)
        help = toolbar.addMenu('&Help')
        help.addAction(self.ac_about)
        help.addAction(self.ac_doc)
    
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
