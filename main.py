import os
import json
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURATION ---
BATTLE_TAG = os.getenv('BATTLE_TAG')
HISTORY_FILE = 'history.json'
BADGE_FILE = 'badge.json'
CHART_FILE = 'rank_history.png'

def rank_to_numeric(rank_string):
    """Converts 'Gold 3' to a number like 1700 for graphing."""
    if not rank_string or "Unranked" in rank_string:
        return 0
    tier_map = {
        "Bronze": 500, "Silver": 1000, "Gold": 1500, "Platinum": 2000, 
        "Diamond": 2500, "Master": 3000, "Grandmaster": 3500, "Champion": 4000
    }
    try:
        parts = rank_string.split()
        tier = parts[0]
        division = int(parts[1])
        return tier_map.get(tier, 0) + ((5 - division) * 100)
    except (IndexError, ValueError):
        return 0

def get_tier_styles(rank_string):
    """Returns a color and label based on the rank tier."""
    tier_colors = {
        "Champion": "#db00ff", "Grandmaster": "#ff0000", "Master": "#ffa500",
        "Diamond": "#b9f2ff", "Platinum": "#95e1d3", "Gold": "#ffd700",
        "Silver": "#c0c0c0", "Bronze": "#cd7f32"
    }
    for tier, color in tier_colors.items():
        if tier in rank_string:
            return color, f"Rank: {tier}"
    return "#333333", "Rank: Unranked"

def get_trend_indicator(history, current_num):
    """Compares current rank to the last entry in history."""
    if not history:
        return ""
    last_num = rank_to_numeric(history[-1]['rank'])
    if current_num > last_num: return " 📈"
    if current_num < last_num: return " 📉"
    return " ="

def run_tracker():
    if not BATTLE_TAG:
        print("Error: BATTLE_TAG secret is missing.")
        return

    # 1. Fetch Data
    tag_id = BATTLE_TAG.replace('#', '-')
    url = f"https://overfast-api.tekrop.fr/players/{tag_id}/summary"
    
    print(f"Fetching data for {tag_id}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return

    data = response.json()
    
    # 2. Extract Competitive Data Safely
    # Note: OverFast API structure may vary; we use .get() to prevent 'undefined'
    comp_data = data.get('competitive', {})
    current_rank = comp_data.get('rank', 'Unranked')
    
    # 3. Load History for Trend Analysis
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)

    # 4. Calculate Visuals
    current_num = rank_to_numeric(current_rank)
    trend = get_trend_indicator(history, current_num)
    badge_color, badge_label = get_tier_styles(current_rank)

    # 5. Update Badge JSON
    with open(BADGE_FILE, 'w') as f:
        json.dump({
            "schemaVersion": 1,
            "label": badge_label,
            "message": f"{current_rank}{trend}",
            "color": badge_color,
            "style": "for-the-badge"
        }, f, indent=4)

    # 6. Update History File
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rank": current_rank
    })
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

    # 7. Generate Chart
    dates = [entry['date'] for entry in history]
    nums = [rank_to_numeric(entry['rank']) for entry in history]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, nums, color='#f99e1a', marker='o', linewidth=2)
    plt.title(f"Overwatch Rank Progression: {BATTLE_TAG}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(CHART_FILE)
    print(f"Successfully updated! Current Rank: {current_rank}")

if __name__ == "__main__":
    run_tracker()
