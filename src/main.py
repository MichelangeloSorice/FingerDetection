import logging

from PyQt5.QtWidgets import QApplication

from gui_hw import BabyMathApp

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    babymath_app = BabyMathApp()
    babymath_app.setWindowTitle('Finger count')
    babymath_app.show()
    sys.exit(app.exec_())
