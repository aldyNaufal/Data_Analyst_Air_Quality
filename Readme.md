# Air Quality Analysis - Beijing

📊 **Ingin melihat analisis interaktif terkait kualitas udara di Beijing?**  
Kunjungi langsung dashboard-nya di sini:  
👉 [https://data-analyst-air-quality-aldy.streamlit.app/](https://data-analyst-air-quality-aldy.streamlit.app/)

---

## 📁 Dataset Overview

Dataset ini berisi data kualitas udara dari berbagai stasiun pemantauan di **Beijing**, mencakup periode waktu yang luas. Data dikumpulkan dari **12 lokasi berbeda** dan mencakup berbagai parameter polusi udara seperti:

- **Polutan udara**: `PM2.5`, `PM10`, `SO2`, `NO2`, `CO`, `O3`  
- **Faktor meteorologi**: `TEMP` (suhu), `PRES` (tekanan udara), `DEWP` (kelembaban), `RAIN` (curah hujan), `wd` (arah angin), dan `WSPM` (kecepatan angin)

Kolom `station` menunjukkan lokasi stasiun tempat data diambil.

---

## 🧱 Struktur Dataset

| Kolom        | Deskripsi                           |
|--------------|--------------------------------------|
| No           | Nomor urut                          |
| year/month/day/hour | Waktu pencatatan data         |
| PM2.5, PM10, SO2, NO2, CO, O3 | Konsentrasi polutan udara |
| TEMP, PRES, DEWP, RAIN | Parameter cuaca/meteorologi |
| wd, WSPM     | Arah dan kecepatan angin             |
| station      | Nama stasiun pemantauan              |

---

## 🧹 Penanganan Missing Values

- Kolom numerik: Diisi dengan **median** untuk meminimalisir pengaruh outlier.
- Kolom objek (seperti `wd`): Diisi dengan string `"NaN"` untuk mempertahankan struktur data.

---

## 🎯 Tujuan Analisis

1. **Mengidentifikasi Tren Kualitas Udara**  
   Menghitung indeks kualitas udara (AQI) dan menganalisis pola polusi dari tahun ke tahun di setiap stasiun.
   
2. **Menganalisis Lonjakan Polusi**  
   Menemukan lokasi dan periode dengan kenaikan polusi tertinggi serta mengevaluasi potensi penyebabnya.
   
3. **Mengelompokkan Polusi Berdasarkan Musim**  
   Menggunakan metode **K-Means Clustering** untuk mengelompokkan pola musiman polusi udara.

---

## 📈 Hasil Analisis

📌 Analisis lengkap dapat dilihat dalam file `ipynb` yang berisi eksplorasi dan visualisasi data.  
📌 Selain itu, tersedia **dashboard interaktif** untuk melihat tren, pola musiman, dan lonjakan polusi secara visual.

🛠 Untuk menjalankan dashboard secara lokal:

1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   cd dashboard
   streamlit run dashboard.py
   ```

📍 Atau cukup akses versi online-nya di:  
🔗 [https://data-analyst-air-quality-aldy.streamlit.app/](https://data-analyst-air-quality-aldy.streamlit.app/)
