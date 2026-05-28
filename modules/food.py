import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import zipfile
import os
import random


def show_food_dashboard():

    # CONFIG
    sample_url = ("https://drive.google.com/uc?export=download&id=1Xdk2g825z7DpfK8d69q_l7xWA5GCzdkb")
    

    sample_zip_path = (
        "Dataset/FoodVision/"
        "foodvision_sample.zip"
    )

    sample_extract_path = (
        "Dataset/FoodVision/"
        "sample_images"
    )

    os.makedirs(
        "Dataset/FoodVision",
        exist_ok=True
    )

     
    # LOAD DATA
    @st.cache_data
    def load_data():

        # langsung read metadata
        df = pd.read_csv('https://drive.google.com/uc?id=1L-0URz8IZ6eAW6WVvJqJHuJFUbTi3iOH')

        # download sample zip sekali
        if not os.path.exists(
            sample_zip_path
        ):

            gdown.download(sample_url, sample_zip_path, quiet=True)

        # extract sekali
        if not os.path.exists(sample_extract_path):
            with zipfile.ZipFile(sample_zip_path, "r") as zip_ref:
                zip_ref.extractall( sample_extract_path)

        return df

    df = load_data()
     
    # SIDEBAR FILTER
    st.sidebar.subheader("🍔 Food Vision Filter")

    selected_classes = (
        st.sidebar.multiselect(
            "Food Class",
            sorted(df['food_class'].unique()),
            default=sorted(df['food_class'].unique())
        )
    )

    df = df[df['food_class'].isin(selected_classes)]

    # KPI
    total_images = len(df)

    total_classes = (df['food_class'].nunique())

    avg_images = (total_images / total_classes if total_classes > 0 else 0)

    dominant_class = (df['food_class'].mode()[0])

     
    # HEADER
    st.title("🍔 Food Vision Dashboard")

    st.caption("Food Image Dataset Analysis")
     
    # METRICS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📷 Total Images", f"{total_images:,}")

    c2.metric("🍱 Total Classes", total_classes)

    c3.metric("📊 Avg Images/Class", round(avg_images, 1))

    c4.metric("⭐ Dominant Class", dominant_class)

    st.divider()
     
    # DISTRIBUTION
    st.subheader("📊 Food Class Distribution")

    class_dist = (df['food_class'].value_counts().reset_index())

    class_dist.columns = ['Food Class', 'Count']

    fig = px.bar(
        class_dist,
        x='Food Class',
        y='Count',
        color='Count',
        color_continuous_scale='Turbo'
    )

    fig.update_layout(
        template='plotly_dark',
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

     
    # SAMPLE IMAGES
    st.subheader("🍕 Sample Food Images")

    available_classes = [
        c for c in selected_classes
        if os.path.exists(
            os.path.join(
                sample_extract_path,
                c
            )
        )
    ]

    cols = st.columns(3)

    random_classes = random.sample(
        available_classes,
        min(6, len(available_classes))
    )

    for i, food_class in enumerate(
        random_classes
    ):

        folder = os.path.join(
            sample_extract_path,
            food_class
        )

        images = [
            img for img in
            os.listdir(folder)
            if img.endswith(
                (
                    ".jpg",
                    ".png",
                    ".jpeg"
                )
            )
        ]

        image_path = os.path.join(
            folder,
            random.choice(images)
        )

        with cols[i % 3]:

            st.image(
                image_path,
                use_container_width=True
            )

            st.caption(
                f"🍽 {food_class}"
            )

    st.divider()

    st.caption("Vitara Capstone Project • Food Vision Dashboard")