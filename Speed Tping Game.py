import tkinter as tk
import time
from random_word import RandomWords
import random

# Global variables
level = 1
lives = 5
start_time = None
level_start_time = None
total_time_played = 0
game_running = False
notification = ""

# Random word generator
r = RandomWords()

# Special sentence generator for typing levels (50 sentences)
special_sentences = [
    "Typing fast can be fun, but accuracy is key.",
    "Practice makes perfect in any skill, especially typing.",
    "The quick brown fox jumps over the lazy dog.",
    "Consistency and patience lead to improvement over time.",
    "Don't let typos discourage you from continuing your progress.",
    "A journey of a thousand miles begins with a single step.",
    "To err is human; to forgive is divine.",
    "The early bird catches the worm.",
    "A stitch in time saves nine.",
    "Better late than never, but never late is better.",
    "Fortune favors the brave.",
    "Actions speak louder than words.",
    "A picture is worth a thousand words.",
    "Every cloud has a silver lining.",
    "Where there's a will, there's a way.",
    "Honesty is the best policy.",
    "Patience is a virtue.",
    "Silence is golden.",
    "A watched pot never boils.",
    "Absence makes the heart grow fonder.",
    "Barking up the wrong tree.",
    "Burning the midnight oil.",
    "Caught between a rock and a hard place.",
    "Cry over spilled milk.",
    "Cutting corners never leads to success.",
    "Don't count your chickens before they hatch.",
    "Don't judge a book by its cover.",
    "Every rose has its thorn.",
    "Great minds think alike.",
    "Hit the nail on the head.",
    "If it ain't broke, don't fix it.",
    "It takes two to tango.",
    "Laughter is the best medicine.",
    "Let the cat out of the bag.",
    "Look before you leap.",
    "Make hay while the sun shines.",
    "Necessity is the mother of invention.",
    "No pain, no gain.",
    "Old habits die hard.",
    "Out of sight, out of mind.",
    "Practice what you preach.",
    "Rome wasn't built in a day.",
    "The pen is mightier than the sword.",
    "The squeaky wheel gets the grease.",
    "Time flies when you're having fun.",
    "Two wrongs don't make a right.",
    "When in Rome, do as the Romans do.",
    "When the going gets tough, the tough get going.",
    "You can't judge a fish by its ability to climb a tree.",
    "You miss 100% of the shots you don't take."
]
def display_notification(message):
    notification_label.config(text=message)
    root.after(2000, lambda: notification_label.config(text=""))

# Function to check if it's a special level
def is_special_level(level):
    return level % 5 == 0

# Generate random words or sentence dynamically based on level
def generate_word_or_sentence(level):
    try:
        if is_special_level(level):  # Special typing level every 5 levels
            return random.choice(special_sentences)
        elif level <= 20:
            return r.get_random_word()  # 1 word for levels 1-20
        elif level <= 40:
            return ' '.join([r.get_random_word() for _ in range(2)])  # 2 words for levels 21-40
        else:
            return ' '.join([r.get_random_word() for _ in range(3)])  # 3 words for levels 41+
    except Exception as e:
        print(f"Error fetching word: {e}")
        return "error"

# Time limit per level
def get_time_for_level(level):
    # Get the time for the CURRENT level
    if is_special_level(level=level-1):  # Special level every 5 levels with 2 minutes (120 seconds)
        return 120
    else:
        return 10  # Regular level time limit

# Start a new level
def next_level():
    global level, level_start_time
    if lives > 0:
       
        # Start timing for the new level
        level_start_time = time.time()

        # Display the word/sentence for the new level
        current_word = generate_word_or_sentence(level)
        word_label.config(text=current_word)
        level_label.config(text=f"Level: {level}")
        
        # Set the entry box to be empty and ready for input
        entry.delete(0, tk.END)
        entry.focus_set()
         # Increment level FIRST before generating the word or sentence
        level += 1


        # Start the timer countdown for this level
        update_timers()
    else:
        game_over()

# Update total time played and per-level countdown timer
def update_timers():
    global total_time_played
    if not game_running:
        return

    current_time = time.time()
    
    # Update total time played
    total_time_played = int(current_time - start_time)
    total_time_label.config(text=f"Total Time Played: {total_time_played} sec")
    
    # Update countdown timer for current level
    level_elapsed_time = current_time - level_start_time
    level_time_left = max(0, get_time_for_level(level) - int(level_elapsed_time))
    countdown_label.config(text=f"Time Remaining: {level_time_left} sec")
    
    if level_time_left == 0:
        display_notification("Oops, time finished!")
        life_lost()

    root.after(1000, update_timers)

# Handle life lost and move to the next level
def life_lost():
    global lives
    lives -= 1
    update_life()
    if lives > 0:
        next_level()
    else:
        game_over()

# Update lives on screen (heart shapes)
def update_life():
    for i in range(5):
        if i < lives:
            life_hearts[i].config(text="♥", fg="red")  # Filled heart
        else:
            life_hearts[i].config(text="♡", fg="grey")  # Outlined heart
    
    if lives <= 0:
        game_over()

