import feedparser
import json
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    {
        "name": "AWS 公式ブログ",
        "url": "https://aws.amazon.com/jp/blogs/news/feed/",
        "tag": "AWS",
        "color": "#FF9900",
    },
    {
        "name": "Zenn - AWS",
        "url": "https://zenn.dev/topics/aws/feed",
        "tag": "Zenn",
        "color": "#3EA8FF",
    },
    {
        "name": "Zenn - Kubernetes",
        "url": "https://zenn.dev/topics/kubernetes/feed",
        "tag": "Zenn",
        "color": "#3EA8FF",
    },
    {
        "name": "Zenn - インフラ",
        "url": "https://zenn.dev/topics/infrastructure/feed",
        "tag": "Zenn",
        "color": "#3EA8FF",
    },
    {
        "name": "Google Cloud Blog",
        "url": "https://cloud.google.com/feeds/gcp-release-notes.xml",
        "tag": "GCP",
        "color": "#4285F4",
    },
    {
        "name": "Azure Updates",
        "url": "https://azurecomcdn.azureedge.net/en-us/updates/feed/",
        "tag": "Azure",
        "color": "#0078D4",
    },
    {
        "name": "Hacker News - Ask HN / Show HN",
        "url": "https://hnrss.org/newest?q=kubernetes+OR+terraform+OR+aws+OR+llm&points=50",
        "tag": "HN",
        "color": "#FF6600",
    },
    {
        "name": "The New Stack",
        "url": "https://thenewstack.io/feed/",
        "tag": "インフラ",
        "color": "#009688",
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
        "tag": "AI",
        "color": "#10A37F",
    },
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/rss.xml",
        "tag": "AI",
        "color": "#B07E53",
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.research.google/feeds/posts/default",
        "tag": "AI",
        "color": "#EA4335",
    },
]

MAX_ITEMS_PER_FEED = 10


def parse_date(entry):
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    for attr in ("published", "updated"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return parsedate_to_datetime(val).astimezone(timezone.utc)
            except Exception:
                pass
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def fetch_feed(feed_def):
    items = []
    try:
        parsed = feedparser.parse(feed_def["url"])
        for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
            title = entry.get("title", "（タイトルなし）").strip()
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            if summary:
                # strip basic HTML tags
                import re
                summary = re.sub(r"<[^>]+>", "", summary)[:200].strip()
            pub = parse_date(entry)
            items.append(
                {
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": pub.isoformat(),
                    "source": feed_def["name"],
                    "tag": feed_def["tag"],
                    "color": feed_def["color"],
                }
            )
    except Exception as e:
        print(f"[ERROR] {feed_def['name']}: {e}")
    return items


def main():
    all_items = []
    for feed_def in FEEDS:
        print(f"Fetching: {feed_def['name']}")
        all_items.extend(fetch_feed(feed_def))

    # Sort by published date descending
    all_items.sort(key=lambda x: x["published"], reverse=True)

    os.makedirs("docs", exist_ok=True)
    out_path = os.path.join("docs", "news.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {"updated": datetime.now(timezone.utc).isoformat(), "items": all_items},
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"Wrote {len(all_items)} items to {out_path}")


if __name__ == "__main__":
    main()
