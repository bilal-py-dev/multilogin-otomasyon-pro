import sqlite3
from datetime import datetime

DB_ADI = "otomasyon_kayitlari.db"

def baglan():
    conn = sqlite3.connect(DB_ADI)
    conn.row_factory = sqlite3.Row
    return conn

def tablolari_olustur():
    conn = baglan()
    c = conn.cursor()
    
    # 1. Kayıtlı Metin / Başvuru Şablonları Tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS metin_sablonlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            baslik TEXT NOT NULL,
            icerik TEXT NOT NULL
        )
    """)
    
    # 2. Detaylı İşlem Geçmişi ve Raporlama Tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS islem_gecmisi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profil_adi TEXT,
            baglanti TEXT NOT NULL,
            kullanilan_metin TEXT,
            tarih_saat TEXT NOT NULL,
            durum TEXT NOT NULL,
            hata_aciklamasi TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def sablon_ekle(baslik, icerik):
    conn = baglan()
    conn.execute("INSERT INTO metin_sablonlari (baslik, icerik) VALUES (?, ?)", (baslik, icerik))
    conn.commit()
    conn.close()

def sablonlari_getir():
    conn = baglan()
    veriler = conn.execute("SELECT * FROM metin_sablonlari ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in veriler]

def sablon_sil(sablon_id):
    conn = baglan()
    conn.execute("DELETE FROM metin_sablonlari WHERE id = ?", (sablon_id,))
    conn.commit()
    conn.close()

def islem_kaydet(profil_adi, baglanti, kullanilan_metin, durum, hata_aciklamasi=""):
    conn = baglan()
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO islem_gecmisi (profil_adi, baglanti, kullanilan_metin, tarih_saat, durum, hata_aciklamasi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (profil_adi, baglanti, kullanilan_metin, zaman, durum, hata_aciklamasi))
    conn.commit()
    conn.close()

def gecmisi_getir():
    conn = baglan()
    veriler = conn.execute("SELECT * FROM islem_gecmisi ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in veriler]