# Game over screen with final score
def game_over():
    global game_running
    if not game_running:
        return
    game_running = False

    game_over_screen = tk.Toplevel(root)
    game_over_screen.title("Game Over")
    game_over_screen.geometry("400x300")
    game_over_screen.resizable(False, False)

    msg = f"Game Over!\nLevels Completed: {level - 1}"
    tk.Label(game_over_screen, text=msg, font=('Helvetica', 14), justify=tk.CENTER).pack(pady=20)

    def close_game():
        root.destroy()

    tk.Button(game_over_screen, text="Exit", command=close_game, font=('Helvetica', 12)).pack(pady=10)

# Check input and move to next level or deduct life
def check_input(event):
    global lives, game_running
    if not game_running:
        return

    user_input = entry.get().strip()
    current_text = word_label.cget("text")
    if user_input == current_text:
        next_level()
    else:
        display_notification("You misyped the word!")
        lives -= 1
        update_life()
        if lives > 0:
            next_level()
        else:
            game_over()
    entry.delete(0, tk.END)

# Start the game
def start_game():
    global level, lives, start_time, level_start_time, game_running
    level = 1
    lives = 5
    start_time = time.time()
    level_start_time = time.time()
    game_running = True
    next_level()
    update_timers()

# GUI setup
root = tk.Tk()
root.title("Typing Test Game")
root.state('zoomed')  # Open in maximized window with standard controls
root.resizable(True, True)  # Allow resizing

# Welcome screen
def welcome_screen():
    welcome_frame = tk.Frame(root)
    welcome_frame.pack(expand=True)

    tk.Label(welcome_frame, text="Welcome to the Typing Test Game!", font=('Helvetica', 18, 'bold')).pack(pady=20)
    tk.Label(welcome_frame, text="Enter your name:", font=('Helvetica', 14)).pack(pady=10)

    player_name_entry = tk.Entry(welcome_frame, font=('Helvetica', 14), width=30)
    player_name_entry.pack(pady=10)

    def start():
        global player_name
        player_name = player_name_entry.get().strip()
        if player_name:
            welcome_frame.destroy()
            main_game_screen()
        else:
            tk.messagebox.showwarning("Input Error", "Please enter your name to start the game.")

    tk.Button(welcome_frame, text="Start Game", command=start, font=('Helvetica', 14), bg='green', fg='white').pack(pady=20)

# Main game screen
def main_game_screen():
    global word_label, entry, level_label, total_time_label, countdown_label, life_hearts, notification_label

    game_frame = tk.Frame(root)
    game_frame.pack(pady=20)

    # Player Name
    tk.Label(game_frame, text=f"Player: {player_name}", font=('Helvetica', 14)).pack(pady=5)

    # Lives as Heart Shapes
    lives_frame = tk.Frame(game_frame)
    lives_frame.pack(pady=10)
    life_hearts = [tk.Label(lives_frame, text="♥", font=('Helvetica', 18), fg="red") for _ in range(5)]
    for heart in life_hearts:
        heart.pack(side=tk.LEFT, padx=5)

    # Timer and level labels at the top of the screen
    timer_frame = tk.Frame(game_frame)
    timer_frame.pack(pady=10)
    
    level_label = tk.Label(timer_frame, text=f"Level: {level}", font=('Helvetica', 14))
    level_label.pack(side=tk.LEFT, padx=10)
    
    total_time_label = tk.Label(timer_frame, text="Total Time Played: 0 sec", font=('Helvetica', 14))
    total_time_label.pack(side=tk.LEFT, padx=10)
    
    countdown_label = tk.Label(timer_frame, text="Time Remaining: 0 sec", font=('Helvetica', 14))
    countdown_label.pack(side=tk.LEFT, padx=10)

    # Word label (current word/sentence to type)
    word_label = tk.Label(game_frame, text="", font=('Helvetica', 20, 'bold'))
    word_label.pack(pady=20)

    notification_label = tk.Label(timer_frame, text="", font=('Helvetica', 14), fg="red")
    notification_label.pack(side=tk.LEFT, padx=10)

    # Input box for typing
    entry = tk.Entry(game_frame, font=('Helvetica', 18), width=40)
    entry.pack(pady=10)
    entry.bind("<Return>", check_input)

    # Start the game
    start_game()

    # Instructions on the right
    instructions_frame = tk.Frame(game_frame)
    instructions_frame.pack(side=tk.RIGHT)
    instructions_text = (
        "Instructions:\n"
        "- Type the words exactly as shown (case-sensitive).\n"
        "- Punctuation must match exactly.\n"
        "- You lose a life if you mistype or run out of time.\n"
        "- Special level every 5 levels with a sentence."
    )
    tk.Label(instructions_frame, text=instructions_text, font=('Helvetica', 12), justify=tk.LEFT).pack()


# Show the welcome screen
welcome_screen()

# Run the GUI
root.mainloop()
