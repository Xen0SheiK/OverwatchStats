import os
import json
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Configuration & Secrets
BATTLE_TAG = os.getenv('BATTLE_TAG')
HISTORY_FILE = 'history.json'
BADGE_FILE = 'badge.json'
CHART_FILE = 'rank_history.png'

def rank_to_numeric(rank_string):
    if not rank_string or "Unranked" in rank_string: return 0
    tier_map = {"Bronze": 500, "Silver": 1000, "Gold": 1500, "Platinum": 2000, 
                "Diamond": 2500, "Master": 3000, "Grandmaster": 3500, "Champion": 4000}
    try:
        tier, division = rank_string.split()
        return tier_map.get(tier, 0) + ((5 - int(division)) * 100)
    except: return 0

def get_rank_color(rank_string):
    if "Gold" in rank_string: return "gold"
    if "Platinum" in rank_string: return "95e1d3"
    if "Diamond" in rank_string: return "b9f2ff"
    return "orange"

def run_tracker():
    if not BATTLE_TAG: return
    
    # Fetch Data
    tag_id = BATTLE_TAG.replace('#', '-')
    url = f"https://overfast-api.tekrop.fr/players/{tag_id}/summary"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        current_rank = data.get('competitive', {}).get('rank', 'Unranked')
        
        # Update History
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f: history = json.load(f)
        
        history.append({"date": datetime.now().strftime("%Y-%m-%d"), "rank": current_rank})
        with open(HISTORY_FILE, 'w') as f: json.dump(history, f, indent=4)
        
        # Update Badge
        with open(BADGE_FILE, 'w') as f:
            json.dump({"schemaVersion": 1, "label": "Rank", "message": current_rank, "color": get_rank_color(current_rank)}, f)
            
        # Generate Chart
        dates = [entry['date'] for entry in history]
        nums = [rank_to_numeric(entry['rank']) for entry in history]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, nums, color='#f99e1a', marker='o')
        plt.title("Overwatch Rank Progression")
        plt.savefig(CHART_FILE)

if __name__ == "__main__":
    run_tracker()