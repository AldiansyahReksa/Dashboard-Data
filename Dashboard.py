import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
file_path_laut = 'kunjungan_wisata_mancanegara_laut.csv'
file_path_darat = 'kunjungan_wisata_mancanegara_darat.csv'
file_path_udara = 'kunjungan_wisata_mancanegara_udara.csv'

# Load data (menggunakan read_csv untuk file CSV)
jalur_laut = pd.read_csv(file_path_laut)
jalur_darat = pd.read_csv(file_path_darat)
jalur_udara = pd.read_csv(file_path_udara)

# Menambah kolom tahunan untuk setiap data
jalur_laut['Tahunan'] = jalur_laut.loc[:, 'Januari':'Agustus'].sum(axis=1)
jalur_darat['Tahunan'] = jalur_darat.loc[:, 'Januari':'Agustus'].sum(axis=1)
jalur_udara['Tahunan'] = jalur_udara.loc[:, 'Januari':'Agustus'].sum(axis=1)

# Streamlit Layout
st.title("Dashboard Data Kunjungan Wisata Mancanegara")

# Widget untuk memilih jalur masuk
jalur_pilihan = st.selectbox(
    "Pilih Jalur Masuk",
    ["Laut", "Darat", "Udara"]
)

# Menyesuaikan data berdasarkan pilihan
if jalur_pilihan == "Laut":
    df = jalur_laut
    jalur_label = "Jalur masuk Laut"
elif jalur_pilihan == "Darat":
    df = jalur_darat
    jalur_label = "Jalur masuk Darat"
else:
    df = jalur_udara
    jalur_label = "Jalur masuk Udara"

# Menampilkan ringkasan data
st.subheader(f"Ringkasan Data Jalur Masuk: **{jalur_pilihan}**")
df_rename = df.rename(columns={jalur_label: "Jalur Masuk", "Tahunan": "Total Kunjungan"})
st.dataframe(df_rename)

# Grafik kunjungan bulanan
month_columns = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus"]
df_melted = df[month_columns].sum().reset_index()
df_melted.columns = ["Bulan", "Kunjungan"]

fig = px.line(df_melted, x="Bulan", y="Kunjungan", title=f"Grafik Kunjungan Bulanan ({jalur_pilihan})")
st.plotly_chart(fig)

# Total kunjungan
total_kunjungan = df["Tahunan"].sum()
st.metric(label="Total Kunjungan", value=f"{total_kunjungan:,}")

# Menampilkan statistik lainnya
st.sidebar.title("Analisis Lanjutan")

# Widget pemilihan bulan untuk analisis
bulan_pilihan = st.sidebar.multiselect(
    "Pilih Bulan untuk Analisis",
    list(df.columns)[1:-1],  # Mengambil bulan dari kolom (menghindari 'Jalur Masuk' dan 'Total')
    default=["Januari"]
)

if bulan_pilihan:
    df_bulan = df[bulan_pilihan].sum().reset_index()
    df_bulan.columns = ["Bulan", "Total Kunjungan"]
    
    # Visualisasi bulan
    st.subheader("Distribusi Kunjungan Berdasarkan Bulan")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_bulan, x="Bulan", y="Total Kunjungan", ax=ax)
    ax.set_title("Distribusi Kunjungan Wisata Berdasarkan Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Kunjungan")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Widget untuk menampilkan total kunjungan
st.sidebar.subheader("Tampilkan Total Kunjungan")
if st.sidebar.checkbox("Tampilkan Total Kunjungan untuk Semua Jalur"):
    total_laut = jalur_laut['Tahunan'].sum()
    total_darat = jalur_darat['Tahunan'].sum()
    total_udara = jalur_udara['Tahunan'].sum()

    st.subheader("Total Kunjungan Wisata Tahunan (Semua Jalur)")
    total_data = {
        "Jalur": ["Laut", "Darat", "Udara"],
        "Total Kunjungan": [total_laut, total_darat, total_udara]
    }
    total_df = pd.DataFrame(total_data)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=total_df, x="Jalur", y="Total Kunjungan", ax=ax, palette="viridis")
    ax.set_title("Total Kunjungan Wisata per Jalur Masuk")
    ax.set_xlabel("Jalur Masuk")
    ax.set_ylabel("Total Kunjungan")
    st.pyplot(fig)
