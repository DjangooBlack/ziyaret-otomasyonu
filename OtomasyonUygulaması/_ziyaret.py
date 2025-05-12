from PyQt6.QtWidgets import *
from ziyaret import Ui_form_anasayfa
import sqlite3

class form_Anasayfa(QMainWindow):
    def __init__(self):
        super().__init__()
        self.home = Ui_form_anasayfa()
        self.home.setupUi(self)
        
        self.home.tableWidget.setEnabled(False)
        
        # butonlar eventleri ------------------------------
        self.home.mn_hakkimda.triggered.connect(self.hakkinda)
        self.home.mn_cikis.triggered.connect(QApplication.instance().quit)
        self.home.btn_kayit.clicked.connect(self.listeKayit)
        self.home.btn_sil.clicked.connect(self.listeSil)
        self.home.btn_ara.clicked.connect(self.listele)   
        
    def baglanti(self):
        with sqlite3.connect("./otomasyon.db") as baglan:
            imlec = baglan.cursor()
            imlec.execute(" create table if not exists tbl_ziyaret (ziyarettarihi TEXT, ziyaretcitc İNT, ziyaretciadi TEXT, ziyaretcisoyadi TEXT, evadi TEXT, evsoyadi TEXT, evno İNT, evblok TEXT) ")
            return baglan 
        
    def listeKayit(self):
        from datetime import date 
        self.today = date.today()
        try:
            conn = self.baglanti()
            sql = conn.cursor()  
            sql.execute(f""" insert into tbl_ziyaret (ziyarettarihi, ziyaretcitc, ziyaretciadi, ziyaretcisoyadi, evadi, evsoyadi, evno, evblok) values ("{self.today}",{int(self.home.txt_ziyaretTC.text())},"{self.home.txt_ziyaretAdi.text()}","{self.home.txt_ziyaretSoyadi.text()}","{self.home.txt_evAdi.text()}","{self.home.txt_evSoyadi.text()}",{int(self.home.txt_evDaire.text())},"{self.home.txt_evBlok.text()}") """)
            conn.commit()
            QMessageBox.information(self, "Kayıt İşlemi", "Ziyaret Verisi Kaydedilmiştir")
            self.temizle()
        except Exception as hata:
            QMessageBox.critical(self, "Bağlantı Hatası", f"Bir Hata Oluştu ! \n{hata}")
    
    def temizle(self):
        self.home.txt_ziyaretTC.clear()
        self.home.txt_ziyaretAdi.clear()
        self.home.txt_ziyaretSoyadi.clear()
        self.home.txt_evAdi.clear()
        self.home.txt_evSoyadi.clear()
        self.home.txt_evDaire.clear()
        self.home.txt_evBlok.clear()
    
    def listeSil(self):
        print("sil")
    
    def listele(self):
        self.home.tableWidget.setEnabled(True)
        tablo = self.home.tableWidget
        tablo.clear()
        try:
            kolonlar = ["ziyarettarihi", "ziyaretcitc", "ziyaretciadi", "ziyaretcisoyadi", "evadi", "evsoyadi", "evno", "evblok"]
            tablo.setHorizontalHeaderLabels(kolonlar)
            conn = self.baglanti()
            cursor = conn.cursor()
            cursor.execute(" select * from tbl_ziyaret ")
            ziyaretler = cursor.fetchall()
            
            if ziyaretler:
                tablo.setRowCount(len(ziyaretler))
                ziyaretSayisi = 0
                for ziyaret in ziyaretler:
                    tablo.setItem(ziyaretSayisi, 0, QTableWidgetItem(str(ziyaret[0])))
                    tablo.setItem(ziyaretSayisi, 1, QTableWidgetItem(str(ziyaret[1])))
                    tablo.setItem(ziyaretSayisi, 2, QTableWidgetItem(str(ziyaret[2])))
                    tablo.setItem(ziyaretSayisi, 3, QTableWidgetItem(str(ziyaret[3])))
                    tablo.setItem(ziyaretSayisi, 4, QTableWidgetItem(str(ziyaret[4])))
                    tablo.setItem(ziyaretSayisi, 5, QTableWidgetItem(str(ziyaret[5])))
                    tablo.setItem(ziyaretSayisi, 6, QTableWidgetItem(str(ziyaret[6])))
                    tablo.setItem(ziyaretSayisi, 7, QTableWidgetItem(str(ziyaret[7])))
                    
                    ziyaretSayisi += 1
            else:
                QMessageBox.warning(self, "Tablo Uyarısı", "Tablo Veriler Bulunamadı")
                
        except Exception as error:
            QMessageBox.critical(self, "Tablo Hatası", "Bir Hata Oluştu \n" + error)
        
    def hakkinda(self):
        QMessageBox.information(self, "Hakımmda", f"<p style=color:#F7E2C7;fons-size:12;>Bu Otomasyon <b>halil ibrahim bayram</b> Tarafında ❤️ ile Yapılmıştır.</p>")
