import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca data kunjungan wisata
df_air = pd.read_excel("kunjungan wisata mancanegara_udara.xlsx")
df_laut = pd.read_excel("kunjungan wisata mancanegara_laut.xlsx")
df_darat = pd.read_excel("kunjungan wisata mancanegara_darat.xlsx")

# Gabungkan semua data untuk analisis lebih luas
all_data = pd.concat([df_air, df_laut, df_darat])

# Sidebar dengan informasi kelompok dan rentang waktu
st.sidebar.title("Dashboard Data")
st.sidebar.write("**Created by Kelompok 3**")
st.sidebar.image("raspberry.png", use_column_width=True)

st.sidebar.write("""
- **Aldiansyah Reksa Pratama** - NRP: 220434015  
- **Almayda Faturohman** - NRP: 220434015  
- **M.Fakhrijal Pratama** - NRP: 220434015  
- **Rifky Azis** - NRP: 220434015  
- **Melly Diyani** - NRP: 220434015
""")

# Filter rentang waktu untuk dataset
min_date = pd.to_datetime(all_data["Tanggal"]).min()
max_date = pd.to_datetime(all_data["Tanggal"]).max()
start_date, end_date = st.sidebar.date_input(
    label='Pilih Rentang Waktu', min_value=min_date, max_value=max_date,
    value=[min_date, max_date]
)

# Filter data sesuai rentang waktu
filtered_data = all_data[
    (pd.to_datetime(all_data["Tanggal"]) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(all_data["Tanggal"]) <= pd.to_datetime(end_date))
]

# Header utama dashboard
st.title("Dashboard Analisis Kunjungan Wisata")

# 1. Metrik kunjungan wisata
st.header("Metrik Kunjungan Wisata")
total_kunjungan = filtered_data["Jumlah"].sum()
rata_rata_kunjungan = filtered_data["Jumlah"].mean()

col1, col2 = st.columns(2)
col1.metric("Total Kunjungan", value=int(total_kunjungan))
col2.metric("Rata-rata Kunjungan", value=round(rata_rata_kunjungan, 2))

# 2. Visualisasi Kunjungan Harian
st.header("Kunjungan Wisata Harian")
fig, ax = plt.subplots(figsize=(12, 6))
filtered_data.groupby("Tanggal")["Jumlah"].sum().plot(ax=ax, marker='o', color='#90CAF9')
ax.set_title("Jumlah Kunjungan Harian", fontsize=16)
ax.set_ylabel("Jumlah Kunjungan")
st.pyplot(fig)

# 3. Visualisasi Berdasarkan Transportasi
st.header("Kunjungan Berdasarkan Transportasi")
transportasi_group = filtered_data.groupby("Transportasi")["Jumlah"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=transportasi_group, x="Transportasi", y="Jumlah", palette="pastel", ax=ax)
ax.set_title("Jumlah Kunjungan per Transportasi", fontsize=16)
ax.set_ylabel("Jumlah Kunjungan")
st.pyplot(fig)

# 4. Widget Tambahan (RFM & Demografi)
st.header("Analisis RFM & Demografi")

# Simulasi RFM dari data wisata
st.subheader("Parameter RFM (Recency, Frequency, Monetary)")
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Recency (Hari)", value=10)  # Simulasi
col2.metric("Rata-rata Frequency", value=4)       # Simulasi
col3.metric("Rata-rata Monetary", value=format_currency(5000000, "IDR", locale='id_ID'))

# Visualisasi tambahan - Demografi (simulasi)
st.subheader("Demografi Pengunjung")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=["Laki-Laki", "Perempuan"], y=[300, 250], palette="muted", ax=ax)  # Simulasi
ax.set_title("Jumlah Pengunjung Berdasarkan Gender", fontsize=16)
ax.set_ylabel("Jumlah")
st.pyplot(fig)
