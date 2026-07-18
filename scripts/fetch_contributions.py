#!/usr/bin/env python3
"""Fetch contribution data from GitHub's public HTML (no token needed)."""
import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def fetch_contributions(username: str, output_path: str = "data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")

    contributions = []
    for day in days:
        date_str = day.get("data-date", "")
        level = day.get("data-level", "0")
        if not date_str:
            continue
        contributions.append({
            "date": date_str,
            "count": int(level),
            "level": int(level),
        })

    if not contributions:
        print("No contribution data found. Check username.")
        sys.exit(1)

    # Calculate stats
    counts = [c["count"] for c in contributions]
    total = sum(counts)
    max_day = max(counts) if counts else 0
    avg = total / len(counts) if counts else 0

    # Current streak
    streak = 0
    for c in reversed(contributions):
        if c["count"] > 0:
            streak += 1
        else:
            break

    # Longest streak
    longest = 0
    current = 0
    for c in contributions:
        if c["count"] > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    # Monthly totals
    monthly = {}
    for c in contributions:
        month = c["date"][:7]
        monthly[month] = monthly.get(month, 0) + c["count"]

    data = {
        "username": username,
        "total": total,
        "max_day": max_day,
        "average": round(avg, 1),
        "current_streak": streak,
        "longest_streak": longest,
        "monthly": monthly,
        "days": contributions,
        "fetched_at": datetime.utcnow().isoformat(),
    }

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(contributions)} days, {total} contributions for @{username}")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "vaib2607"
    fetch_contributions(username)
