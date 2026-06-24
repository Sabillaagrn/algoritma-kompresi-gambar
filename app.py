"""
app.py - Aplikasi utama (Streamlit)
Studi Komparasi Algoritma Kompresi Gambar JPEG
"""

import pandas as pd
import streamlit as st
from PIL import Image

from compression_lib import ALGORITMA
from utils import size_kb, compression_ratio, space_savings, psnr

# Konfigurasi Halaman
st.set_page_config(
    page_title="Komparasi Kompresi JPEG",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- Kumpulan Ikon SVG ------------------------------------------------------
SVG_SPARKLES = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>'
SVG_BOX = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'
SVG_BLOCKS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>'
SVG_ZAP = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
SVG_FILE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>'
SVG_RULER = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
SVG_DISK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
SVG_IMAGE = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'

# ---- Gaya Tampilan (CSS Modern & Adaptif) -----------------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
      html, body, [class*="css"] {
          font-family: 'Plus Jakarta Sans', sans-serif;
      }
      
      .svg-icon {
          vertical-align: text-bottom;
          margin-right: 6px;
      }

      /* Hero section tetap menggunakan warna gelap sebagai aksen */
      .hero {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #ffffff; 
        padding: 3rem 2.5rem; 
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        text-align: center;
      }
      .hero h1 { color:#fff; font-size: 2.2rem; font-weight: 700; margin: 0 0 0.8rem 0; display: flex; align-items: center; justify-content: center;}
      .hero p { color:#cbd5e1; font-size: 1.1rem; margin: 0 auto 1.5rem auto; max-width: 800px; line-height: 1.6;}
      
      .algo-pill {
        display: inline-flex; 
        align-items: center;
        background: rgba(255,255,255, 0.1);
        border: 1px solid rgba(255,255,255, 0.2);
        color:#fff; 
        padding: 0.5rem 1.2rem; 
        border-radius: 50px;
        font-size: 0.9rem; 
        font-weight: 500;
        margin: 0.3rem;
      }

      /* Teks menggunakan var(--text-color) agar adaptif di Light/Dark Mode */
      .filename { font-weight: 600; font-size: 1.15rem; color: var(--text-color); display: flex; align-items: center;}
      .muted { color: var(--text-color); opacity: 0.7; font-size:0.9rem; margin-bottom: 0.2rem; display: flex; align-items: center;}
      .size-orig { font-size: 1rem; color: var(--text-color); font-weight: 600;}
      
      /* Menggunakan border semi-transparan untuk gambar */
      [data-testid="stImage"] img {
          border-radius: 8px;
          border: 1px solid rgba(128, 128, 128, 0.2);
      }
      
      /* Metric container menyesuaikan warna background tema Streamlit */
      [data-testid="metric-container"] {
          background-color: var(--secondary-background-color);
          border: 1px solid rgba(128, 128, 128, 0.2);
          padding: 1rem;
          border-radius: 10px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Bagian Header (Hero) ---------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
      <h1>{SVG_SPARKLES} Studi Komparasi Kompresi Gambar JPG/JPEG</h1>
      <p>Analisis dan bandingkan tiga algoritma kompresi citra terhadap ukuran file dan
      kualitas visual (PSNR). Unggah gambar Anda untuk melihat hasilnya.</p>
      <div>
          <span class="algo-pill">{SVG_BOX} Vector Quantization</span>
          <span class="algo-pill">{SVG_BLOCKS} Block Truncation</span>
          <span class="algo-pill">{SVG_ZAP} Progressive JPEG</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Area Unggah File -------------------------------------------------------
st.markdown("### Mulai di sini")
files = st.file_uploader(
    "Pilih satu atau beberapa gambar (.jpg / .jpeg)",
    type=["jpg", "jpeg"],
    accept_multiple_files=True,
    help="Tarik dan letakkan file gambar ke area ini."
)

if not files:
    st.info("Belum ada file yang diunggah. Silakan pilih gambar di atas untuk memulai perbandingan.")
    st.stop()

# ---- Proses tiap file -------------------------------------------------------
ringkasan = []

st.success(f"**{len(files)} file** siap diproses.")
st.write("")

for idx, f in enumerate(files):
    data_asli = f.getvalue()
    img = Image.open(f)
    kb_asli = size_kb(data_asli)

    with st.container(border=True):
        st.markdown(
            f'<div class="filename">{SVG_FILE} {f.name}</div> '
            f'<div class="muted" style="margin-top: 8px;">{SVG_RULER} {img.width} x {img.height} px '
            f'&nbsp;&nbsp;|&nbsp;&nbsp; {SVG_DISK} Ukuran asli: {kb_asli:.1f} KB</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        kolom = st.columns(len(ALGORITMA) + 1)

        # 1. Kolom Gambar Asli
        with kolom[0]:
            st.image(img, use_container_width=True)
            st.markdown(f'<p class="muted">{SVG_IMAGE} Asli (Sebelum Kompresi)</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="size-orig">{kb_asli:.1f} KB</p>', unsafe_allow_html=True)

        baris = {"File": f.name, "Asli (KB)": round(kb_asli, 1)}
        hasil_kompresi = []

        # 2. Kolom Hasil Algoritma
        for i, (nama, fungsi, ext) in enumerate(ALGORITMA, start=1):
            data = fungsi(img)
            kb = size_kb(data)
            ss = space_savings(data_asli, data)
            cr = compression_ratio(data_asli, data)
            ps = psnr(img, data)
            hasil_kompresi.append((nama, data, kb))

            with kolom[i]:
                st.image(data, use_container_width=True)
                st.markdown(f'<p class="muted">{SVG_ZAP} {nama}</p>', unsafe_allow_html=True)
                
                st.metric(
                    label="Ukuran Akhir",
                    value=f"{kb:.1f} KB",
                    delta=f"{ss:.1f}% hemat",
                    delta_color="normal" if ss > 0 else "inverse",
                )
                
                st.markdown(
                    f'<p class="muted" style="font-size: 0.85rem;">'
                    f'Rasio: {cr:.2f}x <br> '
                    f'PSNR: {"inf" if ps == float("inf") else f"{ps:.1f}"} dB</p>',
                    unsafe_allow_html=True,
                )
                
                st.download_button(
                    label="Unduh",
                    data=data,
                    file_name=f"algo{i}_{f.name.rsplit('.', 1)[0]}.{ext}",
                    key=f"dl_{idx}_{i}",
                    use_container_width=True,
                    type="primary"
                )

            baris[f"Algo {i} (KB)"] = round(kb, 1)
            baris[f"Algo {i} Reduksi (%)"] = round(ss, 1)

        best = min(hasil_kompresi, key=lambda x: x[2])
        baris["Pemenang"] = best[0]
        ringkasan.append(baris)

# ---- Rekap & Komparasi ------------------------------------------------------
st.write("---")
st.markdown("### Ringkasan & Analisis Data")

df = pd.DataFrame(ringkasan)

st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
)

st.write("")

col_a, col_b = st.columns(2)
with col_a:
    with st.container(border=True):
        st.markdown("**Rata-rata Ukuran per Algoritma (KB)**")
        rata = {f"Algo {i}": df[f"Algo {i} (KB)"].mean() for i in (1, 2, 3)}
        # Menghapus argumen color supaya bar_chart menggunakan warna tema bawaan Streamlit
        st.bar_chart(pd.Series(rata, name="KB"))

with col_b:
    with st.container(border=True):
        st.markdown("**Rata-rata Penghematan per Algoritma (%)**")
        rata_ss = {f"Algo {i}": df[f"Algo {i} Reduksi (%)"].mean() for i in (1, 2, 3)}
        st.bar_chart(pd.Series(rata_ss, name="Reduksi (%)"))

col1, col2 = st.columns([1, 3])
with col1:
    st.download_button(
        label="Unduh Laporan (CSV)",
        data=df.to_csv(index=False).encode(),
        file_name="compression_results.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.caption(
        "Keterangan: Algo 1 = Vector Quantization | Algo 2 = Block Truncation Coding | "
        "Algo 3 = Progressive JPEG. Kolom 'Pemenang' dipilih otomatis berdasarkan ukuran file terkecil."
    )