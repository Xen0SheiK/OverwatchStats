import customtkinter as ctk
import json
import os
from PIL import Image

# Use the dark theme for that gamer aesthetic
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class OverwatchStatsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Overwatch Rank Tracker")
        self.geometry("600x450")

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="OW Stats", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.update_btn = ctk.CTkButton(self.sidebar, text="Fetch Stats", command=self.update_stats)
        self.update_btn.grid(row=1, column=0, padx=20, pady=10)

        # --- Main View ---
        self.rank_label = ctk.CTkLabel(self, text="Current Rank: Loading...", font=ctk.CTkFont(size=24))
        self.rank_label.grid(row=0, column=1, padx=20, pady=20)

        # Space for your generated graph
        self.graph_display = ctk.CTkLabel(self, text="Graph will appear here")
        self.graph_display.grid(row=1, column=1, padx=20, pady=20)
        
        self.load_local_data()

    def load_local_data(self):
        if os.path.exists('history.json'):
            with open('history.json', 'r') as f:
                data = json.load(f)
                latest = data[-1]
                self.rank_label.configure(text=f"Current Rank: {latest['rank']}")

    def update_stats(self):
        # You can import your main.py function here to trigger a live update
        self.rank_label.configure(text="Updating...")
        print("Triggering main.py logic...")

if __name__ == "__main__":
    app = OverwatchStatsApp()
    app.mainloop()