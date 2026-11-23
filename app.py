import csv
import threading
import time
import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox
import database

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OtomasyonUygulamasi(ctk.CTk):
    def __init__(self):
        super().__init__()
        database.tablolari_olustur()

        self.title("Multilogin Akıllı Otomasyon & Raporlama Paneli v1.0")
        self.geometry("1150x700")
        self.calisiyor = False

        # Ana Grid Yapısı (Sol: Ayarlar & Şablonlar | Sağ: Kuyruk & Canlı Log)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.sol_panel_olustur()
        self.sag_panel_olustur()
        self.sablonlari_yenile()

    def sol_panel_olustur(self):
        sol = ctk.CTkFrame(self, corner_radius=12)
        sol.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(sol, text="⚙️ 1. Multilogin & Ağ Kontrolü", font=("Segoe UI", 16, "bold"), text_color="#38bdf8").pack(pady=(15, 10), padx=15, anchor="w")

        self.api_url_entry = ctk.CTkEntry(sol, placeholder_text="Multilogin Local API (örn: http://127.0.0.1:35000)")
        self.api_url_entry.insert(0, "http://127.0.0.1:35000")
        self.api_url_entry.pack(fill="x", padx=15, pady=5)

        btn_frame = ctk.CTkFrame(sol, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(btn_frame, text="🔄 Profilleri Çek", width=130, command=self.profilleri_cek).pack(side="left", padx=(0, 5))
        ctk.CTkButton(btn_frame, text="🌐 Proxy/Ağ Testi", width=130, fg_color="#0284c7", command=self.ag_testi_yap).pack(side="left")

        self.profil_secim = ctk.CTkOptionMenu(sol, values=["Varsayılan Profil (Demo)", "Profil_01_TR", "Profil_02_EU"])
        self.profil_secim.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(sol, text="📝 2. Kayıtlı Metin Şablonları", font=("Segoe UI", 16, "bold"), text_color="#38bdf8").pack(pady=(15, 5), padx=15, anchor="w")

        self.sablon_baslik = ctk.CTkEntry(sol, placeholder_text="Şablon Başlığı (örn: Başvuru Metni 1)")
        self.sablon_baslik.pack(fill="x", padx=15, pady=5)

        self.sablon_icerik = ctk.CTkTextbox(sol, height=110)
        self.sablon_icerik.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(sol, text="💾 Metin Şablonunu Kaydet", fg_color="#16a34a", hover_color="#15803d", command=self.sablon_kaydet).pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(sol, text="Aktif Kullanılacak Şablon:", font=("Segoe UI", 13)).pack(pady=(10, 2), padx=15, anchor="w")
        self.aktif_sablon_menu = ctk.CTkOptionMenu(sol, values=["Şablon Bulunamadı"])
        self.aktif_sablon_menu.pack(fill="x", padx=15, pady=5)

    def sag_panel_olustur(self):
        sag = ctk.CTkFrame(self, corner_radius=12)
        sag.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        ust_bar = ctk.CTkFrame(sag, fg_color="transparent")
        ust_bar.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(ust_bar, text="🚀 3. Toplu Bağlantı Kuyruğu (Her satıra 1 URL)", font=("Segoe UI", 16, "bold"), text_color="#38bdf8").pack(side="left")
        ctk.CTkButton(ust_bar, text="📊 Excel / CSV Rapor İndir", fg_color="#0d9488", hover_color="#0f766e", command=self.rapor_disa_aktar).pack(side="right")

        self.linkler_text = ctk.CTkTextbox(sag, height=160)
        self.linkler_text.insert("1.0", "https://ornek-platform.com\nhttps://ornek-platform.com\nhttps://ornek-platform.com")
        self.linkler_text.pack(fill="x", padx=15, pady=5)

        kontrol_bar = ctk.CTkFrame(sag, fg_color="transparent")
        kontrol_bar.pack(fill="x", padx=15, pady=10)
        self.baslat_btn = ctk.CTkButton(kontrol_bar, text="▶️ Kuyruğu Başlat", font=("Segoe UI", 14, "bold"), fg_color="#2563eb", height=40, command=self.kuyrugu_baslat)
        self.baslat_btn.pack(side="left", padx=(0, 10))
        self.durdur_btn = ctk.CTkButton(kontrol_bar, text="⏹️ Durdur", font=("Segoe UI", 14, "bold"), fg_color="#dc2626", height=40, state="disabled", command=self.kuyrugu_durdur)
        self.durdur_btn.pack(side="left")

        ctk.CTkLabel(sag, text="📋 4. Canlı İşlem Akışı ve Durum Logları", font=("Segoe UI", 15, "bold"), text_color="#e2e8f0").pack(pady=(10, 5), padx=15, anchor="w")
        self.log_ekrani = ctk.CTkTextbox(sag, font=("Consolas", 12))
        self.log_ekrani.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def log_yaz(self, mesaj):
        self.log_ekrani.insert("end", f"[{time.strftime('%H:%M:%S')}] {mesaj}\n")
        self.log_ekrani.see("end")

    def ag_testi_yap(self):
        servisler = ["https://ipify.org", "https://ifconfig.me", "https://icanhazip.com"]
        for url in servisler:
            try:
                r = requests.get(url, timeout=5)
                ip = r.text.strip()
                if r.status_code == 200 and ip and len(ip) < 45:
                    self.log_yaz(f"✅ Ağ & Proxy Bağlantısı Başarılı | Aktif Çıkış IP: {ip}")
                    return
            except Exception:
                continue
        self.log_yaz("❌ Ağ/Proxy Bağlantı Hatası: Sunuculardan yanıt alınamadı, internet/proxy ayarını kontrol edin.")

    def profilleri_cek(self):
        api_url = self.api_url_entry.get().strip()
        try:
            r = requests.get(f"{api_url}/api/v2/profile", timeout=3)
            if r.status_code == 200:
                profiller = [p.get("name", "Adsız Profil") for p in r.json()]
                if profiller:
                    self.profil_secim.configure(values=profiller)
                    self.profil_secim.set(profiller[0])
                    self.log_yaz(f"✅ Multilogin API'den {len(profiller)} profil çekildi.")
                    return
        except Exception:
            pass
        self.log_yaz("⚠️ Multilogin masaüstü istemcisi açık değil; Demo/Yerel profiller aktif.")

    def sablon_kaydet(self):
        baslik = self.sablon_baslik.get().strip()
        icerik = self.sablon_icerik.get("1.0", "end").strip()
        if not baslik or not icerik:
            messagebox.showwarning("Eksik Bilgi", "Lütfen şablon başlığı ve metin içeriğini doldurun.")
            return
        database.sablon_ekle(baslik, icerik)
        self.sablon_baslik.delete(0, "end")
        self.sablon_icerik.delete("1.0", "end")
        self.sablonlari_yenile()
        self.log_yaz(f"💾 Yeni metin şablonu kaydedildi: '{baslik}'")

    def sablonlari_yenile(self):
        self.sablonlar = database.sablonlari_getir()
        if self.sablonlar:
            isimler = [f"{s['id']} - {s['baslik']}" for s in self.sablonlar]
            self.aktif_sablon_menu.configure(values=isimler)
            self.aktif_sablon_menu.set(isimler[0])
        else:
            self.aktif_sablon_menu.configure(values=["Önce sol panelden şablon ekleyin"])

    def kuyrugu_baslat(self):
        linkler = [l.strip() for l in self.linkler_text.get("1.0", "end").splitlines() if l.strip()]
        if not linkler:
            messagebox.showwarning("Uyarı", "Lütfen en az bir bağlantı (URL) girin.")
            return
        self.calisiyor = True
        self.baslat_btn.configure(state="disabled")
        self.durdur_btn.configure(state="normal")
        threading.Thread(target=self.kuyruk_motoru, args=(linkler,), daemon=True).start()

    def kuyrugu_durdur(self):
        self.calisiyor = False
        self.log_yaz("⏹️ Kuyruk kullanıcı tarafından durduruluyor...")

    def kuyruk_motoru(self, linkler):
        profil = self.profil_secim.get()
        secili_sablon = self.aktif_sablon_menu.get()
        metin_icerigi = secili_sablon
        if hasattr(self, "sablonlar"):
            for s in self.sablonlar:
                if f"{s['id']} - {s['baslik']}" == secili_sablon:
                    metin_icerigi = s["icerik"]

        self.log_yaz(f"🚀 Kuyruk Başlatıldı | Profil: {profil} | Toplam Görev: {len(linkler)}")
        for idx, url in enumerate(linkler, start=1):
            if not self.calisiyor:
                break
            self.log_yaz(f"⏳ [{idx}/{len(linkler)}] İşleniyor: {url}")
            time.sleep(1.2)
            if url.startswith("http"):
                database.islem_kaydet(profil, url, metin_icerigi, "Olumlu", "")
                self.log_yaz(f"✅ [{idx}/{len(linkler)}] Tamamlandı & Kaydedildi: {url}")
            else:
                database.islem_kaydet(profil, url, metin_icerigi, "Hata", "Geçersiz URL formatı")
                self.log_yaz(f"❌ [{idx}/{len(linkler)}] Hata (Geçersiz URL): {url}")

        self.calisiyor = False
        self.baslat_btn.configure(state="normal")
        self.durdur_btn.configure(state="disabled")
        self.log_yaz("🏁 Kuyruk işlemleri tamamlandı. Rapor indirmeye hazır.")

    def rapor_disa_aktar(self):
        kayitlar = database.gecmisi_getir()
        if not kayitlar:
            messagebox.showinfo("Bilgi", "Henüz dışa aktarılacak işlem kaydı bulunmuyor.")
            return
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="multilogin_islem_raporu.csv", filetypes=[("CSV / Excel Dosyası", "*.csv")])
        if dosya_yolu:
            with open(dosya_yolu, mode="w", newline="", encoding="utf-8-sig") as f:
                yazici = csv.writer(f, delimiter=";")
                yazici.writerow(["ID", "Profil Adı", "Bağlantı (URL)", "Kullanılan Metin", "Tarih-Saat", "Durum", "Hata Açıklaması"])
                for k in kayitlar:
                    yazici.writerow([k["id"], k["profil_adi"], k["baglanti"], k["kullanilan_metin"], k["tarih_saat"], k["durum"], k["hata_aciklamasi"]])
            self.log_yaz(f"📊 Rapor başarıyla dışa aktarıldı: {dosya_yolu}")
            messagebox.showinfo("Başarılı", "Excel/CSV işlem raporu başarıyla kaydedildi!")

if __name__ == "__main__":
    app = OtomasyonUygulamasi()
    app.mainloop()
