import streamlit as st
import pandas as pd

def show_health_dashboard():
    # 2. Fitur Memuat Data
    @st.cache_data
    def load_local_data():
        try:
            df = pd.read_csv("https://drive.google.com/uc?id=1lVkqmIaiBcXtYoHP9M3lSsdrlqIs5sBo")
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            return df
        except FileNotFoundError:
            return None

    df_base = load_local_data()

    if df_base is None:
        st.error("❌ File 'sleep_logs.csv' tidak ditemukan!")
        st.stop()


    # 3. Filter Sidebar
    st.sidebar.header("⚙️ Filter Parameter")


    min_date = df_base['date'].min().to_pydatetime()
    max_date = df_base['date'].max().to_pydatetime()

    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    min_score = float(df_base['quality_score'].min())
    max_score = float(df_base['quality_score'].max())
    selected_score = st.sidebar.slider(
        "Rentang Skor Kualitas Tidur:",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score),
        step=0.1
    )

    # Proses Penyaringan Data Berdasarkan Filter
    df_filtered = df_base[
        (df_base['date'] >= pd.to_datetime(start_date)) & 
        (df_base['date'] <= pd.to_datetime(end_date)) &
        (df_base['quality_score'] >= selected_score[0]) &
        (df_base['quality_score'] <= selected_score[1])
    ].copy()


    # 4. Tampilan Utama Dashboard
    st.title("🌙 Vitara Sleep Scoring Dashboard")
    st.markdown("---")


    # 5. Ringkasan Indikator Kunci (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Log Tidur", value=f"{len(df_filtered):,}")
    with col2:
        avg_duration = df_filtered['duration_hours'].mean() if len(df_filtered) > 0 else 0
        st.metric(label="Rata-rata Durasi", value=f"{avg_duration:.2f} Jam")
    with col3:
        avg_debt = df_filtered['sleep_debt_hours'].mean() if len(df_filtered) > 0 else 0
        st.metric(label="Rata-rata Hutang Tidur", value=f"{avg_debt:.2f} Jam")
    with col4:
        avg_quality = df_filtered['quality_score'].mean() if len(df_filtered) > 0 else 0
        st.metric(label="Rata-rata Skor Kualitas", value=f"{avg_quality:.2f} / 1.0")

    st.markdown("---")

    # Insight & Analsis
    st.header(":bulb: Insight & Analysis")
    
    if len(df_filtered) > 0:
        avg_interruptions = df_filtered['interruptions'].mean()
        max_quality = df_filtered['quality_score'].max()
        min_quality = df_filtered['quality_score'].min()
    
        st.markdown(f"""
        - Pengguna dengan **interupsi tidur lebih sedikit** cenderung memiliki **skor kualitas tidur lebih tinggi**.
        - Rata-rata interupsi tidur pengguna berada di angka **{avg_interruptions:.1f} kali** per malam.
        - Skor kualitas tidur pada data yang difilter berada di rentang **{min_quality:.2f} – {max_quality:.2f}**.
        - Durasi tidur yang lebih lama **tidak selalu menjamin** kualitas tidur yang baik jika interupsi masih tinggi.
        - Hutang tidur cenderung meningkat pada pengguna yang sering mengalami gangguan saat tidur.
        """)
    else:
        st.warning(":warning: Tidak ada data untuk ditampilkan.")

    # 6. Bagian Visualisasi Grafik
    if len(df_filtered) > 0:
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.subheader("📊 Dampak Jumlah Interupsi Terhadap Kualitas Tidur")
            df_int_quality = df_filtered.groupby('interruptions')['quality_score'].mean().reset_index()
            df_int_quality = df_int_quality.sort_values(by='interruptions')
            df_int_quality['interruptions'] = df_int_quality['interruptions'].astype(str)
            df_int_quality = df_int_quality.set_index('interruptions')
            st.bar_chart(df_int_quality, y="quality_score", color="#E67E22")

        with row1_col2:
            st.subheader("📊 Distribusi Skor Kualitas Tidur")
            df_score_dist = df_filtered['quality_score'].value_counts().reset_index()
            df_score_dist.columns = ['Skor Kualitas', 'Jumlah Log']
            df_score_dist = df_score_dist.sort_values(by='Skor Kualitas')
            df_score_dist = df_score_dist.set_index('Skor Kualitas')
            st.bar_chart(df_score_dist, y="Jumlah Log", color="#FF6B6B")

        st.markdown("---")
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            st.subheader("📉 Korelasi Durasi Tidur vs Skor Kualitas")
            st.scatter_chart(df_filtered, x="duration_hours", y="quality_score", color="interruptions")

        with row2_col2:
            st.subheader("🔄 Rata-rata Hutang Tidur Berdasarkan Jumlah Interupsi")
            df_int = df_filtered.groupby('interruptions')['sleep_debt_hours'].mean().reset_index()
            df_int = df_int.sort_values(by='interruptions')
            df_int = df_int.set_index('interruptions')
            st.bar_chart(df_int, y="sleep_debt_hours", color="#6C5CE7")
    else:
        st.warning("⚠️ Data kosong pada filter yang Anda pilih.")

    st.caption("Vitara Capstone Project • Health Scoring Dashboard")
