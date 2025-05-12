from PyQt6.QtWidgets import QApplication
from _ziyaret import form_Anasayfa

app = QApplication([])
pencere = form_Anasayfa()
pencere.show()
app.exec()