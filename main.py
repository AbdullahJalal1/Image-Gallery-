import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode as qr
import pickle  # To save and load the list of image paths

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Gallery")
        self.root.geometry("750x560")
        self.root.resizable(False, False)
        self.root.config(bg="#1E2A47")

        # List to store image paths
        self.image_files = []

        top_frame = tk.Frame(root, bg="white", bd=3, relief="solid")
        top_frame.pack(fill=tk.X, pady=10)

        # Add a heading at the top center of the window
        self.heading_label = tk.Label(top_frame, text="Image Gallery", font=("Helvetica", 25, "bold"), bg="#F4A300", fg="black", bd=1, height=1, width=55)
        self.heading_label.pack()

        # Create a frame to hold the images
        self.image_frame = tk.Frame(root, bg="#1E2A47")
        self.image_frame.pack(padx=15, pady=12, fill=tk.BOTH, expand=True)

        # Add a button to load images
        self.load_button = tk.Button(root, text="Load Images", command=self.open_images, font=("Helvetica", 14, "bold"), bg="#F4A300", fg="black", relief="solid", bd=1, height=1, width=20)
        self.load_button.place(x=250, y=400)

        # Add a button to save images
        self.save_button = tk.Button(root, text="Save Images", command=self.save_images, font=("Helvetica", 14, "bold"), bg="#F4A300", fg="black", relief="solid", bd=1, height=1, width=20)
        self.save_button.place(x=250, y=450)

        # Add a button to exit the application
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_application, font=("Helvetica", 14, "bold"), bg="#F4A300", fg="black", relief="solid", bd=1, height=1, width=20)
        self.exit_button.place(x=250, y=500)

        # Generate QR code and add it to the bottom left
        self.generate_qr_code()

        # Load previously saved images if any
        self.load_saved_images()

    def open_images(self):
        # Select multiple image files
        file_paths = filedialog.askopenfilenames(title="Open Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_paths:
            self.image_files = list(file_paths)
            self.display_images()

    def display_images(self):
        # Clear any previously displayed images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Add images to the frame in a grid layout
        row = 0
        col = 0
        max_columns = 3  # Number of images per row

        for index, image_path in enumerate(self.image_files):
            # Open the image and resize it
            image = Image.open(image_path)
            image = image.resize((220, 135))  # Resize the image to a fixed size
            tk_image = ImageTk.PhotoImage(image)

            # Create a label to display the image with a thinner border and smaller padding
            image_label = tk.Label(self.image_frame, image=tk_image, bd=2, relief="solid", padx=2, pady=2, bg="#1E2A47")
            image_label.image = tk_image  # Keep a reference to the image
            image_label.grid(row=row, column=col, padx=5, pady=5)

            # Add hover effect on the image (change border color on hover)
            image_label.bind("<Enter>", lambda e, label=image_label: self.on_hover(label))
            image_label.bind("<Leave>", lambda e, label=image_label: self.on_leave(label))

            # Bind click event to show the image in a larger view
            image_label.bind("<Button-1>", lambda e, path=image_path: self.show_large_image(path))

            # Update the grid position
            col += 1
            if col == max_columns:
                col = 0
                row += 1

    def on_hover(self, label):
        # Change the border color when hovering
        label.config(highlightbackground="#FF6347", highlightthickness=3)

    def on_leave(self, label):
        # Reset the border color when not hovering
        label.config(highlightbackground="#1E2A47", highlightthickness=3)

    def show_large_image(self, image_path):
        # Open the image and resize it for the larger view
        image = Image.open(image_path)
        image = image.resize((800, 600))  # Resize to a larger size
        tk_image = ImageTk.PhotoImage(image)

        # Create a new top-level window to display the large image
        top_window = tk.Toplevel(self.root)
        top_window.title("Large Image")
        top_window.geometry("800x600")
        top_window.config(bg="#1E2A47")

        # Create a label to display the large image
        large_image_label = tk.Label(top_window, image=tk_image, bg="#1E2A47")
        large_image_label.image = tk_image  # Keep a reference to the image
        large_image_label.pack(expand=True)

        # Add a close button with updated style
        close_button = tk.Button(top_window, text="Close", command=top_window.destroy, font=("Helvetica", 14, "bold"), bg="#F4A300", fg="black")
        close_button.pack(pady=10)

    def generate_qr_code(self):
        # Generate QR code for the specified URL
        img = qr.make("https://www.linkedin.com/in/abdullah-ibne-jalal-65a6312ab/")
        
        # Resize the image to 130x120 pixels
        img = img.resize((157, 104))

        # Convert the image to a format that Tkinter can display
        tk_img = ImageTk.PhotoImage(img)

        # Add the QR code to the bottom left of the window
        qr_label = tk.Label(self.root, image=tk_img, bg="#1E2A47")
        qr_label.image = tk_img  # Keep a reference to the image
        qr_label.place(x=550, y=430)

        # Add the artist heading above the QR code
        artist_label = tk.Label(self.root, text="About", font=("Helvetica", 14, "bold"), bg="#F4A300", fg="black", relief="solid", bd=1, height=1, width=13)
        artist_label.place(x=550, y=400)  # Position above the QR code

    def save_images(self):
        # Save the image file paths to a pickle file
        with open("saved_images.pkl", "wb") as f:
            pickle.dump(self.image_files, f)
        print("Images saved!")

    def load_saved_images(self):
        # Load the saved image file paths from a pickle file
        try:
            with open("saved_images.pkl", "rb") as f:
                self.image_files = pickle.load(f)
                self.display_images()
        except FileNotFoundError:
            # If no saved file exists, do nothing
            pass

    def exit_application(self):
        # Exit the application
        self.root.quit()


root = tk.Tk()
viewer = ImageViewer(root)
root.mainloop()
