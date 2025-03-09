import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

st.title("Beijing Air Quality Analysis")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Main_Data.csv")

data = load_data()

# Membuat tab utama
tab1, tab2, tab3, tab4 = st.tabs(["Dataset Overview", "Analysis Results", "Dataset Contents", "Final Conclusions"])

# =========================
# Tab 1: Overview
# =========================
with tab1:
    st.markdown("""
# **Overview of Air Quality Dataset in Beijing**

## **Deskripsi Dataset**
Dataset ini berisi data kualitas udara yang dikumpulkan dari **12 stasiun pemantauan** di Beijing dalam rentang waktu **1 Maret 2013 - 28 Februari 2017**. Data ini mencakup berbagai parameter polusi udara serta kondisi cuaca yang dapat mempengaruhi tingkat polusi.

## **Sumber Data**
Data ini diperoleh dari sistem pemantauan kualitas udara di Beijing dan mencakup berbagai variabel lingkungan yang berkontribusi terhadap indeks kualitas udara (AQI).

## **Struktur Dataset**
Dataset terdiri dari beberapa kolom utama:

| No | Kolom | Deskripsi |
| --- | --- | --- |
| 1 | `No` | Nomor indeks data |
| 2 | `year` | Tahun pencatatan |
| 3 | `month` | Bulan pencatatan |
| 4 | `day` | Hari pencatatan |
| 5 | `hour` | Jam pencatatan |
| 6 | `PM2.5` | Partikulat udara PM2.5 (µg/m³) |
| 7 | `PM10` | Partikulat udara PM10 (µg/m³) |
| 8 | `SO2` | Konsentrasi sulfur dioksida (µg/m³) |
| 9 | `NO2` | Konsentrasi nitrogen dioksida (µg/m³) |
| 10 | `CO` | Konsentrasi karbon monoksida (mg/m³) |
| 11 | `O3` | Konsentrasi ozon (µg/m³) |
| 12 | `TEMP` | Suhu udara (°C) |
| 13 | `PRES` | Tekanan udara (hPa) |
| 14 | `DEWP` | Titik embun (°C) |
| 15 | `RAIN` | Curah hujan (mm) |
| 16 | `wd` | Arah angin |
| 17 | `WSPM` | Kecepatan angin (m/s) |
| 18 | `station` | Nama stasiun pemantauan |

## **Jumlah Data**
Dataset ini terdiri dari **data gabungan 12 stasiun pemantauan** yang digabung menggunakan metode **outer join** agar tidak ada data yang hilang dari setiap lokasi.

## **Penanganan Missing Values**
- Kolom **numerik** diisi dengan **median** karena median tidak terpengaruh oleh outlier yang ekstrem.
- Kolom **bertipe objek** seperti arah angin (`wd`) diisi dengan string "NaN".

## **Eksplorasi Data dan Tujuan Analisis**
Setelah melakukan eksplorasi dataset, terdapat beberapa pertanyaan utama yang dapat dijawab melalui analisis lebih lanjut:

1. **Bagaimana tren kualitas udara (AQI) di setiap stasiun dari tahun ke tahun?**
   - Menghitung AQI berdasarkan nilai PM2.5 dan PM10.
   - Melihat tren perubahan kualitas udara dari waktu ke waktu.

2. **Di stasiun mana dan pada tahun berapa terjadi kenaikan polusi udara tertinggi? Apa penyebab utama kenaikan ini?**
   - Menggunakan perhitungan persentase kenaikan polusi udara antar tahun.
   - Mengidentifikasi faktor yang menyebabkan lonjakan polusi.

3. **Bagaimana pola pengelompokan tingkat polusi udara dalam satu tahun? Apakah ada pola musiman?**
   - Menggunakan metode **K-Means Clustering** untuk mengelompokkan hari dalam setahun berdasarkan tingkat polusi udara.
   - Mengidentifikasi apakah ada musim tertentu yang memiliki tingkat polusi lebih tinggi.

## **Manfaat Dataset Ini**
Analisis dari dataset ini dapat memberikan manfaat dalam:
- **Mendukung kebijakan lingkungan** dengan mengidentifikasi pola polusi dan penyebabnya.
- **Membantu perencanaan kesehatan masyarakat** dengan memberikan peringatan dini saat polusi tinggi.
- **Menjadi dasar dalam pengembangan model prediksi kualitas udara** untuk peringatan dan mitigasi.

---
Dengan memahami dataset ini secara menyeluruh, kita dapat menggali lebih dalam pola dan tren kualitas udara di Beijing, serta mengambil langkah-langkah strategis untuk mengurangi dampak polusi udara terhadap masyarakat.
""")
# =========================
# Tab 2: Hasil Analisis
# =========================
with tab2:
    st.header("Beijing Air Quality Analysis Results")
    
    # Sub-tab menggunakan button
    subtab = st.session_state.get("subtab", "AQI Trend per Station")
    col1, col2, col3 = st.columns(3)
    if col1.button("AQI Trend per Station"):
        st.session_state.subtab = "AQI Trend per Station"
    if col2.button("Percentage Increase Highest pollution"):
        st.session_state.subtab = "Percentage Increase Highest pollution"
    if col3.button("Seasonal Pattern Clustering"):
        st.session_state.subtab = "Seasonal Pattern Clustering"
    
    subtab = st.session_state.get("subtab", "AQI Trend per Station")
    
    # =========================
    # 1. AQI Trend per Station
    # =========================
    if subtab == "AQI Trend per Station":
        st.subheader("Air Quality (AQI) Trends per Station")
        st.write("Menampilkan tren AQI (PM2.5 dan PM10) tiap stasiun dari tahun ke tahun.")
        
        # Agregasi data per tahun dan stasiun
        data_grouped = data.groupby(['year', 'station']).agg({'PM2.5':'mean', 'PM10':'mean'}).reset_index()
        
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        for station in data_grouped['station'].unique():
            subset = data_grouped[data_grouped['station'] == station]
            ax1.plot(subset['year'], subset['PM2.5'], marker='o', label=station)
        ax1.set_xlabel('Tahun')
        ax1.set_ylabel('PM2.5')
        ax1.set_title('Tren PM2.5 per Stasiun')
        ax1.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig1)
        
        st.markdown("""
**Berdasarkan visualisasi tren AQI PM10 dan PM2.5 di setiap stasiun dari tahun ke tahun, dapat disimpulkan beberapa pola utama terkait kualitas udara:**

1. **Pola Umum**  
   - Secara umum, tren AQI di berbagai stasiun menunjukkan pola **naik-turun**.  
   - AQI meningkat dari tahun 2013 ke 2014, mengalami **penurunan sekitar tahun 2015-2016**, dan kembali meningkat pada 2017.  
   - Pola ini terlihat baik untuk PM10 maupun PM2.5.  

2. **Penurunan pada 2016**  
   - Hampir semua stasiun mengalami **penurunan AQI pada tahun 2016**, yang mengindikasikan adanya perbaikan kualitas udara atau pengurangan polutan di tahun tersebut.  
   - Faktor yang mungkin mempengaruhi adalah kebijakan lingkungan atau perubahan kondisi cuaca.  

3. **Peningkatan Signifikan di 2017**  
   - Pada tahun 2017, AQI kembali meningkat drastis di hampir semua stasiun, terutama pada PM2.5.  
   - Ini menunjukkan peningkatan polusi udara di tahun tersebut, yang bisa disebabkan oleh aktivitas industri, cuaca, atau faktor lainnya.  

4. **Variasi Antar Stasiun**  
   - Meskipun pola umum mirip, ada beberapa variasi antar stasiun.  
   - Beberapa stasiun memiliki AQI yang selalu lebih tinggi dibandingkan lainnya, menunjukkan tingkat polusi yang lebih besar.  

Secara keseluruhan, kualitas udara mengalami **fluktuasi**, dengan tahun 2016 sebagai titik di mana udara relatif lebih bersih, sebelum kembali memburuk pada 2017.
        """)
    
    # =========================
    # 2. Kenaikan Persentase Polusi Udara
    # =========================
    elif subtab == "Percentage Increase Highest pollution":
        st.subheader("Percentage Increase in Air Pollution per Station")
        st.write("Menampilkan stasiun dan tahun dengan kenaikan persentase polusi udara tertinggi.")
        
        agg_data = data.groupby(['station', 'year']).agg({'PM2.5': 'mean', 'PM10': 'mean'}).reset_index()
        agg_data['PM2.5_pct_increase'] = agg_data.groupby('station')['PM2.5'].pct_change() * 100
        agg_data['PM10_pct_increase'] = agg_data.groupby('station')['PM10'].pct_change() * 100
        agg_data = agg_data.dropna()
        
        st.markdown("""
### **2. Di stasiun mana dan pada tahun berapa terjadi kenaikan persentase polusi udara tertinggi? Apa penyebab utama kenaikan ini?**

#### **Jawaban:**  
Berdasarkan visualisasi data, kenaikan persentase polusi udara tertinggi terjadi di:  
1. **PM2.5** – **Stasiun Wanshouxigong pada tahun 2017**, dengan kenaikan **sekitar 36%** dibandingkan tahun sebelumnya.  
2. **PM10** – **Stasiun Tiantan pada tahun 2017**, dengan kenaikan **hampir 29%** dibandingkan tahun sebelumnya.  

#### **Penyebab Utama Kenaikan Ini:**  
Kenaikan signifikan dalam konsentrasi PM2.5 dan PM10 pada tahun 2017 bisa disebabkan oleh beberapa faktor utama:  

1. **Kondisi Cuaca yang Tidak Menguntungkan**  
   - Tahun 2017 di beberapa wilayah mengalami kondisi atmosfer yang tidak mendukung dispersi polutan, seperti suhu rendah, kelembaban tinggi, dan tekanan udara yang menyebabkan polutan tetap berada di dekat permukaan.  

2. **Peningkatan Aktivitas Industri dan Kendaraan**  
   - Wanshouxigong dan Tiantan merupakan area dengan aktivitas industri dan transportasi tinggi. Peningkatan produksi industri dan jumlah kendaraan bermotor dapat meningkatkan emisi partikulat di udara.  

3. **Kebakaran Biomassa atau Aktivitas Pertanian**  
   - Pembakaran lahan pertanian atau biomassa di sekitar wilayah tersebut juga dapat menyumbang peningkatan partikel PM2.5 dan PM10.  

4. **Efek Musiman dan Polusi dari Wilayah Lain**  
   - Selama musim dingin, penggunaan batu bara untuk pemanas rumah tangga dan industri meningkat, yang berkontribusi pada peningkatan partikel polusi udara. Selain itu, polusi bisa datang dari daerah sekitar karena pola angin yang membawa polutan dari satu kota ke kota lain.  

5. **Penurunan Efektivitas Regulasi Lingkungan**  
   - Jika pada periode tersebut terjadi kelonggaran dalam penerapan kebijakan pengurangan emisi industri dan transportasi, maka kemungkinan besar terjadi lonjakan polusi.  

#### **Kesimpulan**  
Tahun 2017 menunjukkan kenaikan signifikan polusi udara di beberapa stasiun, terutama Wanshouxigong (PM2.5) dan Tiantan (PM10). Peningkatan ini didorong oleh kombinasi faktor lingkungan, aktivitas manusia, dan kondisi cuaca yang memperparah kualitas udara. Regulasi ketat dan inovasi dalam pengelolaan polusi sangat diperlukan untuk mencegah lonjakan serupa di masa depan.
        """)
    
    # =========================
    # 3. Clustering Pola Musiman
    # =========================
    elif subtab == "Seasonal Pattern Clustering":
        st.subheader("Seasonal Pattern Clustering of Air Pollution")
        st.write("Mengelompokkan hari dalam setahun berdasarkan tingkat polusi udara (PM2.5 dan PM10) menggunakan K-Means.")
        
        data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
        daily_data = data.groupby('date').agg({'PM2.5': 'mean', 'PM10': 'mean'}).reset_index()
        kmeans = KMeans(n_clusters=4, random_state=42)
        daily_data['cluster'] = kmeans.fit_predict(daily_data[['PM2.5', 'PM10']])
        
        st.markdown("""
Berdasarkan hasil analisis clustering menggunakan K-Means pada data harian polusi udara (PM2.5 dan PM10), kita dapat mengidentifikasi pola musiman yang signifikan dalam tingkat polusi udara sepanjang tahun.

### **1. Pola Pengelompokan Polusi Udara dalam Satu Tahun**
Hasil clustering menunjukkan bahwa hari-hari dalam setahun dapat dikategorikan ke dalam empat kelompok berdasarkan tingkat polusi udara:
- **Cluster 1 (Polusi Udara Rendah)** – Ditandai dengan warna biru paling terang.
- **Cluster 2 (Polusi Udara Sedang)** – Warna biru yang sedikit lebih gelap.
- **Cluster 3 (Polusi Udara Tinggi)** – Warna biru lebih pekat.
- **Cluster 4 (Polusi Udara Sangat Tinggi)** – Warna biru yang paling gelap.

Dari grafik distribusi cluster per bulan, terlihat bahwa bulan-bulan tertentu memiliki lebih banyak hari dengan tingkat polusi udara yang tinggi dibandingkan bulan lainnya.

### **2. Apakah Ada Pola Musiman yang Signifikan?**
Dari visualisasi distribusi cluster per bulan:
- **Polusi udara rendah hingga sedang (Cluster 1 & 2)** lebih sering terjadi pada pertengahan hingga akhir tahun, terutama di bulan **Juni hingga Agustus**. Ini bisa mengindikasikan kondisi atmosfer yang lebih bersih pada periode tersebut, kemungkinan karena faktor cuaca atau curah hujan yang lebih tinggi yang membantu mengurangi konsentrasi polutan di udara.
- **Polusi udara tinggi hingga sangat tinggi (Cluster 3 & 4)** cenderung lebih dominan di awal tahun, terutama di **Januari hingga Mei**. Ini dapat dikaitkan dengan musim kemarau atau aktivitas industri dan kendaraan yang lebih intensif pada periode tersebut.

### **Kesimpulan**
Terdapat pola musiman dalam tingkat polusi udara:
- **Musim dengan polusi tinggi** umumnya terjadi di awal tahun (Januari – Mei).
- **Musim dengan polusi rendah** lebih sering terjadi di pertengahan hingga akhir tahun (Juni – Agustus).

Pola ini bisa menjadi acuan untuk strategi mitigasi polusi udara, seperti meningkatkan pemantauan kualitas udara di bulan-bulan dengan risiko tinggi dan mengedukasi masyarakat untuk mengurangi aktivitas yang dapat meningkatkan polusi udara.
        """)

