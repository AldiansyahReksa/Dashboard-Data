import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
file_path = 'data_2017.xlsx'  # Pastikan file ini sesuai dengan yang Anda unggah
df = pd.read_excel(file_path, skiprows=1)  # Abaikan header tambahan

# Bersihkan dan atur ulang kolom
df.columns = [
    "Pintu Masuk", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember", "Tahunan"
]
numeric_columns = df.columns[1:]  # Kolom angka (Januari hingga Tahunan)
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Streamlit Layout
st.sidebar.title("Dashboard Data Kunjungan Wisata")
st.sidebar.write("**Created by Kelompok 3**")
st.sidebar.image("raspberry.png", use_column_width=True)

st.sidebar.write("""
- **Aldiansyah Reksa Pratama** - NRP: 220434015  
- **Almayda Faturohman** - NRP: 220434015  
- **M.Fakhrijal Pratama** - NRP: 220434015  
- **Rifky Azis** - NRP: 220434015  
- **Melly Diyani** - NRP: 220434015
""")

# Filter data berdasarkan pintu masuk
pintu_pilihan = st.sidebar.selectbox(
    "Pilih Pintu Masuk",
    df["Pintu Masuk"].unique()
)

data_filtered = df[df["Pintu Masuk"] == pintu_pilihan]

# Visualisasi Data
st.title("Analisis Kunjungan Wisata Mancanegara")
st.subheader(f"Distribusi Wisatawan di Pintu Masuk: {pintu_pilihan}")

# Visualisasi kunjungan tahunan
st.write(f"**Total Kunjungan Tahunan di {pintu_pilihan}:** {data_filtered['Tahunan'].values[0]:,.2f}")

# Visualisasi distribusi bulanan
bulan_data = data_filtered.iloc[0, 1:-1].reset_index()
bulan_data.columns = ["Bulan", "Total Kunjungan"]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=bulan_data, x="Bulan", y="Total Kunjungan", ax=ax)
ax.set_title(f"Distribusi Kunjungan Bulanan di {pintu_pilihan}")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Kunjungan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Analisis keseluruhan
if st.sidebar.checkbox("Tampilkan Analisis Keseluruhan"):
    st.subheader("Total Kunjungan Wisata untuk Semua Pintu Masuk")
    total_data = df.groupby("Pintu Masuk")["Tahunan"].sum().reset_index()
    total_data.columns = ["Pintu Masuk", "Total Kunjungan"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=total_data, x="Pintu Masuk", y="Total Kunjungan", ax=ax)
    ax.set_title("Total Kunjungan Wisata per Pintu Masuk")
    ax.set_xlabel("Pintu Masuk")
    ax.set_ylabel("Total Kunjungan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Korelasi antar bulan
if st.sidebar.checkbox("Tampilkan Korelasi Antar Bulan"):
    corr_matrix = df[numeric_columns[:-1]].corr()  # Kecualikan kolom Tahunan
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Matriks Korelasi Antar Bulan")
    st.pyplot()
