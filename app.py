import sys
import pyautogui
import pytesseract
from PyQt5.QtWidgets import QApplication, QWidget, QRubberBand, QMessageBox, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QRect, QPoint, QSize

class ScreenshotApp(QWidget):
    # 初期化
    def __init__(self):
        super().__init__()
        self.initUI()
        self.find_text = []

    # UIの初期化
    def initUI(self):
        self.setWindowTitle('範囲指定スクリーンショット')
        self.showFullScreen() 
        self.setWindowOpacity(0.2) # 透過
        self.origin = QPoint()

        # 四角形の選択範囲に設定 (一番上のウィンドウに設定)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.show()


    # マウス 押下イベント
    def mousePressEvent(self, event):
        self.origin = event.pos() # 押下位置を取得
        self.rubberBand.setGeometry(QRect(self.origin, QSize())) # QSize() : サイズの初期化
        self.rubberBand.show()

    # マウス 移動イベント
    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    # マウス 離した時イベント
    def mouseReleaseEvent(self, event):
        # 選択範囲非表示にして、範囲を取得
        self.rubberBand.hide()
        rect = self.rubberBand.geometry()

        # スクリーンショット
        self.takeScreenshot(rect)
        # 半透明のウィンドウを閉じる
        self.close()

    # スクリーンショット 保存
    def takeScreenshot(self, rect):
        # x : 左上のx座標, y : 左上のy座標, 
        screenshot = pyautogui.screenshot(region=(rect.x(), rect.y(), rect.width(), rect.height()))
        screenshot.save('screenshot.png')

        # スクリーンショットから文字列を取得
        try:
            text = pytesseract.image_to_string(screenshot)
            self.find_text = text.split('\n')
            self.showTextBoxes()
        except Exception as e:
            QMessageBox.warning(self, 'エラー', f'文字認識できませんでした: {e}')
            return
        
        # テキストボックスを生成して表示
        self.showTextBoxes()

    # テキストボックス表示
    def showTextBoxes(self):
        self.text_box_window = QWidget()
        self.text_box_window.setWindowTitle('ふんわり文字認識')
        layout = QVBoxLayout()

        # 認識したテキストをテキストボックスに表示
        for text in self.find_text:
            if text.strip():
                text_box = QLineEdit(text)
                layout.addWidget(text_box)

        # ボタン 設定
        select_button = QPushButton('もう一回')
        select_button.clicked.connect(self.showAgain)
        layout.addWidget(select_button)

        self.text_box_window.setLayout(layout)
        self.text_box_window.show()

    # もう一回ボタン押下時
    def showAgain(self):
        self.text_box_window.close()
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    sys.exit(app.exec_())
