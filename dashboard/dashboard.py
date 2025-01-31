import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("main_data2.csv")

df = load_data()

# Sidebar Layout
st.sidebar.header("Dashboard Navigation")
selected_category = st.sidebar.selectbox("Pilih Kategori Data", df["Description"].unique())

# Fitur tambahan: Filter berdasarkan rentang tanggal
st.sidebar.subheader("Filter Data")
start_date = st.sidebar.date_input("Tanggal Awal", pd.to_datetime(df.index.min()))
end_date = st.sidebar.date_input("Tanggal Akhir", pd.to_datetime(df.index.max()))

# Filter berdasarkan kategori
filtered_data = df[(df["Description"] == selected_category)]

# Dashboard Title
st.title("📊 Bike Rental Dashboard")
st.write("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan berbagai faktor.")

# Fitur tambahan: Pencarian kategori
selected_subcategories = st.multiselect("Pilih Subkategori (opsional)", filtered_data["Category"].unique(), default=filtered_data["Category"].unique())
filtered_data = filtered_data[filtered_data["Category"].isin(selected_subcategories)]

# Menampilkan data
st.subheader("📋 Data Terkait")
st.dataframe(filtered_data)

# Generate dynamic description based on selected subcategories
if not filtered_data.empty:
    st.subheader("ℹ️ Informasi Detail")
    description_texts = []

    # Loop through the selected subcategories and create description text
    for category in selected_subcategories:
        category_data = filtered_data[filtered_data["Category"] == category]
        avg_value = category_data["Value"].mean()
        description_texts.append(f"Penyewaan sepeda pada kategori **{category}** rata-rata: **{avg_value:.2f}**.")

    # Display all description texts
    for desc in description_texts:
        st.write(desc)

else:
    st.write("Tidak ada data yang sesuai dengan filter yang dipilih.")

# Visualisasi Data dengan keterangan
st.subheader("📈 Visualisasi Data")
base_color = "#4c72b0"
highlight_color = "#1f3c70"  # Warna lebih tua untuk nilai tertinggi

if "Average Rentals by Season" in selected_category:
    st.write("Grafik ini menunjukkan rata-rata penyewaan sepeda berdasarkan musim.")
    filtered_data = filtered_data.sort_values("Value", ascending=True)
    plt.figure(figsize=(8,5))
    bars = plt.bar(filtered_data["Category"], filtered_data["Value"], color=base_color)
    bars[-1].set_color(highlight_color)  # Menyoroti nilai tertinggi
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata Penyewaan")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(plt)

elif "Average Rentals by Hour" in selected_category:
    st.write("Grafik ini menampilkan rata-rata penyewaan sepeda berdasarkan jam dalam sehari.")
    filtered_data = filtered_data.sort_values("Category")
    peak_hour = filtered_data.loc[filtered_data['Value'].idxmax()]
    st.write(f"Jam dengan penyewaan tertinggi adalah jam {int(peak_hour['Category'])}:00 dengan rata-rata {peak_hour['Value']:.0f} sepeda disewa.")
    plt.figure(figsize=(10,5))
    plt.plot(filtered_data["Category"], filtered_data["Value"], color=base_color, marker='o')
    plt.scatter(peak_hour["Category"], peak_hour["Value"], color=highlight_color, s=100, label='Puncak')
    plt.xlabel("Jam")
    plt.ylabel("Rata-rata Penyewaan")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    plt.legend()
    st.pyplot(plt)

elif "Correlation Between Variables" in selected_category:
    st.write("Heatmap ini menunjukkan korelasi antara variabel cuaca dan jumlah penyewaan sepeda.")
    heatmap_data = filtered_data.pivot(index="Category", columns="Subcategory", values="Value")
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    st.write("Semakin tinggi nilai korelasi (mendekati 1 atau -1), semakin kuat hubungan antara variabel tersebut.")

elif "Average Rentals by Day Type" in selected_category:
    st.write("Grafik ini menunjukkan perbedaan rata-rata penyewaan sepeda pada hari kerja dan akhir pekan.")
    filtered_data = filtered_data.sort_values("Value", ascending=True)
    plt.figure(figsize=(8,5))
    bars = plt.bar(filtered_data["Category"], filtered_data["Value"], color=base_color)
    bars[-1].set_color(highlight_color)
    plt.xlabel("Tipe Hari")
    plt.ylabel("Rata-rata Penyewaan")
    plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Hari Kerja vs Akhir Pekan")
    st.pyplot(plt)

elif "Average Usage (Daily and Hourly)" in selected_category:
    st.write("Grafik ini membandingkan penggunaan sepeda antara pengguna terdaftar (registered) dan pengguna casual, baik dalam skala harian maupun per jam.")
    filtered_data = filtered_data.sort_values("Value", ascending=True)
    plt.figure(figsize=(10,5))
    sns.barplot(data=filtered_data, x="Category", y="Value", hue="Subcategory", palette=[base_color, highlight_color])
    plt.ylabel("Rata-rata Penyewaan")
    plt.title("Perbandingan Penggunaan Sepeda: Casual vs Registered")
    st.pyplot(plt)

# Widgets (Checkbox & Button)
if st.checkbox("Tampilkan 5 Baris Data Pertama"):
    st.write(df.head())

if st.button("Refresh Data"):
    st.experimental_rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.text("@Daffa Kurnia Nurfirdaus")