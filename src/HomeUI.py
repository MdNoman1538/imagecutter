import json
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk


class HomeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cutter")
        self.root.geometry("600x500")

        # Initialize variables
        self.length_var = tk.StringVar()
        self.breadth_var = tk.StringVar()
        self.source_var = tk.StringVar()
        self.destination_var = tk.StringVar()
        self.x_axis_var = tk.StringVar()
        self.y_axis_var = tk.StringVar()
        self.distance_var = tk.StringVar()

        self.selected_images = []
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Load Parameters", command=self.load_parameters).grid(row=0, column=0, columnspan=3, pady=20)
        
        tk.Label(self.root, text="Length:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.length_var).grid(row=1, column=1)

        tk.Label(self.root, text="Breadth:").grid(row=2, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.breadth_var).grid(row=2, column=1)

        tk.Label(self.root, text="Source Location:").grid(row=3, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.source_var).grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_source).grid(row=3, column=2, padx=5)

        tk.Label(self.root, text="Destination Folder:").grid(row=4, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.destination_var).grid(row=4, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_destination).grid(row=4, column=2, padx=5)

        tk.Label(self.root, text="X Axis Location:").grid(row=5, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.x_axis_var).grid(row=5, column=1)

        tk.Label(self.root, text="Y Axis Location:").grid(row=6, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.y_axis_var).grid(row=6, column=1)

        tk.Label(self.root, text="Distance Between Rectangles:").grid(row=7, column=0, sticky='e', padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.distance_var).grid(row=7, column=1)

        tk.Button(self.root, text="Apply", command=self.submit).grid(row=8, column=0, columnspan=2, pady=20)
        tk.Button(self.root, text="Save Parameters", command=self.save_parameters).grid(row=8, column=1, pady=20)
        tk.Button(self.root, text="Edit View", command=self.edit_view).grid(row=8, column=2, pady=20)
        
    def edit_view(self):
        if not self.selected_images:
            messagebox.showwarning("No Images Selected", "Please select images first.")
            return

        # Create a new popup window
        popup = tk.Toplevel(self.root)
        popup.title("Edit View")
        popup.geometry("800x600")

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(popup)
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        row = 0
        col = 0
        for file_path in self.selected_images:
            img = Image.open(file_path)
            img.thumbnail((100, 100))
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(scrollable_frame, image=img)
            panel.image = img
            panel.grid(row=row, column=col, padx=5, pady=5)
            panel.bind("<Button-1>", lambda event, file_path=file_path: self.open_image_in_popup(file_path))
            col += 1
            if col == 4:
                col = 0
                row += 1
    
    def draw_rectangles(self, canvas, img_width, img_height):
        try:
            length = int(self.length_var.get())
            breadth = int(self.breadth_var.get())
            x_axis = int(self.x_axis_var.get())
            y_axis = int(self.y_axis_var.get())
            distance = int(self.distance_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integer values for length, breadth, x_axis, y_axis, and distance.")
            return

        # Clear any existing rectangles
        canvas.delete("rect")
     
        # Draw rectangles based on the parameters
        current_x = x_axis
        current_y = y_axis

        print(" before draw   inside function")
        while current_y + breadth <= img_height:
            while current_x + length <= img_width:
                canvas.create_rectangle(current_x, current_y, current_x + length, current_y + breadth, outline="red", tags="rect")
                current_x += length + distance
            current_x = x_axis
            current_y += breadth + distance
    
    

    def adjust_images(event):
            for widget in scrollable_frame.winfo_children():
                widget.grid_forget()

            width = event.width
            col_count = width // 120  # Assuming each image with padding takes 120px
            if col_count == 0:
                col_count = 1

    def open_image_in_popup(self, file_path):
        # Open the image
        img = Image.open(file_path)
        img_width, img_height = img.size

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the maximum allowed size for the popup window
        max_width = int(screen_width * 0.9)
        max_height = int(screen_height * 0.9)

        # Resize the image if it's larger than the maximum allowed size
        if img_width > max_width or img_height > max_height:
            img.thumbnail((max_width, max_height), Image.LANCZOS)
            img_width, img_height = img.size

        # Create a new popup window
        img_popup = tk.Toplevel(self.root)
        img_popup.title("Image View")

        # Set the size of the popup window
        popup_width = min(max_width, img_width) 
        popup_height = min(max_height, img_height)
        img_popup.geometry(f"{popup_width}x{popup_height}+100+100")  # Fixed coordinates (100, 100)

        # Display the image
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(img_popup, image=img)
        panel.image = img
        panel.pack(fill=tk.BOTH, expand=True)
        # Create a canvas to display the image
        canvas = tk.Canvas(img_popup, width=img_width, height=img_height)
        canvas.pack(fill=tk.BOTH, expand=True)

        # Display the image on the canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        print(" before draw")
        # Draw rectangles on the image
        self.draw_rectangles(canvas, img_width, img_height)

    def browse_source(self):
        folder_path = filedialog.askdirectory(title="Select Source Folder")
        if folder_path:
            self.source_var.set(folder_path)
            self.show_images_in_folder(folder_path)

    def load_parameters(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], title="Select JSON File")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    params = json.load(file)
                    self.length_var.set(params.get("length", ""))
                    self.breadth_var.set(params.get("breadth", ""))
                    self.destination_var.set(params.get("destination", ""))
                    self.x_axis_var.set(params.get("x_axis", ""))
                    self.y_axis_var.set(params.get("y_axis", ""))
                    self.distance_var.set(params.get("distance", ""))
                messagebox.showinfo("Load Successful", "Parameters loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load parameters: {e}")

    def save_parameters(self):
            params = {
                "length": self.length_var.get(),
                "breadth": self.breadth_var.get(),
                "destination": self.destination_var.get(),
                "x_axis": self.x_axis_var.get(),
                "y_axis": self.y_axis_var.get(),
                "distance": self.distance_var.get()
            }

            folder_path = filedialog.askdirectory(title="Select Folder to Save Parameters")
            if folder_path:
                file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if file_name:
                    with open(file_name, 'w') as file:
                        json.dump(params, file)
                    messagebox.showinfo("Save Successful", "Parameters saved successfully!")
    
    def select_image(self, file_path):
        if not hasattr(self, 'selected_images'):
         self.selected_images = []
        if file_path not in self.selected_images:
         self.selected_images.append(file_path)
         print(f"Selected: {file_path}")
       
        else:
         self.selected_images.remove(file_path)
         print(f"Deselected: {file_path}")
         print(f"Currently selected images: {self.selected_images}")
    
    def show_images_in_folder(self, folder_path):
        # Resize the main window
        self.root.geometry("1000x500")

        # Create a frame for displaying images
        image_frame = tk.Frame(self.root)
        image_frame.grid(row=0, column=3, rowspan=8, padx=10, pady=10)

        row = 0
        col = 0
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(folder_path, file_name)
                img = Image.open(file_path)
                img.thumbnail((100, 100))
                img = ImageTk.PhotoImage(img)
                panel = tk.Label(image_frame, image=img)
                panel.image = img
                panel.grid(row=row, column=col, padx=5, pady=5)
                panel.bind("<Button-1>", lambda event, file_path=file_path: self.on_image_click(event, file_path))
                col += 1
                if col == 3:
                    col = 0
                    row += 1
    
    
    def on_image_click(self, event, file_path):
        panel = event.widget
        if file_path in self.selected_images:
            img = Image.open(file_path)
            img.thumbnail((100, 100))
            panel.image = ImageTk.PhotoImage(img)
            panel.config(image=panel.image)
            self.selected_images.remove(file_path)
            print(f"Deselected: {file_path}")
        else:
            panel.image = panel.image._PhotoImage__photo.subsample(2, 2)
            panel.config(image=panel.image)
            self.selected_images.append(file_path)
            print(f"Selected: {file_path}")
            panel.bind("<Button-1>", lambda event, file_path=file_path: self.on_image_click(event, file_path))
        print(f"Currently selected images: {self.selected_images}")
    


    

    def browse_destination(self):
        folder_path = filedialog.askdirectory(title="Select Destination Folder")
        if folder_path:
            self.destination_var.set(folder_path)

    def submit(self):
        length = self.length_var.get()
        breadth = self.breadth_var.get()
        source = self.source_var.get()
        destination = self.destination_var.get()
        x_axis = self.x_axis_var.get()
        y_axis = self.y_axis_var.get()
        distance = self.distance_var.get()

        print(f"Length: {length}")
        print(f"Breadth: {breadth}")
        print(f"Source: {source}")
        print(f"Destination: {destination}")
        print(f"X Axis Location: {x_axis}")
        print(f"Y Axis Location: {y_axis}")
        print(f"Distance Between Rectangles: {distance}")
        messagebox.showinfo("Submission Successful", "Parameters submitted successfully!")