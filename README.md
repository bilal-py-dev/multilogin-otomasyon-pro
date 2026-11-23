# 🚀 Multilogin API Uyumlu Masaüstü Otomasyon & Raporlama Paneli

Multilogin Local API ile entegre çalışabilen, toplu bağlantı kuyruğu yöneten, metin şablonları kaydeden ve tüm işlem geçmişini tek tıkla **Excel/CSV** raporu olarak dışa aktaran kurumsal masaüstü otomasyon yazılımı.

## ✨ Öne Çıkan Özellikler
- **Multilogin & Ağ Kontrolü:** Yerel API üzerinden profil listeleme, aktif çıkış IP ve proxy bağlantı testi.
- **Metin Şablonu Yönetimi:** Sık kullanılan başvuru veya işlem metinlerini SQLite veritabanında kaydetme ve tek tıkla seçme.
- **Akıllı Kuyruk Sistemi:** Çoklu bağlantıları sıraya alma, anlık durum takibi, hata yakalama ve durdur/başlat kontrolü.
- **Detaylı Veritabanı & Excel/CSV Çıktısı:** Tüm işlem geçmişini (profil, URL, metin, tarih-saat, durum ve hata açıklaması) saklama ve Türkçe karakter uyumlu CSV raporu alma.
- **Bağımsız Windows (.exe) Mimarisi:** `PyInstaller` ile derlenmiş, Python kurulumu gerektirmeyen tek parça çalıştırılabilir yapı.

## 🛠️ Kullanılan Teknolojiler
- **Dil & Arayüz:** Python, CustomTkinter
- **Veritabanı & Raporlama:** SQLite3, CSV (UTF-8 BOM)
- **Ağ & Paketleme:** Requests, Threading, PyInstaller
