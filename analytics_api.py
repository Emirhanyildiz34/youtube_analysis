import requests
import pandas as pd

def get_analytics_data(channel_id, access_token):
    url = "https://youtubeanalytics.googleapis.com/v2/reports"
    params = {
        "ids": "channel==MINE",
        "metrics": "views,likes,comments,estimatedMinutesWatched",
        "dimensions": "day",
        "startDate": "2024-01-01",
        "endDate": "2024-12-31",
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if "rows" not in data:
        raise Exception("API'den geçerli veri alınamadı. Access token geçersiz olabilir.")  #raise Programın istenmeyen veya beklenmeyen bir durumda durmasını sağlar.

    df = pd.DataFrame(data["rows"], columns=["date", "views", "likes", "comments", "watch_minutes"])
    df["date"] = pd.to_datetime(df["date"])
    return df
