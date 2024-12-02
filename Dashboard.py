import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
file_path = "all_data.csv"
data = pd.read_csv(file_path)

# Streamlit UI
st.title("Dashboard Data Kunjungan")

# Dropdown untuk memilih jalur masuk
options = ["Laut", "Darat", "Udara"]
selected_option = st.selectbox("Pilih Jalur Masuk:", options)

# Menyesuaikan data berdasarkan jalur masuk
if selected_option == "Laut":
    df = data[["Jalur masuk Laut", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
               "Juli", "Agustus", "September", "Oktober", "November", "Desember", "Total_Laut"]]
    df.rename(columns={"Jalur masuk Laut": "Jalur Masuk", "Total_Laut": "Total"}, inplace=True)
elif selected_option == "Darat":
    df = data[["Jalur masuk Darat", "Januari.1", "Februari.1", "Maret.1", "April.1", "Mei.1", "Juni.1",
               "Juli.1", "Agustus.1", "September.1", "Oktober.1", "November.1", "Desember.1", "Total_Darat"]]
    df.rename(columns={"Jalur masuk Darat": "Jalur Masuk", "Total_Darat": "Total"}, inplace=True)
    df.columns = df.columns.str.replace(r"\.\d+$", "", regex=True)
else:
    df = data[["Jalur masuk Udara", "Januari.2", "Februari.2", "Maret.2", "April.2", "Mei.2", "Juni.2",
               "Juli.2", "Agustus.2", "September.2", "Oktober.2", "November.2", "Desember.2", "Total_Udara"]]
    df.rename(columns={"Jalur masuk Udara": "Jalur Masuk", "Total_Udara": "Total"}, inplace=True)
    df.columns = df.columns.str.replace(r"\.\d+$", "", regex=True)

# Menampilkan ringkasan data
st.write(f"Ringkasan Data Jalur Masuk: **{selected_option}**")
st.dataframe(df)

# Grafik kunjungan bulanan
month_columns = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                 "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

df_melted = df.melt(id_vars=["Jalur Masuk"], value_vars=month_columns,
                    var_name="Bulan", value_name="Kunjungan")

fig = px.line(df_melted, x="Bulan", y="Kunjungan", color="Jalur Masuk",
              title=f"Grafik Kunjungan Bulanan ({selected_option})")
st.plotly_chart(fig)

# Total kunjungan
total_kunjungan = df["Total"].sum()
st.metric(label="Total Kunjungan", value=f"{total_kunjungan:,}")
