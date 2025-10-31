import datetime
import os

import feedgen.feed as ffeed
import requests


def add_entry(fg: ffeed.FeedGenerator, event: dict):
    """
    connpass API から取得したイベント情報を RSS エントリーとして追加する
    """
    fe = fg.add_entry()
    fe.id(event["url"])
    fe.title(event["title"])
    fe.link(href=event["url"])
    description = ""
    # 開催地情報を追加
    if event.get("place"):
        description += f"📍 会場: {event['place']}"
        if event.get("address"):
            description += f"\n住所: {event['address']}"

    # 説明文を作成（catch と description の組み合わせ）
    description += f"\n\n{event.get('catch', '')}"
    description += f"\n\n{event.get('description', '')}"
    fe.description(description)

    # 開始日時を published として設定
    if "started_at" in event:
        fe.published(event["started_at"])

    # 画像を設定（enclosure として追加）
    if event.get("image_url"):
        # feedgen では enclosure を使って画像を追加
        # RSS では enclosure は通常メディアファイル用
        # 代わりに content として設定することも可能
        fe.enclosure(event["image_url"], 0, "image/png")

    return fg


def fetch_content(keyword: list, prefecture: str) -> dict:
    """
    connpass API からイベント情報を取得する
    """
    URL = "https://connpass.com/api/v2/events/"
    API_KEY = os.getenv("CONNPASS_API_KEY", "")
    headers = {"X-API-Key": API_KEY, "User-Agent": "connpass-rss/1.0"}
    params = {"keyword": keyword, "prefecture": prefecture}

    try:
        print(f"Fetching content from {URL} with params {params}")
        response = requests.get(URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": "Failed to fetch content", "events": []}


def main():
    PREFECTURE_EN = "aichi"
    PREFECTURE_JA = "愛知"
    content = fetch_content(prefecture=PREFECTURE_EN, keyword=[])
    print(f"取得したイベント数: {len(content.get('events', []))}")

    fg = ffeed.FeedGenerator()
    fg.id("https://connpass.com/explore/")
    fg.title(PREFECTURE_JA + "のイベント")
    fg.author({"name": "connpass-rss", "email": "example@example.com"})
    fg.link(href="https://connpass.com/explore/", rel="alternate")
    fg.subtitle(PREFECTURE_JA + "のイベント情報")
    fg.link(href="https://connpass.com/explore/", rel="self")
    fg.language("ja")

    # 取得したイベントのうちこれから開催されるものをRSSエントリーとして追加
    for event in content.get("events", []):
        if event.get("started_at") > datetime.datetime.now().isoformat():
            print(f"Adding event to RSS feed: {event['title']}")
            fg = add_entry(fg, event)

    fg.rss_file("rss.xml")  # Write the RSS feed to a file
    print(f"RSS feed generated: rss.xml ({len(content.get('events', []))} events)")


if __name__ == "__main__":
    main()
