import streamlit as st
from youtube_api import get_channel_videos
from data_utils import plot_views_over_time, plot_top_videos_by_views, basic_stats
from analytics_api import get_analytics_data
from config import YOUTUBE_API_KEY
import pandas as pd
from data_utils import plot_engagement_trends
from data_utils import get_low_performing_videos, plot_title_length_vs_views

st.set_page_config(page_title="YouTube Kanal Analizi", layout="wide")

st.title("📊 YouTube Kanal Analiz Uygulaması")

# Kullanıcı tipi seçimi
api_type = st.selectbox("API Türünü Seçin", ["Genel (herkese açık)", "Kanal Sahibi (Analytics API)"])
channel_id = st.text_input("YouTube Kanal ID'si Girin")

if api_type == "Kanal Sahibi (Analytics API)":
    access_token = st.text_input("YouTube Analytics API Access Token", type="password")

# Bilgilendirici açıklama
with st.expander("ℹ️ Kanal Sahibi API Erişimi Nasıl Alınır?"):
    st.markdown("""
    **YouTube Analytics API Kullanmak için:**
    1. [Google Developers Console](https://console.developers.google.com/) üzerinden proje oluşturun.
    2. `YouTube Analytics API` etkinleştirin.
    3. OAuth 2.0 ile Playground üzerinden yetkilendirme yapın.
    4. `https://www.googleapis.com/auth/yt-analytics.readonly` iznini seçin.
    5. Erişim token’ınızı buraya yapıştırın.
    """)

if st.button("Verileri Getir"):
    if not channel_id:
        st.warning("Lütfen bir YouTube Kanal ID'si girin.")
    else:
        with st.spinner("Veriler yükleniyor..."):
            try:
                if api_type == "Genel (herkese açık)":
                    df = get_channel_videos(channel_id, api_key=YOUTUBE_API_KEY, max_videos=1000)
                    if df.empty:
                        st.warning("Video bulunamadı veya geçersiz kanal ID.")
                    else:
                        st.success("Genel kanal verileri yüklendi.")
                        stats = basic_stats(df)
                        st.subheader("📌 Temel İstatistikler")
                        st.write(stats)

                        st.subheader("📈 Zamana Göre İzlenme Grafiği")
                        fig1 = plot_views_over_time(df)
                        st.pyplot(fig1)

                        st.subheader("🏆 En Çok İzlenen Videolar")
                        fig2 = plot_top_videos_by_views(df)
                        st.pyplot(fig2)

                else:
                    if not access_token:
                        st.error("Lütfen access token girin.")
                    else:
                        df = get_analytics_data(channel_id, access_token)
                        st.success("Kanal sahibine özel Analytics verileri yüklendi.")

                        st.subheader("📊 Günlük İzlenme Zaman Serisi")
                        st.line_chart(df.set_index("date")[["views"]]) #line_chart çizgi grafiği oluşturur

                        st.subheader("⏱ Ortalama İzlenme Süresi (Dakika)")
                        st.write(f"Ortalama: {int(df['watch_minutes'].mean())} dakika")

                        st.subheader("🗓 Tahmini Aylık İzlenme")
                        monthly_views = df.resample("M", on="date")["views"].sum()  #resample zaman serisini aylık olarak gruplar   
                        st.bar_chart(monthly_views)
                    with st.expander("🎯 Beğeni/Yorum Oranı Trendleri"):
                        fig = plot_engagement_trends(df)
                        st.pyplot(fig)

                    with st.expander("⚠️ Düşük Performanslı Videolar"):    #expander, İçindeki içeriği varsayılan olarak gizler.Kullanıcı üzerine tıklayınca içindeki bileşenler görünür.

                        low_df = get_low_performing_videos(df)
                        st.dataframe(low_df[['title', 'viewCount', 'publishedAt']]) #publishedAt, videonun YouTube’a yüklendiği tarihi temsil eder.

                    with st.expander("🧠 Başlık Uzunluğu ve İzlenme Analizi"):
                        fig = plot_title_length_vs_views(df)
                        st.pyplot(fig)


            except Exception as e:
                st.error(f"Hata oluştu: {e}")

