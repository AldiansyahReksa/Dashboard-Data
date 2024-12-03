import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
file_path = 'data_2017.xlsx'  # Ganti dengan path file Anda
df = pd.read_excel(file_path, skiprows=1)  # Abaikan header tambahan

# Bersihkan dan atur ulang kolom
df.columns = [
    "Pintu Masuk", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember", "Tahunan"
]
numeric_columns = df.columns[2:]  # Kolom angka (Januari hingga Tahunan)
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Filtering berdasarkan kategori jalur
kategori_jalur = st.sidebar.selectbox(
    "Pilih Kategori Jalur",
    ["A. Pintu Udara", "B. Pintu Laut", "C. Pintu Darat"]
)

if kategori_jalur == "A. Pintu Udara":
    df_filtered_jalur = df.iloc[0:16]  # Baris 0 hingga 17
elif kategori_jalur == "B. Pintu Laut":
    df_filtered_jalur = df.iloc[17:24]  # Baris 19 hingga 25
elif kategori_jalur == "C. Pintu Darat":
    df_filtered_jalur = df.iloc[25:31]  # Baris 27 hingga 32

# Pilih pintu masuk spesifik berdasarkan jalur
pintu_pilihan = st.sidebar.selectbox(
    "Pilih Nama Pintu Masuk",
    df_filtered_jalur["Pintu Masuk"].unique()
)

# Filter data berdasarkan pilihan pintu masuk
data_filtered = df_filtered_jalur[df_filtered_jalur["Pintu Masuk"] == pintu_pilihan]

# Visualisasi Data
st.title("Analisis Kunjungan Wisata Mancanegara")
st.subheader(f"Distribusi Wisatawan di Pintu Masuk: {pintu_pilihan}")

# Visualisasi kunjungan tahunan
st.write(f"**Total Kunjungan Tahunan di {pintu_pilihan}:** {data_filtered['Tahunan'].values[0]:,.2f}")

# Visualisasi distribusi bulanan
bulan_data = data_filtered.iloc[0, 2:-1].reset_index()
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
    total_data = df_filtered_jalur.groupby("Pintu Masuk")["Tahunan"].sum().reset_index()
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
    corr_matrix = df_filtered_jalur[numeric_columns[:-1]].corr()  # Kecualikan kolom Tahunan
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Matriks Korelasi Antar Bulan")
    st.pyplot()
