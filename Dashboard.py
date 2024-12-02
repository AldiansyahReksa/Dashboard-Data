import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# File paths
file_path_laut = 'kunjungan wisata mancanegara_laut.xlsx'
file_path_darat = 'kunjungan wisata mancanegara_darat.xlsx'
file_path_udara = 'kunjungan wisata mancanegara_udara.xlsx'

# Load data
df_laut = pd.read_excel(file_path_laut)
df_darat = pd.read_excel(file_path_darat)
df_udara = pd.read_excel(file_path_udara)

# Menambah kolom tahunan untuk setiap data
df_laut['Tahunan'] = df_laut.loc[:, 'Januari':'Agustus'].sum(axis=1)
df_darat['Tahunan'] = df_darat.loc[:, 'Januari':'Agustus'].sum(axis=1)
df_udara['Tahunan'] = df_udara.loc[:, 'Januari':'Agustus'].sum(axis=1)

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

# Pilih Jalur Masuk
jalur_pilihan = st.sidebar.selectbox(
    "Pilih Jalur Masuk",
    ["Laut", "Darat", "Udara"]
)

# Filter data berdasarkan jalur pilihan
if jalur_pilihan == "Laut":
    data_filtered = df_laut
    jalur_label = "Jalur masuk Laut"
elif jalur_pilihan == "Darat":
    data_filtered = df_darat
    jalur_label = "Jalur masuk Darat"
else:
    data_filtered = df_udara
    jalur_label = "Jalur masuk Udara"

# Filter data (exclude total rows jika ada kolom jalur)
if jalur_label in data_filtered.columns:
    data_filtered = data_filtered[data_filtered[jalur_label].str.lower() != 'total']

# Visualisasi Data
st.title("Analisis Kunjungan Wisata Mancanegara")
st.subheader(f"Distribusi Wisatawan melalui {jalur_pilihan}")

# Grup data berdasarkan jalur masuk
grouped_data = data_filtered.groupby(jalur_label)['Tahunan'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=grouped_data.index, y=grouped_data.values, ax=ax)
ax.set_title(f"Distribusi Wisatawan melalui Jalur Masuk {jalur_pilihan}")
ax.set_xlabel("Jalur Masuk")
ax.set_ylabel("Total Wisatawan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Rata-rata pengunjung tahunan
st.write(f"**Rata-rata Kunjungan Tahunan Jalur {jalur_pilihan}:** {grouped_data.mean():,.2f}")

# Widget untuk bulan analisis
bulan_pilihan = st.sidebar.multiselect(
    "Pilih Bulan untuk Analisis",
    list(data_filtered.loc[:, 'Januari':'Agustus'].columns),
    default=['Januari']
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

# Analisis Total Kunjungan
st.sidebar.subheader("Tampilkan Total Kunjungan")
if st.sidebar.checkbox("Total Semua Jalur"):
    total_laut = df_laut['Tahunan'].sum()
    total_darat = df_darat['Tahunan'].sum()
    total_udara = df_udara['Tahunan'].sum()

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

# Menambahkan fitur baru

# Distribusi Kunjungan per Bulan
st.sidebar.subheader("Distribusi Kunjungan per Bulan")
if st.sidebar.checkbox("Tampilkan Distribusi Kunjungan per Bulan"):
    st.subheader("Distribusi Total Kunjungan per Bulan untuk Semua Jalur")
    monthly_visits = df_laut.groupby('Januari').sum()['Tahunan'].append(
        df_darat.groupby('Januari').sum()['Tahunan']).append(df_udara.groupby('Januari').sum()['Tahunan'])
    monthly_visits = monthly_visits.reset_index()
    monthly_visits.columns = ['Bulan', 'Total Kunjungan']
    sns.barplot(x="Bulan", y="Total Kunjungan", data=monthly_visits)
    plt.title("Distribusi Kunjungan per Bulan")
    st.pyplot()

# Korelasi Antar-Jalur
st.sidebar.subheader("Korelasi Antar Jalur")
if st.sidebar.checkbox("Tampilkan Korelasi Antar Jalur"):
    df_all = pd.concat([df_laut[['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus']],
                        df_darat[['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus']],
                        df_udara[['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus']]], axis=1)
    
    corr_matrix = df_all.corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Matriks Korelasi Antar Jalur")
    st.pyplot()

# Trend Kunjungan per Jalur
st.sidebar.subheader("Trend Kunjungan per Jalur")
if st.sidebar.checkbox("Tampilkan Trend Kunjungan per Jalur"):
    selected_jalur = st.selectbox('Pilih Jalur untuk Trend', ['Laut', 'Darat', 'Udara'])
    if selected_jalur == 'Laut':
        df_selected = df_laut
    elif selected_jalur == 'Darat':
        df_selected = df_darat
    else:
        df_selected = df_udara
    
    trend_data = df_selected[['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus']].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    trend_data.plot(kind='line', ax=ax)
    ax.set_title(f"Trend Kunjungan per Bulan - Jalur {selected_jalur}")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Kunjungan")
    st.pyplot()

# Prediksi Kunjungan Bulan Berikutnya
st.sidebar.subheader("Prediksi Kunjungan")
if st.sidebar.checkbox("Prediksi Kunjungan Bulan Berikutnya"):
    selected_jalur = st.selectbox('Pilih Jalur untuk Prediksi', ['Laut', 'Darat', 'Udara'])
    if selected_jalur == 'Laut':
        df_selected = df_laut
    elif selected_jalur == 'Darat':
        df_selected = df_darat
    else:
        df_selected = df_udara
    
    monthly_data = df_selected[['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus']].sum()
    X = list(range(1, 9))  # Bulan 1-8
    y = monthly_data.values

    # Linear regression untuk prediksi
    X = pd.DataFrame(X)
    model = LinearRegression()
    model.fit(X, y)
    next_month = model.predict([[9]])  # Prediksi untuk bulan 9

    st.write(f"Prediksi Kunjungan Bulan 9 (September) untuk Jalur {selected_jalur}: {next_month[0]:,.2f}")