# =========================
# Tab 3: Isi Dataset
# =========================
with tab3:
    st.subheader("Dataset Contents")
    st.write(data.head(50))

# =========================
# Tab 4: Kesimpulan Akhir
# =========================
with tab4:
    st.subheader("Final Conclusions")
    st.markdown("""
Berdasarkan tiga jawaban dari pertanyaan di atas, dapat disimpulkan bahwa:  

### **1. Tren Polusi Udara Mengalami Fluktuasi**  
Polusi udara (PM10 dan PM2.5) tidak menunjukkan tren linear, tetapi mengalami **fluktuasi** dari tahun ke tahun.  
- Tahun **2016** adalah periode di mana kualitas udara membaik secara signifikan.  
- Tahun **2017** terjadi lonjakan drastis polusi udara, terutama di stasiun **Wanshouxigong (PM2.5) dan Tiantan (PM10)**.  

### **2. Faktor Penyebab Kenaikan Polusi Udara**  
Kenaikan polusi udara pada tahun tertentu disebabkan oleh kombinasi beberapa faktor, seperti:  
- **Kondisi atmosfer** yang tidak mendukung penyebaran polutan.  
- **Peningkatan aktivitas industri dan kendaraan** yang meningkatkan emisi partikulat.  
- **Pembakaran biomassa atau aktivitas pertanian** yang menambah polutan udara.  
- **Musim dingin** yang mendorong penggunaan batu bara untuk pemanas, memperburuk kualitas udara.  
- **Penurunan efektivitas regulasi lingkungan** yang menyebabkan lonjakan emisi dari sumber industri dan transportasi.  

### **3. Polusi Udara Memiliki Pola Musiman**  
- **Polusi udara tinggi** terjadi di awal tahun (**Januari – Mei**), terutama karena kondisi cuaca kering dan peningkatan aktivitas industri.  
- **Polusi udara lebih rendah** terjadi di pertengahan hingga akhir tahun (**Juni – Agustus**), kemungkinan karena curah hujan yang lebih tinggi dan kondisi atmosfer yang lebih baik.
    """)
