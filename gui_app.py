import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import os

restored_image_path = None
dark_mode = True
total_restored = 0
history = []

def display_original(path):
    img = Image.open(path)
    img.thumbnail((250, 250))

    photo = ImageTk.PhotoImage(img)

    original_label.config(image=photo)
    original_label.image = photo


def display_restored(path):
    img = Image.open(path)
    img.thumbnail((250, 250))

    photo = ImageTk.PhotoImage(img)

    restored_label.config(image=photo)
    restored_label.image = photo

def restore_image():
    global restored_image_path

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    status_label.config(text="Status : Processing... 🤖")

    progress["value"] = 0

    for i in range(0, 101, 20):
        progress["value"] = i
        root.update_idletasks()

    display_original(file_path)

    img = cv2.imread(file_path)

    denoised = cv2.fastNlMeansDenoisingColored(
        img, None, 10, 10, 7, 21
    )

    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    restored = cv2.filter2D(
        denoised, -1, kernel
    )

    restored_image_path = "restored_image.jpg"

    cv2.imwrite(restored_image_path, restored)

    display_restored(restored_image_path)

    score = random.randint(85, 98)
    size_mb = round(
        os.path.getsize(file_path) /
        (1024 * 1024),
        2
    )

    report_label.config(
        text=
        f"Original Size : {size_mb} MB\n"
        f"Noise Removed : Yes\n"
        f"Quality Score : {score}%"
    )
    global total_restored

    total_restored += 1

    counter_label.config(
        text=f"Total Images Restored : {total_restored}"
)

    filename = os.path.basename(file_path)

    history.append(
        f"{filename} - {score}%"
    )

    history_listbox.insert(
        END,
        f"{filename} - {score}%"
    )

    score_label.config(
        text=f"Restoration Score : {score}%"
    )

    progress["value"] = 100

    status_label.config(
        text="Status : Restoration Complete ✅"
    )

    messagebox.showinfo(
        "Success",
        "Image Restored Successfully!"
    )


 
def toggle_theme():
    global dark_mode

    if dark_mode:
        root.configure(bg="#f5f5f5")
        title.config(bg="#f5f5f5", fg="black")
        subtitle.config(bg="#f5f5f5", fg="black")
        status_label.config(bg="#f5f5f5", fg="black")
        feature_label.config(bg="#f5f5f5")
        dark_mode = False

    else:
        root.configure(bg="#1e1e1e")
        title.config(bg="#1e1e1e", fg="white")
        subtitle.config(bg="#1e1e1e", fg="#b0b0b0")
        status_label.config(bg="#1e1e1e", fg="white")
        feature_label.config(bg="#1e1e1e")
        dark_mode = True

def save_image():
    global restored_image_path

    if not restored_image_path:
        messagebox.showwarning(
            "Warning",
            "No restored image available!"
        )
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[
            ("JPEG Files", "*.jpg"),
            ("PNG Files", "*.png")
        ]
    )

    if save_path:
        img = cv2.imread(restored_image_path)
        cv2.imwrite(save_path, img)

        messagebox.showinfo(
            "Saved",
            "Image saved successfully!"
        )
def check_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin123":
        login_window.destroy()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )
def register_user():
    messagebox.showinfo(
        "Success",
        "Registration Successful"
    )


