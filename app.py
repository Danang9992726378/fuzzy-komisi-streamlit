import streamlit as st
from PIL import Image

# ---------- Header ----------
st.set_page_config(page_title="Prediksi Harga Layanan", page_icon="🚚", layout="centered")
st.title("🚚 Prediksi Harga Layanan Berbasis Fuzzy Sugeno")
st.markdown("""
Gunakan aplikasi ini untuk memperkirakan **harga layanan pengiriman** berdasarkan jarak, suhu cuaca, dan jumlah barang.
""")

# ---------- Gambar Ilustrasi ----------
image = Image.open("logistik.jpg")  # Pastikan file logistik.jpg berada di direktori yang sama
st.image(image, caption="Ilustrasi Layanan Pengiriman", use_column_width=True)

# ---------- Fungsi Fuzzy ----------
def jarak_dekat(x): return max(0, min(1, (5 - x) / 5))
def jarak_sedang(x):
    if 5 < x <= 10:
        return (x - 5) / 5
    elif 10 < x <= 11:
        return (11 - x) / 1
    return 0
def jarak_jauh(x): return max(0, min(1, (x - 10) / 10))

def cuaca_hujan(suhu): return 1 if suhu <= 24 else 0
def cuaca_berawan(suhu): return 1 if 25 <= suhu <= 28 else 0
def cuaca_panas(suhu): return 1 if suhu > 28 else 0

def barang_sedikit(x): return max(0, min(1, (1.5 - x) / 1.5))
def barang_sedang(x):
    if 1 < x < 3:
        return 1 - abs(2 - x)
    return 0
def barang_banyak(x): return max(0, min(1, (x - 1.5) / 1.5))

def hitung_komisi_sugeno(jarak, suhu, barang):
    µ_jd = jarak_dekat(jarak)
    µ_js = jarak_sedang(jarak)
    µ_jj = jarak_jauh(jarak)

    µ_hujan = cuaca_hujan(suhu)
    µ_berawan = cuaca_berawan(suhu)
    µ_panas = cuaca_panas(suhu)

    µ_bs = barang_sedikit(barang)
    µ_bsd = barang_sedang(barang)
    µ_bb = barang_banyak(barang)

    rules = [
        (min(µ_jd, µ_hujan, µ_bs), 7000), (min(µ_jd, µ_hujan, µ_bsd), 8000), (min(µ_jd, µ_hujan, µ_bb), 9000),
        (min(µ_jd, µ_berawan, µ_bs), 8500), (min(µ_jd, µ_berawan, µ_bsd), 9500), (min(µ_jd, µ_berawan, µ_bb), 10500),
        (min(µ_jd, µ_panas, µ_bs), 10000), (min(µ_jd, µ_panas, µ_bsd), 11000), (min(µ_jd, µ_panas, µ_bb), 12000),
        (min(µ_js, µ_hujan, µ_bs), 9500), (min(µ_js, µ_hujan, µ_bsd), 10500), (min(µ_js, µ_hujan, µ_bb), 11500),
        (min(µ_js, µ_berawan, µ_bs), 11000), (min(µ_js, µ_berawan, µ_bsd), 12000), (min(µ_js, µ_berawan, µ_bb), 13000),
        (min(µ_js, µ_panas, µ_bs), 12500), (min(µ_js, µ_panas, µ_bsd), 13500), (min(µ_js, µ_panas, µ_bb), 15000),
        (min(µ_jj, µ_hujan, µ_bs), 15000), (min(µ_jj, µ_hujan, µ_bsd), 17000), (min(µ_jj, µ_hujan, µ_bb), 19000),
        (min(µ_jj, µ_berawan, µ_bs), 18000), (min(µ_jj, µ_berawan, µ_bsd), 20000), (min(µ_jj, µ_berawan, µ_bb), 22000),
        (min(µ_jj, µ_panas, µ_bs), 21000), (min(µ_jj, µ_panas, µ_bsd), 23000), (min(µ_jj, µ_panas, µ_bb), 25000),
    ]

    numerator = sum([r[0] * r[1] for r in rules])
    denominator = sum([r[0] for r in rules])
    return 7000 if denominator == 0 else numerator / denominator

def kategori_komisi(harga):
    harga = round(harga)
    if 7000 <= harga <= 10000:
        return "Kecil"
    elif 10000 < harga <= 15000:
        return "Sedang"
    elif 16000 < harga <= 30000:
        return "Besar"
    else:
        return "Tidak Diketahui"

# ---------- Layout Input ----------
st.markdown("## 🔢 Input Data")
col1, col2, col3 = st.columns(3)
with col1:
    jarak = st.number_input("Jarak (km)", min_value=0.0, max_value=20.0, step=0.1)
with col2:
    suhu = st.number_input("Suhu (°C)", min_value=0.0, max_value=40.0, step=0.1)
with col3:
    barang = st.number_input("Jumlah Barang", min_value=0.0, max_value=3.0, step=0.1)

# ---------- Output ----------
if st.button("🚀 Cek Harga"):
    harga = hitung_komisi_sugeno(jarak, suhu, barang)
    kategori = kategori_komisi(harga)

    cuaca = "Hujan" if cuaca_hujan(suhu) else ("Berawan" if cuaca_berawan(suhu) else "Panas")

    st.markdown("""
    ## 🔍 Hasil Prediksi:
    - 🛣️ **Jarak**: {:.1f} km  
    - 🌡️ **Suhu**: {:.1f} °C ({})  
    - 📦 **Jumlah Barang**: {:.1f} item  
    - 💰 **Harga Layanan**: Rp{:,}  
    - 🏷️ **Kategori**: {}
    """.format(jarak, suhu, cuaca, barang, round(harga), kategori))
