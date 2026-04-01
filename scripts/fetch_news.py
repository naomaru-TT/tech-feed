import feedparser
import json
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEEDS = [
    # ── AWS ──────────────────────────────────────────────
    {
        "name": "AWS 公式ブログ（日本語）",
        "url": "https://aws.amazon.com/jp/blogs/news/feed/",
        "tag": "AWS",
        "color": "#FF9900",
    },
    {
        "name": "AWS What's New（日本語）",
        "url": "https://aws.amazon.com/jp/about-aws/whats-new/recent/feed/",
        "tag": "AWS",
        "color": "#FF9900",
    },
    {
        "name": "Zenn - AWS",
        "url": "https://zenn.dev/topics/aws/feed",
        "tag": "AWS",
        "color": "#FF9900",
    },
    {
        "name": "Qiita - AWS",
        "url": "https://qiita.com/tags/aws/feed",
        "tag": "AWS",
        "color": "#FF9900",
    },
    # ── AI ───────────────────────────────────────────────
    {
        "name": "Zenn - 機械学習",
        "url": "https://zenn.dev/topics/machinelearning/feed",
        "tag": "AI",
        "color": "#10A37F",
    },
    {
        "name": "Zenn - LLM",
        "url": "https://zenn.dev/topics/llm/feed",
        "tag": "AI",
        "color": "#10A37F",
    },
    {
        "name": "Qiita - 機械学習",
        "url": "https://qiita.com/tags/%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92/feed",
        "tag": "AI",
        "color": "#10A37F",
    },
    {
        "name": "Qiita - ChatGPT",
        "url": "https://qiita.com/tags/chatgpt/feed",
        "tag": "AI",
        "color": "#10A37F",
    },
    {
        "name": "ITmedia AI+",
        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
        "tag": "AI",
        "color": "#10A37F",
    },
    # ── インフラ ─────────────────────────────────────────
    {
        "name": "Zenn - Kubernetes",
        "url": "https://zenn.dev/topics/kubernetes/feed",
        "tag": "インフラ",
        "color": "#326CE5",
    },
    {
        "name": "Zenn - Terraform",
        "url": "https://zenn.dev/topics/terraform/feed",
        "tag": "インフラ",
        "color": "#326CE5",
    },
    {
        "name": "Zenn - Docker",
        "url": "https://zenn.dev/topics/docker/feed",
        "tag": "インフラ",
        "color": "#326CE5",
    },
    {
        "name": "Qiita - インフラ",
        "url": "https://qiita.com/tags/%E3%82%A4%E3%83%B3%E3%83%95%E3%83%A9/feed",
        "tag": "インフラ",
        "color": "#326CE5",
    },
    {
        "name": "Qiita - Kubernetes",
        "url": "https://qiita.com/tags/kubernetes/feed",
        "tag": "インフラ",
        "color": "#326CE5",
    },
    # ── GCP ──────────────────────────────────────────────
    {
        "name": "Google Cloud リリースノート",
        "url": "https://cloud.google.com/feeds/gcp-release-notes.xml",
        "tag": "GCP",
        "color": "#4285F4",
    },
    {
        "name": "Zenn - GCP",
        "url": "https://zenn.dev/topics/gcp/feed",
        "tag": "GCP",
        "color": "#4285F4",
    },
    # ── テック全般 ────────────────────────────────────────
    {
        "name": "ITmedia エンタープライズ",
        "url": "https://rss.itmedia.co.jp/rss/2.0/itmediaenterprise.xml",
        "tag": "テック",
        "color": "#888780",
    },
    {
        "name": "Publickey",
        "url": "https://www.publickey1.jp/atom.xml",
        "tag": "テック",
        "color": "#888780",
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
