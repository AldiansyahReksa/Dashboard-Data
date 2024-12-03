import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Layout
st.sidebar.title("Dashboard Data Kunjungan Wisata")
st.sidebar.write("**Created by Kelompok 3**")

# Filter jalur
jalur_pilihan = st.sidebar.selectbox(
    "Pilih Jalur",
    combined_data["Jalur"].unique()
)

# Filter nama jalur berdasarkan jalur pilihan
nama_jalur_pilihan = st.sidebar.selectbox(
    "Pilih Nama Jalur",
    combined_data[combined_data["Jalur"] == jalur_pilihan]["Pintu Masuk"].unique()
)

# Filter data berdasarkan pilihan
data_filtered = combined_data[
    (combined_data["Jalur"] == jalur_pilihan) &
    (combined_data["Pintu Masuk"] == nama_jalur_pilihan)
]

# Visualisasi Data
st.title("Analisis Kunjungan Wisata Mancanegara")
st.subheader(f"Distribusi Wisatawan di Jalur {jalur_pilihan}: {nama_jalur_pilihan}")

# Visualisasi kunjungan tahunan
st.write(f"**Total Kunjungan Tahunan di {nama_jalur_pilihan}:** {data_filtered['Tahunan'].values[0]:,.2f}")

# Visualisasi distribusi bulanan
bulan_data = data_filtered.iloc[0, 1:-2].reset_index()
bulan_data.columns = ["Bulan", "Total Kunjungan"]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=bulan_data, x="Bulan", y="Total Kunjungan", ax=ax)
ax.set_title(f"Distribusi Kunjungan Bulanan di {nama_jalur_pilihan}")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Kunjungan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Analisis keseluruhan
if st.sidebar.checkbox("Tampilkan Analisis Keseluruhan"):
    st.subheader("Total Kunjungan Wisata untuk Semua Jalur")
    total_data = combined_data.groupby(["Jalur", "Pintu Masuk"])["Tahunan"].sum().reset_index()
    total_data.columns = ["Jalur", "Pintu Masuk", "Total Kunjungan"]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=total_data, x="Pintu Masuk", y="Total Kunjungan", hue="Jalur", ax=ax)
    ax.set_title("Total Kunjungan Wisata per Pintu Masuk")
    ax.set_xlabel("Pintu Masuk")
    ax.set_ylabel("Total Kunjungan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
