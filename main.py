import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
from utils.gui_helpers import get_asset_path
import subprocess
import sys
import os

# Function to start each game
def start_game(script_name):
    try:
        game_path = os.path.join(os.path.dirname(__file__), 'games', f"{script_name}.py")
        if not os.path.exists(game_path):
            raise FileNotFoundError(f"Game file not found: {game_path}")
        subprocess.Popen([sys.executable, game_path])
    except Exception as e:
        messagebox.showerror("Error", f"Cannot start the game: {e}")

# GUI setup
def launch_main_menu():
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created assets directory at: {assets_dir}")

    root = tk.Tk()
    root.title("Game Hub")
    root.geometry("600x600")
    root.resizable(False, False)
    root.configure(bg="#222831")

    tk.Label(root, text="Welcome to Game Hub", font=("Arial", 24, "bold"), fg="#00adb5", bg="#222831").pack(pady=20)

    # Games dictionary
    games = {
        "Tic Tac Toe": ("tic_tac_toe", "tic_tac_toe.png"),
        "Flappy Bird": ("flappy_bird", "flappy_bird.png"),
        "Brick Breaker": ("brick_breaker", "brick_breaker.png"),
        "SnakeGame": ("SnakeGame", "SnakeGame.png")
    }

    # Create buttons dynamically
    for game_name, (script, img_file) in games.items():
        frame = tk.Frame(root, bg="#222831")
        frame.pack(pady=10)

        try:
            img_path = get_asset_path(img_file)
            print(f"Attempting to load image: {img_path}")  # Debug print
            if not os.path.exists(img_path):
                print(f"Image file does not exist: {img_path}")  # Debug print
            img = Image.open(img_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)

            btn = tk.Button(frame, text=game_name, image=img, compound="left", padx=20, font=("Arial", 14),
                            command=lambda script=script: start_game(script), bg="#393e46", fg="white", bd=0)
            btn.image = img  # keep a reference!
            btn.pack()
        except Exception as e:
            print(f"Error details: {str(e)}")  # Debug print
            tk.Label(frame, text=f"Error loading {game_name}: {str(e)}", 
                     font=("Arial", 12), fg="red", bg="#222831").pack()

    tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14),
              bg="#ff5722", fg="white", padx=20, pady=10).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    launch_main_menu()
