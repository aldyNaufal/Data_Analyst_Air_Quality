import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
# -------------------------------
# Fungsi untuk memuat dataset dengan caching
# -------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Main_Data.csv")
        # Membuat kolom datetime dari kolom year, month, day, dan hour
        df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        return df
    except Exception as e:
        st.error("Error loading data: " + str(e))
        return pd.DataFrame()

data = load_data()

# Sekarang kita bisa membuat kolom tambahan dengan menggunakan kolom datetime yang baru dibuat
data['day_of_week'] = data['datetime'].dt.day_name()

# Daftar polutan dan variabel cuaca yang tersedia
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
weather_vars = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

# Daftar stasiun
stations = data['station'].unique()

# -------------------------------
# Custom CSS untuk styling tombol dan sidebar
# -------------------------------
st.markdown("""
    <style>
    /* Rata kiri untuk teks tombol */
    div.stButton > button {
        text-align: left !important;
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        font-size: 18px;
        padding: 0;
        margin-top: 10px;
        cursor: pointer;
        display: block;
        width: 100%;
    }
    /* Background sidebar agar tombol terlihat */
    .css-1d391kg {
        background-color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Inisialisasi state untuk navigasi
# -------------------------------
if "page" not in st.session_state:
    params = st.experimental_get_query_params()
    st.session_state.page = params.get("page", ["About"])[0]

def set_page(page):
    st.session_state.page = page
    st.query_params = {"page": page}

# -------------------------------
# Sidebar Navigasi
# -------------------------------
st.sidebar.title("Beijing Air Quality Analysis")
if st.sidebar.button("About Data"):
    set_page("About")
if st.sidebar.button("Visualization Data"):
    set_page("Visualization")
if st.sidebar.button("Data"):
    set_page("Data")

# -------------------------------
# Tampilan halaman berdasarkan pilihan navigasi
# -------------------------------
if st.session_state.page == "Data":
    st.title("📊 Dataset Air Quality")

    # Filter interaktif di sidebar
    st.sidebar.subheader("🎯 Filter Data")
    # Pastikan kolom ada dalam dataset
    year_options = sorted(data["year"].unique()) if "year" in data.columns else []
    month_options = sorted(data["month"].unique()) if "month" in data.columns else []
    station_options = sorted(data["station"].unique()) if "station" in data.columns else []

    year_selected = st.sidebar.multiselect("Pilih Tahun:", year_options, default=year_options)
    month_selected = st.sidebar.multiselect("Pilih Bulan:", month_options, default=month_options)
    station_selected = st.sidebar.multiselect("Pilih Stasiun:", station_options, default=station_options)

    # Pastikan filter tidak kosong
    if not year_selected:
        year_selected = year_options
    if not month_selected:
        month_selected = month_options
    if not station_selected:
        station_selected = station_options

    # Konversi tipe data tahun dan bulan
    try:
        year_selected = list(map(int, year_selected))
        month_selected = list(map(int, month_selected))
    except Exception:
        pass

    # Normalisasi nama stasiun untuk filtering
    if "station" in data.columns:
        data["station"] = data["station"].str.strip().str.lower()
    station_selected = [s.strip().lower() for s in station_selected]

    # Filter dataset berdasarkan pilihan user
    filtered_df = data[
        (data["year"].isin(year_selected)) &
        (data["month"].isin(month_selected)) &
        (data["station"].isin(station_selected))
    ]

    st.write(f"Total data setelah filter: {filtered_df.shape[0]}")
    st.subheader("📑 Data yang Ditampilkan:")
    st.write(f"Menampilkan **{filtered_df.shape[0]}** baris dari total **{data.shape[0]}** data yang tersedia.")
    st.dataframe(filtered_df)

    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data yang cocok dengan filter yang dipilih.")

elif st.session_state.page == "Visualization":
    st.header("Visualization Data")
    
    # Membuat 4 tab untuk konten visualisasi
    tab1, tab2, tab3, tab4 = st.tabs(["Tab 1", "Tab 2", "Tab 3", "Tab 4"])
    
    # ====================
    # Tab 1: Analisis Tren Waktu
    # ====================
    with tab1:
        st.subheader("Analisis Tren Waktu")
        # Filter: Pilih polutan dan frekuensi visualisasi
        selected_pollutant = st.selectbox("Pilih Polutan", pollutants)
        frequency = st.selectbox("Pilih Frekuensi", ["Harian", "Bulanan", "Tahunan"])
        # Filter: Pilih rentang tanggal
        min_date = data['datetime'].min().date()
        max_date = data['datetime'].max().date()
        date_range = st.date_input("Pilih Rentang Tanggal", [min_date, max_date])
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = data[(data['datetime'].dt.date >= start_date) & (data['datetime'].dt.date <= end_date)]
        else:
            df_filtered = data.copy()
        
        # Kelompokkan data sesuai frekuensi yang dipilih
        if frequency == "Harian":
            # Buat kolom 'Tanggal' berupa tanggal saja
            df_filtered = df_filtered.copy()  # menghindari SettingWithCopyWarning
            df_filtered['Tanggal'] = df_filtered['datetime'].dt.date
            df_grouped = df_filtered.groupby('Tanggal')[selected_pollutant].mean().reset_index()
            df_grouped['Tanggal'] = pd.to_datetime(df_grouped['Tanggal'])
        elif frequency == "Bulanan":
            df_filtered = df_filtered.copy()
            df_filtered['Tanggal'] = df_filtered['datetime'].dt.to_period('M').dt.to_timestamp()
            df_grouped = df_filtered.groupby('Tanggal')[selected_pollutant].mean().reset_index()
        elif frequency == "Tahunan":
            df_filtered = df_filtered.copy()
            df_filtered['Tanggal'] = df_filtered['datetime'].dt.to_period('Y').dt.to_timestamp()
            df_grouped = df_filtered.groupby('Tanggal')[selected_pollutant].mean().reset_index()
        
        df_grouped = df_grouped.sort_values('Tanggal')
        st.line_chart(df_grouped.set_index('Tanggal')[selected_pollutant])
    
    # ====================
    # Tab 2: Hubungan dengan Kondisi Cuaca
    # ====================
    with tab2:
       st.subheader("Hubungan antara Polutan dan Kondisi Cuaca")
       # Filter: Pilih polutan dan variabel cuaca
       selected_pollutant = st.selectbox("Pilih Polutan", pollutants, key="pollutant_tab2")
       selected_weather = st.selectbox("Pilih Variabel Cuaca", weather_vars)
      
       # Visualisasi scatter plot dengan marker berisi warna gelap dan tepi warna terang
       fig, ax = plt.subplots()
       ax.scatter(
          data[selected_pollutant],
          data[selected_weather],
          alpha=0.7,
          facecolor="#1f77b4",   # biru gelap untuk isi marker
          edgecolor="#aec7e8"    # biru muda untuk tepi marker
       )
       ax.set_xlabel(selected_pollutant)
       ax.set_ylabel(selected_weather)
       ax.set_title(f"Korelasi antara {selected_pollutant} dan {selected_weather}")
       st.pyplot(fig)

    # ====================
    # Tab 3: Analisis Berdasarkan Lokasi/Stasiun
    # ====================
    with tab3:
       st.subheader("Analisis Berdasarkan Lokasi/Stasiun")
       # Filter: Pilih stasiun (bisa lebih dari satu) dan polutan
       selected_stations = st.multiselect("Pilih Stasiun", options=stations, default=list(stations))
       selected_pollutant = st.selectbox("Pilih Polutan", pollutants, key="pollutant_tab3")
      
       df_station = data[data['station'].isin(selected_stations)]
       # Menghitung rata-rata polutan per stasiun
       df_grouped = df_station.groupby('station')[selected_pollutant].mean().reset_index()
      
       # Buat palet warna: skala 'Blues' dimana nilai tertinggi = biru gelap dan terendah = biru muda
       norm = mcolors.Normalize(vmin=df_grouped[selected_pollutant].min(), vmax=df_grouped[selected_pollutant].max())
       colors = [plt.cm.Blues(norm(val)) for val in df_grouped[selected_pollutant]]
      
      # Visualisasi bar chart dengan warna sesuai nilai
       fig, ax = plt.subplots()
       sns.barplot(data=df_grouped, x='station', y=selected_pollutant, ax=ax, palette=colors)
       ax.set_title(f"Rata-rata {selected_pollutant} per Stasiun")
       st.pyplot(fig)

    # ====================
    # Tab 4: Heatmap dan Visualisasi Kalender (Agregasi per 10 jam)
    # ====================
    with tab4:
       st.subheader("Heatmap Polusi")
       # Filter: Pilih polutan untuk ditampilkan pada heatmap
       selected_pollutant = st.selectbox("Pilih Polutan", pollutants, key="pollutant_tab4")
      
       # Buat salinan data dan agregasikan per 10 jam
       df_heat = data.copy()
       # Buat kolom 'hour_bin' berdasarkan interval 10 jam: 0, 10, 20
       df_heat['hour_bin'] = (df_heat['hour'] // 10) * 10
      
       # Pivot table: rata-rata polutan per hari dalam seminggu dan per interval 10 jam
       df_heat = df_heat.pivot_table(index='day_of_week', columns='hour_bin', values=selected_pollutant, aggfunc='mean')
      
       # Atur urutan hari
       order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
       df_heat = df_heat.reindex(order)
       # Urutkan kolom jam (interval 10 jam)
       df_heat = df_heat.reindex(sorted(df_heat.columns), axis=1)
      
       fig, ax = plt.subplots(figsize=(10, 6))
       sns.heatmap(df_heat, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
       ax.set_title(f"Heatmap {selected_pollutant} per 10 Jam dan Hari")
       st.pyplot(fig)


elif st.session_state.page == "About":
    st.header("Overview of Air Quality Dataset in Beijing")
    st.markdown("""
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
      Dataset ini terdiri dari **data gabungan 12 stasiun pemantauan** yang digabung menggunakan metode **outer join** agar tidak ada data yang hilang dari setiap lokasi. Untuk melihat detail isi dataset, silakan kunjungi laman [Data](?page=Data).

      ## **Eksplorasi Data dan Tujuan Analisis**
      Setelah melakukan eksplorasi dataset, terdapat beberapa pertanyaan utama yang dapat dijawab melalui analisis lebih lanjut:

      1. **Bagaimana tren kualitas udara (AQI) di setiap stasiun dari tahun ke tahun?**
         - Menghitung AQI berdasarkan nilai PM2.5 dan PM10.
         - Melihat tren perubahan kualitas udara dari waktu ke waktu.

      2. **Di stasiun mana dan pada tahun berapa terjadi kenaikan polusi udara tertinggi? Apa penyebab utama kenaikan ini?**
         - Menggunakan perhitungan persentase kenaikan polusi udara antar tahun.
         - Mengidentifikasi faktor yang menyebabkan lonjakan polusi.

      3. **Bagaimana pola kejadian polusi udara tinggi di setiap stasiun? Apakah terdapat pola tertentu dalam kejadian polusi tinggi berdasarkan aspek Recency, Frequency, dan Monetary?**
         - Mengidentifikasi stasiun yang paling sering dan terbaru mengalami kejadian polusi udara tinggi.
         - Menilai tingkat keparahan polusi di setiap stasiun melalui rata-rata nilai PM2.5 pada hari-hari dengan polusi tinggi.  

      ## **Manfaat Dataset Ini**
      Analisis dari dataset ini dapat memberikan manfaat dalam:
      - **Mendukung kebijakan lingkungan** dengan mengidentifikasi pola polusi dan penyebabnya.
      - **Membantu perencanaan kesehatan masyarakat** dengan memberikan peringatan dini saat polusi tinggi.
      - **Menjadi dasar dalam pengembangan model prediksi kualitas udara** untuk peringatan dan mitigasi.

      ---
      Dengan memahami dataset ini secara menyeluruh, kita dapat menggali lebih dalam pola dan tren kualitas udara di Beijing, serta mengambil langkah-langkah strategis untuk mengurangi dampak polusi udara terhadap masyarakat.
      """, unsafe_allow_html=True)
