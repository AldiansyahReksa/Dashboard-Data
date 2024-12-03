import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
file_path = 'data_2017.xlsx'  # Pastikan file sesuai dengan dataset Anda
df = pd.read_excel(file_path, skiprows=1)

# Bersihkan data
df.columns = [
    "Pintu Masuk", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember", "Tahunan"
]
numeric_columns = df.columns[1:]  # Kolom angka (Januari hingga Tahunan)
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Tambahkan kolom kategori jalur
df["Jalur"] = df["Pintu Masuk"].apply(
    lambda x: "Darat" if "Darat" in x else "Laut" if "Laut" in x else "Udara"
)

# Streamlit Layout
st.sidebar.title("Dashboard Kunjungan Wisata Mancanegara")
st.sidebar.write("**Created by Kelompok 3**")
st.sidebar.image("raspberry.png", use_column_width=True)

# Pilih kategori jalur
jalur_pilihan = st.sidebar.selectbox(
    "Pilih Kategori Jalur",
    df["Jalur"].unique()
)

# Filter nama jalur berdasarkan kategori
jalur_tersedia = df[df["Jalur"] == jalur_pilihan]["Pintu Masuk"].unique()
nama_pilihan = st.sidebar.selectbox(
    "Pilih Nama Jalur",
    jalur_tersedia
)

# Date Picker untuk tahun dan bulan
st.sidebar.write("Pilih Bulan dan Tahun:")
bulan_pilihan = st.sidebar.selectbox(
    "Pilih Bulan",
    df.columns[1:13]
)
tahun_pilihan = st.sidebar.selectbox(
    "Pilih Tahun",
    ["2017"]  # Sesuaikan jika ada data tahun lain
)

# Data berdasarkan filter
data_filtered = df[df["Pintu Masuk"] == nama_pilihan]

# Checkbox untuk analisis
st.sidebar.subheader("Analisis Data")
tampilkan_total = st.sidebar.checkbox("Tampilkan Total Semua Jalur")
tampilkan_distribusi = st.sidebar.checkbox("Distribusi Kunjungan per Bulan")
tampilkan_trend = st.sidebar.checkbox("Trend Kunjungan per Jalur")

# Main Container
st.title("Analisis Data Kunjungan Wisata")
container = st.container()

with container:
    if tampilkan_total:
        st.subheader("Total Kunjungan Wisata untuk Semua Jalur")
        total_data = df.groupby("Jalur")["Tahunan"].sum().reset_index()
        total_data.columns = ["Jalur", "Total Kunjungan"]

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=total_data, x="Jalur", y="Total Kunjungan", ax=ax, palette="viridis")
        ax.set_title("Total Kunjungan Wisata per Jalur")
        ax.set_xlabel("Jalur")
        ax.set_ylabel("Total Kunjungan")
        st.pyplot(fig)

    if tampilkan_distribusi:
        st.subheader(f"Distribusi Kunjungan Bulanan di {nama_pilihan} ({bulan_pilihan})")
        total_kunjungan = data_filtered[bulan_pilihan].values[0]
        st.write(f"**Total Kunjungan di {nama_pilihan} pada bulan {bulan_pilihan}:** {total_kunjungan:,.2f}")

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=[bulan_pilihan], y=[total_kunjungan], ax=ax, palette="pastel")
        ax.set_title(f"Distribusi Kunjungan Bulan {bulan_pilihan}")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Kunjungan")
        st.pyplot(fig)

    if tampilkan_trend:
        st.subheader(f"Trend Kunjungan Wisata di {nama_pilihan}")
        trend_data = data_filtered.iloc[0, 1:13].reset_index()
        trend_data.columns = ["Bulan", "Jumlah"]

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=trend_data, x="Bulan", y="Jumlah", ax=ax)
        ax.set_title("Trend Kunjungan Wisata per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Total Kunjungan")
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
