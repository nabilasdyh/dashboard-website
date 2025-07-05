# 🚗 Dashboard Data Kendaraan & Prediksi Harga

Aplikasi web interaktif berbasis Streamlit untuk menganalisis data penjualan kendaraan dan memprediksi harga mobil. 
Dibangun menggunakan Python, pandas, scikit-learn, dan dideploy di Streamlit Cloud.

🔗 **Aplikasi Live**: [dashboard-vehicle.streamlit.app](https://dashboard-vehicle.streamlit.app)  
📦 **Repositori GitHub**: [github.com/nabilasdyh/dashboard-website](https://github.com/nabilasdyh/dashboard-website)

---

## Page/Fitur

### 🔍 Analisis Data
- Filter berdasarkan **Merek**, **Tipe Bodi**, dan **Tahun Produksi**
- Menampilkan metrik utama:
  - 💸 Total Penjualan
  - 🚘 Total Unit Terjual
  - 💰 Rata-rata Harga
- Visualisasi:
  - Distribusi Harga
  - Unit Terjual per Tahun
  - Komposisi Tipe Bodi (Donut Chart)
  - Rata-rata Harga berdasarkan Jumlah Pintu
- Sorotan Bahan Bakar:
  - Jenis bahan bakar terbanyak yang digunakan
  - Diagram batang horizontal untuk distribusi bahan bakar

### 💰 Prediksi Harga
- Masukkan fitur kendaraan 
- Prediksi estimasi harga kendaraan

---

## 🖼️ Pratinjau

![image](https://github.com/user-attachments/assets/0cf34965-17da-4b69-9ccf-97b04793ca50)


---

## 🧠 Informasi Model

- Disimpan dalam file pickle: `vehicle_bundle.pkl`
  Berisi:
  - Pipeline preprocessing
  - Model terlatih
  - fitur

---

Aplikasi ini dideploy di [Streamlit Community Cloud](https://streamlit.io/cloud).
