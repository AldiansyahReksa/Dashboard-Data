import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# File paths
file_path_laut = "kunjungan wisata mancanegara_laut.xlsx"
file_path_darat = "kunjungan wisata mancanegara_darat.xlsx"
file_path_udara = "kunjungan wisata mancanegara_udara.xlsx"

# Load data
jalur_laut = pd.read_excel(file_path_laut)
jalur_darat = pd.read_excel(file_path_darat)
jalur_udara = pd.read_excel(file_path_udara)

# Menambah kolom tahunan untuk setiap data
jalur_laut["Tahunan"] = jalur_laut.loc[:, "Januari":"Agustus"].sum(axis=1)
jalur_darat["Tahunan"] = jalur_darat.loc[:, "Januari":"Agustus"].sum(axis=1)
jalur_udara["Tahunan"] = jalur_udara.loc[:, "Januari":"Agustus"].sum(axis=1)

# Gabungkan semua data untuk analisis
jalur_laut["Transportasi"] = "Laut"
jalur_darat["Transportasi"] = "Darat"
jalur_udara["Transportasi"] = "Udara"
all_data = pd.concat([jalur_laut, jalur_darat, jalur_udara])

# Streamlit Sidebar
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

# Streamlit Layout
st.title("Dashboard Analisis Kunjungan Wisata Mancanegara")

# Widget Pemilihan Jalur Masuk
jalur_pilihan = st.sidebar.selectbox(
    "Pilih Jalur Masuk",
    ["Semua", "Laut", "Darat", "Udara"]
)

# Filter data berdasarkan pilihan jalur
if jalur_pilihan == "Laut":
    data_filtered = jalur_laut
    jalur_label = "Laut"
elif jalur_pilihan == "Darat":
    data_filtered = jalur_darat
    jalur_label = "Darat"
elif jalur_pilihan == "Udara":
    data_filtered = jalur_udara
    jalur_label = "Udara"
else:
    data_filtered = all_data
    jalur_label = "Semua Jalur"

# Visualisasi Data
st.subheader(f"Distribusi Wisatawan melalui {jalur_label}")

if jalur_label != "Semua Jalur":
    grouped_data = data_filtered.groupby("Transportasi")["Tahunan"].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=grouped_data.index, y=grouped_data.values, ax=ax)
    ax.set_title(f"Distribusi Wisatawan melalui Jalur {jalur_label}")
    ax.set_xlabel("Transportasi")
    ax.set_ylabel("Total Wisatawan")
    st.pyplot(fig)

    # Rata-rata pengunjung tahunan
    st.write(f"**Rata-rata Kunjungan Tahunan Jalur {jalur_label}:** {grouped_data.mean():,.2f}")
else:
    total_kunjungan = all_data.groupby("Transportasi")["Tahunan"].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=total_kunjungan.index, y=total_kunjungan.values, ax=ax, palette="viridis")
    ax.set_title("Total Kunjungan Wisata per Jalur Masuk")
    ax.set_xlabel("Jalur Masuk")
    ax.set_ylabel("Total Kunjungan")
    st.pyplot(fig)

# Widget untuk bulan analisis
bulan_pilihan = st.sidebar.multiselect(
    "Pilih Bulan untuk Analisis",
    list(data_filtered.loc[:, "Januari":"Agustus"].columns),
    default=["Januari"]
)

if bulan_pilihan:
    data_bulan = data_filtered[bulan_pilihan].sum().reset_index()
    data_bulan.columns = ["Bulan", "Total Kunjungan"]

    # Visualisasi bulan
    st.subheader("Distribusi Kunjungan Berdasarkan Bulan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data_bulan, x="Bulan", y="Total Kunjungan", ax=ax)
    ax.set_title("Distribusi Kunjungan Wisata Berdasarkan Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Kunjungan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
else:
    st.warning("Pilih minimal satu bulan untuk analisis.")

# Total Kunjungan Semua Jalur
if st.sidebar.checkbox("Tampilkan Total Kunjungan Semua Jalur"):
    total_laut = jalur_laut["Tahunan"].sum()
    total_darat = jalur_darat["Tahunan"].sum()
    total_udara = jalur_udara["Tahunan"].sum()

    st.subheader("Total Kunjungan Wisata Tahunan (Semua Jalur)")
    total_data = {
        "Jalur": ["Laut", "Darat", "Udara"],
        "Total Kunjungan": [total_laut, total_darat, total_udara]
    }
    total_df = pd.DataFrame(total_data)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=total_df, x="Jalur", y="Total Kunjungan", ax=ax, palette="muted")
    ax.set_title("Total Kunjungan Wisata per Jalur Masuk")
    ax.set_xlabel("Jalur Masuk")
    ax.set_ylabel("Total Kunjungan")
    st.pyplot(fig)
