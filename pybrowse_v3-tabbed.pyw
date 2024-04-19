import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *  
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def close_tab(self, index):
        self.parent().removeTab(index)

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        size.setWidth(max(size.width(), 150))  
        return size


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pybrowse v3 - PYTHON")
        self.setGeometry(0, 0, 1300, 1000)  

        self.tabs = QTabWidget()
        self.tabs.setTabBar(CustomTabBar(self))
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl("https://www.qwant.com"))  

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        navtb.addAction(QAction('Back', self, triggered=lambda: self.tabs.currentWidget().back()))
        navtb.addAction(QAction('Forward', self, triggered=lambda: self.tabs.currentWidget().forward()))
        navtb.addAction(QAction('Reload', self, triggered=lambda: self.tabs.currentWidget().reload()))
        navtb.addWidget(self.url_bar)
        navtb.addAction(QAction('New Tab', self, triggered=self.add_new_tab_action))

        self.new_tab_shortcut = QShortcut(QKeySequence(Qt.AltModifier + Qt.Key_C), self)
        self.new_tab_shortcut.activated.connect(self.add_new_tab_action)

        self.webpage = None

    def add_new_tab(self, qurl):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.titleChanged.connect(lambda title, index=self.tabs.count(): self.update_tab_title(index, title))
        browser.page().profile().downloadRequested.connect(self.download_requested)

        i = self.tabs.addTab(browser, self.format_tab_name("New Tab"))
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

    def tab_open_doubleclick(self, i):
        if i == -1:  
            self.add_new_tab(QUrl('https://www.qwant.com'))

    def add_new_tab_action(self):
        self.add_new_tab(QUrl('https://www.qwant.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_tab_title(self, index, title):
        self.tabs.setTabText(index, self.format_tab_name(title))

    def format_tab_name(self, name):
        if len(name) > 20:
            return name[:19] + "..."
        return name

    def download_requested(self, download_item):
        default_path = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        suggested_name = download_item.suggestedFileName()
        if not suggested_name:
            suggested_name = "downloaded_file"

        path, _ = QFileDialog.getSaveFileName(self, "Save File", default_path + "/" + suggested_name)
        if path:
            download_item.setPath(path)
            download_item.accept()
            download_item.finished.connect(self.handle_download_finished)
        else:
            download_item.cancel()

    def handle_download_finished(self):
        download_item = self.sender()
        download_item.deleteLater()
        download_item.finished.disconnect(self.handle_download_finished)

def main():
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
