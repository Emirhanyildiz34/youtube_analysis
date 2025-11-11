import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="darkgrid")



def plot_engagement_trends(df):
    df = df.copy()
    df['like_rate'] = df['likeCount'] / df['viewCount']
    df['comment_rate'] = df['commentCount'] / df['viewCount']
    df = df.sort_values('publishedAt')

    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df['publishedAt'], df['like_rate'], label='Beğeni Oranı', marker='o')
    ax.plot(df['publishedAt'], df['comment_rate'], label='Yorum Oranı', marker='x')
    ax.set_title('Zamana Göre Beğeni/Yorum Oranı')
    ax.set_ylabel('Oran')
    ax.set_xlabel('Yayın Tarihi')
    ax.legend()
    plt.tight_layout()
    return fig

def get_low_performing_videos(df):
    avg_views = df['viewCount'].mean()
    low_videos = df[df['viewCount'] < avg_views]
    return low_videos.sort_values('viewCount')

def plot_title_length_vs_views(df):
    df = df.copy()
    df['title_length'] = df['title'].apply(len)
    df['word_count'] = df['title'].apply(lambda x: len(x.split()))

    fig, ax = plt.subplots(figsize=(10,6))
    sns.scatterplot(data=df, x='title_length', y='viewCount', ax=ax, color='royalblue')
    ax.set_title('Başlık Uzunluğu vs. İzlenme Sayısı')
    ax.set_xlabel('Başlık Uzunluğu (karakter)')
    ax.set_ylabel('İzlenme Sayısı')
    plt.tight_layout()
    return fig

def plot_views_over_time(df):
    df_sorted = df.sort_values('publishedAt')
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(df_sorted['publishedAt'], df_sorted['viewCount'], marker='o')
    ax.set_title('Videoların Yayınlanma Tarihine Göre İzlenme Sayıları')
    ax.set_xlabel('Yayınlanma Tarihi')
    ax.set_ylabel('İzlenme Sayısı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_top_videos_by_views(df, top_n=10):
    top_videos = df.sort_values('viewCount', ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x='viewCount', y='title', data=top_videos, palette='viridis', ax=ax)
    ax.set_title(f'En Çok İzlenen İlk {top_n} Video')
    ax.set_xlabel('İzlenme Sayısı')
    ax.set_ylabel('Video Başlığı')
    plt.tight_layout()
    return fig

def basic_stats(df):
    stats = {
        'Toplam Video': len(df),
        'Toplam İzlenme': df['viewCount'].sum(),
        'Ortalama İzlenme': int(df['viewCount'].mean()),
        'Toplam Yorum': df['commentCount'].sum(),
        'Toplam Beğeni': df['likeCount'].sum(),
    }
    return stats
