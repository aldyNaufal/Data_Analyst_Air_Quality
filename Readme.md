# Dataset Overview

Dataset ini berisi data kualitas udara dari berbagai stasiun pemantauan di Beijing, mencakup periode waktu yang luas. Data ini dikumpulkan dari 12 lokasi berbeda dan mencakup berbagai parameter polusi udara seperti PM2.5, PM10, SO2, NO2, CO, dan O3, serta faktor meteorologi seperti suhu (TEMP), tekanan udara (PRES), kelembaban (DEWP), curah hujan (RAIN), arah angin (wd), dan kecepatan angin (WSPM). Kolom 'station' menunjukkan lokasi tempat data diambil.

## Struktur Dataset
Dataset ini memiliki kolom-kolom sebagai berikut:
- **No**: Nomor urut
- **year, month, day, hour**: Waktu pencatatan data
- **PM2.5, PM10, SO2, NO2, CO, O3**: Konsentrasi polutan udara
- **TEMP, PRES, DEWP, RAIN**: Parameter meteorologi
- **wd, WSPM**: Arah dan kecepatan angin
- **station**: Nama stasiun pemantauan

## Penanganan Missing Values
- Untuk kolom numerik, nilai yang hilang diisi dengan **median** dari masing-masing kolom untuk mengurangi dampak outlier.
- Untuk kolom bertipe objek (seperti 'wd'), nilai yang hilang diisi dengan string "NaN".

## Tujuan Analisis
1. **Mengidentifikasi Tren Kualitas Udara**
   - Menghitung indeks kualitas udara (AQI) dan menganalisis pola polusi di setiap stasiun dari tahun ke tahun.
2. **Menganalisis Lonjakan Polusi**
   - Menemukan lokasi dan periode dengan kenaikan polusi tertinggi serta mengevaluasi penyebabnya.
3. **Mengelompokkan Tingkat Polusi Berdasarkan Musim**
   - Menggunakan K-Means Clustering untuk mengelompokkan pola polusi dalam setahun guna melihat perbedaan antar musim.

## Hasil Analisis
Jika ingin melihat hasil analisis lebih lanjut, dapat ditemukan di file **ipynb** yang berisi eksplorasi data dan perhitungan lebih detail. Selain itu, telah disiapkan **dashboard interaktif** yang menampilkan ringkasan analisis ini. Untuk menjalankannya, pastikan terlebih dahulu menginstal dependensi yang ada di file `requirements.txt` dengan perintah:
```sh
pip install -r requirements.txt
```
Setelah itu, jalankan dashboard dengan perintah berikut:
```sh
cd dashboard
streamlit run dashboard.py
```
Dashboard ini memberikan visualisasi dari tren polusi udara, pola musiman, serta analisis kenaikan polusi di berbagai lokasi Beijing.

