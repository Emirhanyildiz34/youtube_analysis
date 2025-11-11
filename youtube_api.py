from config import YOUTUBE_API_KEY
from googleapiclient.discovery import build
import pandas as pd
import isodate  # video süresini çözmek için


def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
    
def parse_duration(duration_str):
    try:
        duration = isodate.parse_duration(duration_str)
        return duration.total_seconds()
    except:
        return None

def get_channel_videos(channel_id, api_key= YOUTUBE_API_KEY, max_videos=100):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    videos = []
    next_page_token = None

    while len(videos) < max_videos:
        remaining = max_videos - len(videos)      #remaining kalan video sayısını hesaplar
        max_results = 50 if remaining > 50 else remaining

        request = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=max_results,
            order='date',
            type='video',
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'publishedAt': item['snippet']['publishedAt']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    df = pd.DataFrame(videos)

    if df.empty:
        return df
    
    # Videoların istatistiklerini alalım
    video_ids = df['video_id'].tolist()
    details = []
    for i in range(0, len(video_ids), 50):
        chunk_ids = video_ids[i:i+50]
        stats_request = youtube.videos().list(
            part='statistics',
            id=','.join(chunk_ids)
        )
        stats_response = stats_request.execute()

        for item in stats_response.get('items', []):
            details.append({
                'video_id': item['id'],
                'viewCount': safe_int(item['statistics'].get('viewCount')),
                'likeCount': safe_int(item['statistics'].get('likeCount')),
                'commentCount': safe_int(item['statistics'].get('commentCount'))
            })

    details_df = pd.DataFrame(details)
    result = pd.merge(df, details_df, on='video_id')
    result['publishedAt'] = pd.to_datetime(result['publishedAt'])
    return result

