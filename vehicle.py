#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Vehicle Dashboard", page_icon="🚗", layout="wide")

# Load model dan metadata
with open('vehicle_bundle.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
feature_cols = bundle['features']
categorical_cols = bundle['categorical_cols']

# Load dataset
df = pd.read_csv('vehicles_dataset_clean.csv')

# Sidebar
st.sidebar.title("🔍 Filter Kendaraan")
selected_make = st.sidebar.multiselect("Pilih Merek", options=df['make'].unique(), default=df['make'].unique())
selected_body = st.sidebar.multiselect("Pilih Tipe Bodi", options=df['body'].unique(), default=df['body'].unique())
selected_year = st.sidebar.slider("Tahun Produksi", int(df['year'].min()), int(df['year'].max()), (2020, 2024))

filtered_df = df[
    (df['make'].isin(selected_make)) &
    (df['body'].isin(selected_body)) &
    (df['year'].between(*selected_year))
]

# Navigasi
page = st.sidebar.radio("📂 Navigasi", ["📊 Data Analysis", "💰 Price Prediction"])

# ============================
# TAB 1: DATA ANALYSIS
# ============================
if page == "📊 Data Analysis":
    main_col, fuel_col = st.columns([3, 1])
    with main_col:
        st.title("📊 Vehicle Data Analysis")
    
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💸 Total Penjualan", f"${filtered_df['price'].sum():,.0f}")
        with col2:
            st.metric("🚘 Total Unit Terjual", f"{len(filtered_df):,}")
        with col3:
            st.metric("💰 Rata-rata Harga", f"${filtered_df['price'].mean():,.0f}")
    
        st.markdown("---")

    # ============================
    # 📊 Baris 1: Distribusi Harga & Unit Terjual per Tahun
    # ============================
    
        st.markdown("### 📈 Distribusi Harga & Unit Terjual per Tahun")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribusi Harga")
            fig1, ax1 = plt.subplots(figsize=(5, 3))
            sns.histplot(filtered_df['price'], bins=30, kde=True, ax=ax1, color='skyblue')
            ax1.set_xlabel("Harga")
            ax1.set_ylabel("Jumlah")
            st.pyplot(fig1)
        
        with col2:
            st.subheader("Unit Terjual per Tahun")
            year_counts = filtered_df['year'].astype(int).value_counts().sort_index()
            fig2, ax2 = plt.subplots(figsize=(5, 3))
            sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax2, palette='Blues_d')
            ax2.set_xlabel("Tahun")
            ax2.set_ylabel("Jumlah Unit")
            st.pyplot(fig2)
        
        # ============================
        # 📊 Baris 2: Komposisi Tipe Bodi & Harga vs Doors
        # ============================
        st.markdown("### 🚘 Komposisi Tipe Bodi & Harga vs Jumlah Pintu")
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Komposisi Tipe Bodi")
            body_counts = filtered_df['body'].value_counts()
        
            fig3, ax3 = plt.subplots(figsize=(5, 3))
            wedges, _ = ax3.pie(
                body_counts.values,
                startangle=90,
                wedgeprops=dict(width=0.4)  # Ini yang bikin jadi donut
            )
            ax3.legend(
                wedges,
                body_counts.index,
                title="Tipe Bodi",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )
            ax3.axis('equal')
            st.pyplot(fig3)
    
    
        with col4:
            st.subheader("Harga Rata-rata Berdasarkan Jumlah Pintu")
            avg_price_doors = filtered_df.groupby('doors')['price'].mean().sort_index()
            fig4, ax4 = plt.subplots(figsize=(5, 3))
            sns.barplot(x=avg_price_doors.index.astype(int), y=avg_price_doors.values, palette='Set2', ax=ax4)
            ax4.set_xlabel("Jumlah Pintu")
            ax4.set_ylabel("Rata-rata Harga")
            st.pyplot(fig4)
        # Tambahkan garis horizontal sebagai pemisah antar bagian
        st.markdown("---")

        
    with fuel_col:
        st.markdown("### 🔦 Bahan Bakar")
        fuel_counts = filtered_df['fuel'].value_counts()
        top_fuel = fuel_counts.idxmax()
        top_count = fuel_counts.max()
            
        st.metric(label="🔋 Jenis Bahan Bakar Terbanyak", value=top_fuel)
        st.metric(label="🚘 Jumlah Unit", value=f"{top_count:,}")
            
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = sns.barplot(
            y=fuel_counts.index,
            x=fuel_counts.values,
            palette='Set2',
            ax=ax
            )
            
        # label angka di ujung bar
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge', padding=3)
            
        # Hilangkan sumbu X dan garis-garisnya
        ax.set_xlabel("")
        ax.set_xlim(0, fuel_counts.values.max() * 1.2)
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
        sns.despine(left=True, bottom=True)
            
        # Hilangkan garis grid horizontal
        ax.grid(False)
            
        st.pyplot(fig)


    # --- Eksplorasi Data Mentah (Expander) ---
    st.subheader("🔬 Eksplorasi Data Mentah")

    # Buat area yang bisa diklik untuk expand/collapse
    with st.expander("Klik untuk melihat detail data transaksi"):

        # Penjelasan singkat
        st.write("Berikut adalah sebagian kecil dari data transaksi yang digunakan untuk dashboard ini.")
        
        # Slider untuk memilih berapa banyak baris data yang ingin ditampilkan
        num_rows_to_display = st.slider(
            "Jumlah Baris Data yang Ditampilkan:",
            min_value=10, # Nilai terkecil yang bisa dipilih pengguna (slider mulai dari angka 10)
            max_value=200, # Nilai terbesar yang bisa dipilih pengguna (slider mentok di 200)
            value=50, # Nilai default saat slider muncul pertama kali
            step=10 # Jarak antar nilai pada slider (misalnya: 10, 20, 30, ..., 200)
        )

        # Tampilkan tabel data sesuai jumlah baris yang dipilih
        st.dataframe(filtered_df.head(num_rows_to_display))
        
        # Tampilkan statistik deskriptif (count, mean, std, min, max, dsb)
        st.write("Statistik Deskriptif:")
        st.dataframe(filtered_df.describe())


# ============================
# TAB 2: PRICE PREDICTION
# ============================
else:
    st.title("💰 Prediksi Harga Kendaraan")

    st.write("Isi detail kendaraan di bawah ini untuk memprediksi harganya:")

    input_data = {}
    for col in feature_cols:
        if col in categorical_cols:
            options = sorted(df[col].dropna().unique())
            input_data[col] = st.selectbox(f"{col}", options)
        elif col == 'year':
            input_data[col] = st.selectbox("year", list(range(2020, 2031)))
        elif col == 'doors':
            input_data[col] = st.selectbox("doors", [2, 3, 4, 5])
        else:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            mean_val = float(df[col].mean())
            input_data[col] = st.slider(f"{col}", min_val, max_val, mean_val)

    input_df = pd.DataFrame([input_data])

    if st.button("🔮 Prediksi Harga"):
        prediction = model.predict(input_df)[0]
        st.success(f"💸 Estimasi Harga Kendaraan: **${prediction:,.2f}**")


# In[ ]:




