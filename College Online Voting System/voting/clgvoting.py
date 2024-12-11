import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="voter_details"
)

# Global variables
candidates = {"Candidate A": 0, "Candidate B": 0, "Candidate C": 0}
voted_users = set()
current_user = None
voting_frozen = False

# Admin credentials
admin_username = "admin"
admin_password = "admin"

users_name = set()

# Function to fetch regular users from the database and populate the 'users_name' set
def fetch_regular_users():
    mycursor = mydb.cursor()
    sql = "SELECT username FROM users"
    mycursor.execute(sql)
    users_result = mycursor.fetchall()
    for user in users_result:
        users_name.add(user)

# Call this function at the beginning to fetch regular users from the database
fetch_regular_users()

# Function to authenticate user from the database
def authenticate(username, password):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    user = mycursor.fetchone()
    if user:
        return True
    elif(username == admin_username and password == admin_password):
        return True
    else:
        return False

# Function to handle login
def on_login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        if username in voted_users:
            messagebox.showerror("Error", "You have already voted.")
            return
        current_user = username
        messagebox.showinfo("Success", "Login successful!")
        # Clear entry fields after successful login
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        if authenticate(username, admin_password):  # Check if the user is admin
            freeze_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Place the freeze button in login frame
            username_entry.config(state="disabled")
            password_entry.config(state="disabled")
            login_button.config(state="disabled")
            return  # Do nothing for admin login, let the freeze button handle it
        else:
            vote_button["state"] = tk.NORMAL  # Enable vote button for regular users
            vote_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Show vote frame covering the entire window
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Function to handle voting
def vote():
    global voted_users
    global current_user
    global candidates
    global voting_frozen

    if voting_frozen:
        messagebox.showerror("Error", "Voting is currently frozen.")
        return

    candidate = selected_candidate.get()
    if not candidate:
        messagebox.showerror("Error", "Please select a candidate.")
        return

    voted_users.add(current_user)
    candidates[candidate] += 1

    messagebox.showinfo("Success", f"You have voted for {candidate}. Thank you!")

    if len(voted_users) == len(users_name):  # Check if all regular users have voted
        if admin_username not in voted_users:  # Check if admin has voted
            messagebox.showinfo("Voting Completed", "All users have voted.")
            show_results()  # Show results when all regular users have voted
            display_welcome()
    else:
        display_welcome()  # Show welcome page for the next user

# Function to handle admin freeze
def freeze_voting():
    global voting_frozen
    voting_frozen = True
    messagebox.showinfo("Voting Frozen", "Voting has been frozen.")
    show_results()

# Function to display login page
def display_login():
    welcome_frame.place_forget()
    login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    freeze_button.place_forget()  # Remove freeze button from other frames
    freeze_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Place the freeze button in login frame

# Function to display welcome page
def display_welcome():
    vote_frame.place_forget()
    login_frame.place_forget()
    welcome_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    selected_candidate.set("Candidate")

# Function to display results
def show_results():
    results_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    results_label = tk.Label(results_frame, text="Results:", font=("Arial", 20))
    results_label.pack(pady=20)

    for candidate, votes in candidates.items():
        candidate_result = tk.Label(results_frame, text=f"{candidate}: {votes}", font=("Arial", 16))
        candidate_result.pack()

# Function to start voting
def start_voting():
    welcome_frame.place_forget()
    login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Main window
root = tk.Tk()
root.title(" College Online Voting System")

# Set window to be resizable and maximizable
root.resizable(True, True)

# Function to load and stretch an image
def load_and_stretch_image(image_path, width, height):
    img = Image.open(image_path)
    img = img.resize((width, height))
    return ImageTk.PhotoImage(img)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set initial window size
root.geometry(f"{screen_width}x{screen_height}")

# Create background images for welcome, login, vote, and results frames
welcome_bg_image = load_and_stretch_image("welcome.jpeg", screen_width, screen_height)
login_bg_image = load_and_stretch_image("login.jpg", screen_width, screen_height)
vote_bg_image = load_and_stretch_image("usersvote.jpg", screen_width, screen_height)
res_bg_image = load_and_stretch_image("Results.jpg", screen_width, screen_height)

# Create welcome frame with background image using label
welcome_frame = tk.Label(root, image=welcome_bg_image)
welcome_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create "Let's Vote" button in welcome frame
start_voting_button = tk.Button(welcome_frame, text="Let's Vote", command=start_voting, font=("Arial", 20), bg="blue", fg="white")
start_voting_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create login frame with background image using label
login_frame = tk.Label(root, image=login_bg_image)

# Create a frame to hold login widgets
login_widget_frame = tk.Frame(login_frame, bg="light blue")
login_widget_frame.place(relx=0.3, rely=0.5, relwidth=0.3, relheight=0.3, anchor=tk.CENTER)

# Create login widgets
username_label = tk.Label(login_widget_frame, text="Username:", font=("Arial", 12), bg="blue", fg="white")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(login_widget_frame, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=5)
password_label = tk.Label(login_widget_frame, text="Password:", font=("Arial", 12), bg="blue", fg="white")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(login_widget_frame, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Create login button
login_button = tk.Button(login_widget_frame, text="Login", command=on_login, font=("Arial", 12), bg="blue", fg="white")
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create vote frame with background image using label
vote_frame = tk.Label(root, image=vote_bg_image)

# Create a frame to hold vote widgets
vote_widget_frame = tk.Frame(vote_frame, bg="light blue")
vote_widget_frame.place(relx=0.5, rely=0.4, relwidth=0.3, relheight=0.3, anchor=tk.CENTER)

# Create vote widgets
candidate_label = tk.Label(vote_widget_frame, text="Select Candidate:", font=("Arial", 16), bg="blue", fg="white")
candidate_label.grid(row=0, column=0, padx=10, pady=5)

# Create dropdown menu for candidate selection
selected_candidate = tk.StringVar() # Set initial value
candidate_options = list(candidates.keys())
selected_candidate.set("Candidate")  # Set default value
candidate_dropdown = tk.OptionMenu(vote_widget_frame, selected_candidate, *candidate_options)
candidate_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Create vote button
vote_button = tk.Button(vote_widget_frame, text="Vote", command=vote, font=("Arial", 12), bg="blue", fg="white")
vote_button.grid(row=1, column=0, columnspan=2, pady=10)

# Create results frame with background image using label
results_frame = tk.Label(root, image=res_bg_image)

# Create freeze button for admin
freeze_button = tk.Button(login_widget_frame, text="Freeze Voting", command=freeze_voting, font=("Arial", 12), bg="blue", fg="white")

# Display the welcome frame initially
display_welcome()

# Run the main event loop
root.mainloop()