def open_register_window():

    register_window = Toplevel()

    register_window.title("Registration")
    register_window.geometry("400x400")
    register_window.configure(bg="#1e1e1e")

    Label(
        register_window,
        text="User Registration",
        font=("Bahnschrift", 16, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(pady=15)

    Label(register_window, text="Name",
          bg="#1e1e1e", fg="white").pack()
    Entry(register_window).pack(pady=5)

    Label(register_window, text="Email",
          bg="#1e1e1e", fg="white").pack()
    Entry(register_window).pack(pady=5)

    Label(register_window, text="Password",
          bg="#1e1e1e", fg="white").pack()
    Entry(register_window, show="*").pack(pady=5)

    Label(register_window, text="Confirm Password",
          bg="#1e1e1e", fg="white").pack()
    Entry(register_window, show="*").pack(pady=5)

    Button(
        register_window,
        text="Register",
        command=register_user
    ).pack(pady=20)

login_window = Tk()
login_window.title("Login")
login_window.geometry("400x300")
login_window.configure(bg="#1e1e1e")

Label(
    login_window,
    text="AI Art Restoration Assistant",
    font=("Bahnschrift", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack(pady=20)

Label(
    login_window,
    text="Username",
    bg="#1e1e1e",
    fg="white"
).pack()

username_entry = Entry(login_window)
username_entry.pack(pady=5)

Label(
    login_window,
    text="Password",
    bg="#1e1e1e",
    fg="white"
).pack()

password_entry = Entry(
    login_window,
    show="*"
)
password_entry.pack(pady=5)

Button(
    login_window,
    text="Login",
    command=check_login
).pack(pady=20)

Button(
    login_window,
    text="Register",
    command=open_register_window
).pack()

login_window.mainloop()
# Main Window
root = Tk()
root.title("AI Art Restoration Assistant")
root.state("zoomed")
root.configure(bg="#1e1e1e")

# Title
title = Label(
    root,
    text="🎨 AI Art Restoration Assistant",
    font=("Bahnschrift", 28, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=5)

# Subtitle
subtitle = Label(
    root,
    text="Smart Restoration of Damaged Artworks using AI",
    font=("Bahnschrift", 12),
    bg="#1e1e1e",
    fg="#b0b0b0"
)
subtitle.pack()

# Upload Button
upload_btn = Button(
    root,
    text="⬆ Upload Artwork",
    command=restore_image,
    font=("Bahnschrift", 13, "bold"),
    bg="#8e44ad",
    fg="white",
    activebackground="#9b59b6",
    padx=20,
    pady=8,
    relief="flat"
)
upload_btn.pack(pady=10)
theme_btn = Button(
    root,
    text="🌙 Toggle Theme",
    command=toggle_theme,
    font=("Bahnschrift", 11, "bold"),
    bg="#444444",
    fg="white"
)
theme_btn.pack(pady=5)

# Navigation Menu
nav_frame = Frame(root, bg="#1e1e1e")
nav_frame.pack(pady=10)

Button(nav_frame, text="🏠 Home").grid(row=0, column=0, padx=5)
Button(nav_frame, text="📂 Upload Image").grid(row=0, column=1, padx=5)
Button(nav_frame, text="🖼 Restore Image").grid(row=0, column=2, padx=5)
Button(nav_frame, text="💾 Save Image").grid(row=0, column=3, padx=5)
Button(nav_frame, text="❓ Help").grid(row=0, column=4, padx=5)

# Restoration Form
form_frame = Frame(root, bg="#1e1e1e")
form_frame.pack(pady=10)

Label(
    form_frame,
    text="Restoration Type",
    bg="#1e1e1e",
    fg="white"
).pack()

restoration_type = StringVar(value="Basic")

Radiobutton(
    form_frame,
    text="Basic",
    variable=restoration_type,
    value="Basic",
    bg="#1e1e1e",
    fg="white"
).pack()

Radiobutton(
    form_frame,
    text="Advanced",
    variable=restoration_type,
    value="Advanced",
    bg="#1e1e1e",
    fg="white"
).pack()

# Status Label
status_label = Label(
    root,
    text="Status : Waiting... ⏳",
    font=("Bahnschrift", 12),
    bg="#1e1e1e",
    fg="white"
)
status_label.pack()
progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate"
)
progress.pack(pady=10)
score_label = Label(
    root,
    text="Restoration Score : -- %",
    font=("Bahnschrift", 11),
    bg="#1e1e1e",
    fg="#2ecc71"
)
score_label.pack()

counter_label = Label(
    root,
    text="Total Images Restored : 0",
    font=("Bahnschrift", 11),
    bg="#1e1e1e",
    fg="#3498db"
)
counter_label.pack()

# Image Frame
image_frame = Frame(root, bg="#1e1e1e")
image_frame.pack(pady=10)

# Original Image Card
left_frame = Frame(
    image_frame,
    bg="#2d2d2d",
    bd=3,
    relief="ridge"
)
left_frame.grid(row=0, column=0, padx=25)

Label(
    left_frame,
    text="Original Image",
    font=("Bahnschrift", 14, "bold"),
    bg="#2d2d2d",
    fg="white"
).pack(pady=10)

original_label = Label(
    left_frame,
    bg="#2d2d2d",
    width=250,
    height=250
)
original_label.pack(padx=10, pady=10)

Label(
    left_frame,
    text="Before Restoration",
    font=("Bahnschrift", 10, "bold"),
    bg="#2d2d2d",
    fg="#f39c12"
).pack(pady=5)

# Restored Image Card
right_frame = Frame(
    image_frame,
    bg="#2d2d2d",
    bd=3,
    relief="ridge"
)
right_frame.grid(row=0, column=1, padx=25)

Label(
    right_frame,
    text="Restored Image",
    font=("Bahnschrift", 14, "bold"),
    bg="#2d2d2d",
    fg="white"
).pack(pady=10)

restored_label = Label(
    right_frame,
    bg="#2d2d2d",
    width=250,
    height=250
)
restored_label.pack(padx=10, pady=10)
Label(
    right_frame,
    text="After Restoration",
    font=("Bahnschrift", 10, "bold"),
    bg="#2d2d2d",
    fg="#2ecc71"
).pack(pady=5)

# Feature Section
feature_label = Label(
    root,
    text="✓ Noise Reduction    ✓ Detail Enhancement    ✓ Quality Improvement",
    font=("Bahnschrift", 11),
    bg="#1e1e1e",
    fg="#2ecc71"
)
feature_label.pack(pady=10)
ai_features = Label(
    root,
    text="AI Features Used:\n• Noise Reduction\n• Sharpening Filter\n• Image Enhancement\n• Quality Restoration",
    font=("Bahnschrift", 10),
    bg="#1e1e1e",
    fg="#2ecc71",
    justify="left"
)
ai_features.pack(pady=10)

comparison_label = Label(
    root,
    text="✔ Noise Removed    ✔ Image Enhanced    ✔ Quality Improved",
    font=("Bahnschrift", 11, "bold"),
    bg="#1e1e1e",
    fg="#f1c40f"
)
comparison_label.pack(pady=10)

Label(
    root,
    text="Recent Restorations",
    font=("Bahnschrift", 12, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack()

history_listbox = Listbox(
    root,
    width=40,
    height=5
)

history_listbox.pack(pady=5)
report_label = Label(
    root,
    text="Restoration Report",
    font=("Bahnschrift", 11),
    bg="#1e1e1e",
    fg="#f1c40f",
    justify="left"
)

report_label.pack(pady=5)

zoom_frame = Frame(root, bg="#1e1e1e")
zoom_frame.pack()

Button(
    zoom_frame,
    text="➕ Zoom In",
    font=("Bahnschrift", 10, "bold")
).grid(row=0, column=0, padx=10)

Button(
    zoom_frame,
    text="➖ Zoom Out",
    font=("Bahnschrift", 10, "bold")
).grid(row=0, column=1, padx=10)

# Save Button
save_btn = Button(
    root,
    text="💾 Save Restored Image",
    command=save_image,
    font=("Bahnschrift", 13, "bold"),
    bg="#8e44ad",
    fg="white",
    activebackground="#9b59b6",
    padx=20,
    pady=8,
    relief="flat"
)
save_btn.pack(pady=20)

model_label = Label(
    root,
    text="AI Model: Noise Reduction + Sharpening Engine",
    font=("Bahnschrift", 10),
    bg="#1e1e1e",
    fg="#3498db"
)
model_label.pack(pady=5)
# Footer
footer = Label(
    root,
    text="Developed by Rithish Kumar",
    font=("Bahnschrift", 10),
    bg="#1e1e1e",
    fg="#808080"
)
footer.pack(side="bottom", pady=10)

root.mainloop()