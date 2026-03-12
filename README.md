# 🛡️ Overwatch Stats Auto-Tracker

[![Overwatch Auto-Tracker](https://github.com/PH4MInfoTech/OverwatchStats/actions/workflows/daily_track.yml/badge.svg)](https://github.com/PH4MInfoTech/OverwatchStats/actions/workflows/daily_track.yml)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An automated data pipeline that tracks Overwatch 2 competitive ranks, generates historical progression charts, and updates dynamic GitHub profile badges daily.

---

## 🚀 Live Stats
| Current Rank | Rank History |

| [Overwatch Rank](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/PH4MInfoTech/OverwatchStats/main/badge.json?v=1)|
| ![Rank Progression](https://raw.githubusercontent.com/PH4MInfoTech/OverwatchStats/main/rank_history.png) |

---

## 🛠️ Features
* **Automated Daily Tracking:** Powered by GitHub Actions to fetch data every 24 hours.
* **Dynamic Badges:** Custom logic updates badge colors based on your competitive tier (Gold, Platinum, etc.).
* **Trend Analysis:** Automatically detects and displays rank momentum (📈/📉).
* **Data Visualization:** Generates a time-series plot of your rank journey using Matplotlib.

## 🧰 Tech Stack
* **Language:** Python 3.x
* **Automation:** GitHub Actions (CI/CD)
* **API:** OverFast API (Blizzard Data)
* **Libraries:** Requests, Matplotlib, JSON

## 🔧 Setup & Installation

1. **Fork the Repository:** Click the "Fork" button at the top right of this page.

2. **Add Your BattleTag Secret:**
   Go to **Settings > Secrets and variables > Actions** and create a New Repository Secret:
   * **Name:** `BATTLE_TAG`
   * **Value:** `YourName#1234`

3. **Enable Workflow Permissions:**
   Go to **Settings > Actions > General**. Under "Workflow permissions," select **"Read and write permissions"** so the bot can save your stats.

4. **Manual Run:**
   Go to the **Actions** tab, select "Overwatch Auto-Tracker," and click **Run workflow** to generate your first badge!

---

## 📂 Project Structure
```text
OverwatchStats/
├── .github/workflows/
│   └── daily_track.yml   # Automation Schedule
├── main.py               # Core Logic & API Integration
├── history.json          # Historical Data Storage
├── badge.json            # Dynamic Shield Data
└── requirements.txt      # Project Dependencies
