import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
jalur_laut = pd.read_excel('kunjungan_wisata_mancanegara_laut.xlsx')
jalur_darat = pd.read_excel('kunjungan_wisata_mancanegara_darat.xlsx')
jalur_udara = pd.read_excel('kunjungan_wisata_mancanegara_udara.xlsx')

# Cleaning data
jalur_laut['Tahunan'] = jalur_laut.loc[:, 'Januari':'Agustus'].sum(axis=1)
jalur_darat['Tahunan'] = jalur_darat.loc[:, 'Januari':'Agustus'].sum(axis=1)
jalur_udara['Tahunan'] = jalur_udara.loc[:, 'Januari':'Agustus'].sum(axis=1)

# Sidebar filters
st.sidebar.title("Filters")
view_option = st.sidebar.selectbox("View Data By:", ["All Routes", "Sea Route", "Land Route", "Air Route"])

# Display data
st.title("Tourism Data Dashboard")
if view_option == "All Routes":
    total_laut = jalur_laut['Tahunan'].sum()
    total_darat = jalur_darat['Tahunan'].sum()
    total_udara = jalur_udara['Tahunan'].sum()

    # Plot total visits per route
    st.subheader("Total Visits Per Route (January - August)")
    fig, ax = plt.subplots()
    ax.bar(["Sea Route", "Land Route", "Air Route"], [total_laut, total_darat, total_udara], color=["blue", "green", "red"])
    ax.set_ylabel("Total Visits")
    st.pyplot(fig)

elif view_option == "Sea Route":
    st.subheader("Sea Route Data")
    st.dataframe(jalur_laut)

elif view_option == "Land Route":
    st.subheader("Land Route Data")
    st.dataframe(jalur_darat)

elif view_option == "Air Route":
    st.subheader("Air Route Data")
    st.dataframe(jalur_udara)
