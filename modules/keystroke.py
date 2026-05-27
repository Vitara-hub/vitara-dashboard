import streamlit as st
import pandas as pd
import plotly.express as px

def show_keystroke_dashboard():

    # LOAD DATA
    df = pd.read_csv('https://drive.google.com/uc?id=1BMdcEBx4x2-KE4HhOjdvAjIQny3BXDVP')

    # SIDEBAR FILTER
    st.sidebar.subheader("⌨️ Keystroke Filter")

    stress_range = st.sidebar.slider(
        "Stress Range",
        0.0,
        1.0,
        (0.0, 1.0)
    )

    df = df[
        (df['stress_label'] >= stress_range[0]) &
        (df['stress_label'] <= stress_range[1])
    ]

    # HEADER DATA
    total_users = df['user_id'].nunique()
    total_sessions = len(df)

    avg_wpm = round(df['wpm'].mean(), 1)
    avg_stress = round(df['stress_label'].mean(), 2)
    avg_backspace = round(df['backspace_rate'].mean(), 2)
    avg_variance = round(df['typing_variance'].mean(), 2)

    # TITLE
    col1, col2 = st.columns([5,1])

    with col1:
        st.title("⌨️ Keystroke Dynamics Dashboard")
        st.caption("Typing Behavior & Stress Pattern Analysis")

    with col2:
        st.image("Assets/keyboard.png", width=180)

    # METRICS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👤 Total Users", total_users)

    with col2:
        st.metric("📄 Total Sessions", f"{total_sessions:,}")

    with col3:
        st.metric("⚡ Average WPM", avg_wpm)

    with col4:
        st.metric("🔥 Average Stress", avg_stress)

    st.divider()

    # DYNAMIC INSIGHT
    with st.container(border=True):

        st.markdown(f"""
        ### 📌 Insight & Analysis

        - Dataset terdiri dari **{total_users} user**
        - Total typing session sebanyak **{total_sessions:,}**
        - Rata-rata typing speed user berada di angka **{avg_wpm} WPM**
        - Rata-rata stress score berada di angka **{avg_stress}**
        - Average backspace rate sebesar **{avg_backspace}**
        - Typing variance rata-rata berada di angka **{avg_variance}**
        """)

        # Typing speed analysis
        if avg_wpm >= 60:
            st.success("""
            ⚡ User menunjukkan performa mengetik cepat
            dengan tingkat efisiensi typing yang tinggi.
            """)

        elif avg_wpm >= 40:
            st.info("""
            ⌨️ User menunjukkan typing performance
            pada tingkat menengah dengan pola stabil.
            """)

        else:
            st.warning("""
            🐢 Dataset menunjukkan typing speed
            yang relatif lambat.
            """)

        # Stress analysis
        if avg_stress >= 0.7:
            st.error("""
            🔥 Typing pattern menunjukkan indikasi
            tingkat stress yang tinggi.
            """)

        elif avg_stress >= 0.4:
            st.warning("""
            ⚠️ Tingkat stress berada pada kategori
            menengah dengan variasi typing behavior.
            """)

        else:
            st.success("""
            ✅ Mayoritas session menunjukkan
            tingkat stress rendah dan typing stabil.
            """)

    st.divider()

     
    # WPM DISTRIBUTION
    fig_wpm = px.histogram(
        df,
        x='wpm',
        nbins=20,
        title='Typing Speed Distribution',
        color_discrete_sequence=['#00F5FF']
    )

    fig_wpm.update_layout(
        template='plotly_dark',
        height=400
    )

     
    # STRESS DISTRIBUTION
    fig_stress = px.histogram(
        df,
        x='stress_label',
        nbins=20,
        title='Stress Distribution',
        color_discrete_sequence=['#FF4ECD']
    )

    fig_stress.update_layout(
        template='plotly_dark',
        height=400
    )

     
    # ROW 1
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_wpm, use_container_width=True)

    with col2:
        st.plotly_chart(fig_stress, use_container_width=True)

     
    # USER WPM
    user_wpm = (
        df.groupby('user_id')['wpm']
        .mean()
        .reset_index()
    )

    fig_user = px.line(
        user_wpm,
        x='user_id',
        y='wpm',
        markers=True,
        title='Average WPM per User'
    )

    fig_user.update_layout(
        template='plotly_dark',
        height=400
    )

     
    # WPM VS STRESS
    fig_scatter = px.scatter(
        df,
        x='wpm',
        y='stress_label',
        color='typing_variance',
        size='backspace_rate',
        hover_data=['user_id'],
        title='Typing Speed vs Stress',
        color_continuous_scale='Turbo'
    )

    fig_scatter.update_layout(
        template='plotly_dark',
        height=400
    )

     
    # ROW 2
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_user, use_container_width=True)

    with col2:
        st.plotly_chart(fig_scatter, use_container_width=True)

     
    # TYPING VARIANCE
    fig_variance = px.histogram(
        df,
        x='typing_variance',
        nbins=20,
        title='Typing Variance Distribution',
        color_discrete_sequence=['#8B5CF6']
    )

    fig_variance.update_layout(
        template='plotly_dark',
        height=400
    )

    st.plotly_chart(
        fig_variance,
        use_container_width=True
    )

     
    # CONCLUSION
    with st.container(border=True):

        st.markdown("""
        ### ✅ Conclusion

        Dataset keystroke dynamics menunjukkan pola
        hubungan antara typing behavior dan tingkat stress.

        Data telah melalui preprocessing dan siap
        digunakan untuk predictive analytics,
        stress monitoring, maupun machine learning.
        """)

     
    # USER SUMMARY
    st.subheader("👤 User Typing Summary")

    user_summary = (
        df.groupby('user_id')
        .agg({
            'wpm': 'mean',
            'stress_label': 'mean',
            'backspace_rate': 'mean',
            'typing_variance': 'mean'
        })
        .reset_index()
    )

    st.dataframe(
        user_summary,
        use_container_width=True
    )

    # FOOTER
    st.divider()

    st.caption("Vitara Capstone Project • Keystroke Dynamics Dashboard")