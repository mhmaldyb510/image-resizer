import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

class ImageReSizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image ReSizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        self.original_image = None
        self.resized_image = None
        self.filename = None
        self.maintain_aspect = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel (original image)
        left_panel = tk.LabelFrame(main_frame, text="Original Image", bg="#f0f0f0", font=("Arial", 12))
        left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Right panel (resized image)
        right_panel = tk.LabelFrame(main_frame, text="Resized Image", bg="#f0f0f0", font=("Arial", 12))
        right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Control panel
        control_panel = tk.LabelFrame(main_frame, text="Controls", bg="#f0f0f0", font=("Arial", 12))
        control_panel.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Original image canvas
        self.original_canvas = tk.Canvas(left_panel, bg="white")
        self.original_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resized image canvas
        self.resized_canvas = tk.Canvas(right_panel, bg="white")
        self.resized_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control panel widgets
        # First row - Select image and display info
        file_frame = tk.Frame(control_panel, bg="#f0f0f0")
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        select_btn = ttk.Button(file_frame, text="Select Image", command=self.select_image)
        select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.image_info_label = tk.Label(file_frame, text="No image selected", bg="#f0f0f0")
        self.image_info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Second row - Width and height inputs
        dimensions_frame = tk.Frame(control_panel, bg="#f0f0f0")
        dimensions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(dimensions_frame, text="Width:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 5))
        self.width_entry = ttk.Entry(dimensions_frame, width=8)
        self.width_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.width_entry.bind("<KeyRelease>", self.on_width_change)
        
        tk.Label(dimensions_frame, text="Height:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(0, 5))
        self.height_entry = ttk.Entry(dimensions_frame, width=8)
        self.height_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.height_entry.bind("<KeyRelease>", self.on_height_change)
        
        maintain_aspect_check = ttk.Checkbutton(
            dimensions_frame, 
            text="Maintain Aspect Ratio", 
            variable=self.maintain_aspect
        )
        maintain_aspect_check.pack(side=tk.LEFT, padx=(0, 15))
        
        preview_btn = ttk.Button(dimensions_frame, text="Preview", command=self.preview_resize)
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = ttk.Button(dimensions_frame, text="Save Image", command=self.save_image)
        save_btn.pack(side=tk.LEFT)
        
    def select_image(self):
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        
        self.filename = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        
        if self.filename:
            try:
                self.original_image = Image.open(self.filename)
                self.display_original_image()
                self.update_image_info()
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(self.original_image.width))
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(self.original_image.height))
                self.preview_resize()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def display_original_image(self):
        if self.original_image:
            # Resize image to fit canvas while maintaining aspect ratio
            canvas_width = self.original_canvas.winfo_width()
            canvas_height = self.original_canvas.winfo_height()
            
            if canvas_width <= 1:  # Canvas not yet drawn
                canvas_width = 400
                canvas_height = 300
            
            img_width, img_height = self.original_image.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.tk_original_image = ImageTk.PhotoImage(resized)
            
            self.original_canvas.config(width=canvas_width, height=canvas_height)
            self.original_canvas.delete("all")
            self.original_canvas.create_image(
                canvas_width//2, canvas_height//2, 
                image=self.tk_original_image, 
                anchor=tk.CENTER
            )
    
    def update_image_info(self):
        if self.original_image:
            width, height = self.original_image.size
            filename = os.path.basename(self.filename)
            info_text = f"File: {filename} | Original Size: {width}x{height} pixels"
            self.image_info_label.config(text=info_text)
    
    def on_width_change(self, event=None):
        if self.maintain_aspect.get() and self.original_image:
            try:
                new_width = int(self.width_entry.get())
                original_width, original_height = self.original_image.size
                aspect_ratio = original_height / original_width
                new_height = int(new_width * aspect_ratio)
                
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, str(new_height))
            except ValueError:
                pass
    
    def on_height_change(self, event=None):
        if self.maintain_aspect.get() and self.original_image:
            try:
                new_height = int(self.height_entry.get())
                original_width, original_height = self.original_image.size
                aspect_ratio = original_width / original_height
                new_width = int(new_height * aspect_ratio)
                
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, str(new_width))
            except ValueError:
                pass
    
    def preview_resize(self):
        if not self.original_image:
            messagebox.showinfo("Info", "Please select an image first.")
            return
        
        try:
            new_width = int(self.width_entry.get())
            new_height = int(self.height_entry.get())
            
            if new_width <= 0 or new_height <= 0:
                messagebox.showerror("Error", "Width and height must be positive numbers.")
                return
            
            # Resize the image
            self.resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Display the resized image
            canvas_width = self.resized_canvas.winfo_width()
            canvas_height = self.resized_canvas.winfo_height()
            
            if canvas_width <= 1:  # Canvas not yet drawn
                canvas_width = 400
                canvas_height = 300
            
            img_width, img_height = self.resized_image.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            display_width = int(img_width * ratio)
            display_height = int(img_height * ratio)
            
            display_image = self.resized_image.resize((display_width, display_height), Image.LANCZOS)
            self.tk_resized_image = ImageTk.PhotoImage(display_image)
            
            self.resized_canvas.config(width=canvas_width, height=canvas_height)
            self.resized_canvas.delete("all")
            self.resized_canvas.create_image(
                canvas_width//2, canvas_height//2, 
                image=self.tk_resized_image, 
                anchor=tk.CENTER
            )
            
            # Update the canvas with new image dimensions
            resize_info = f"Resized: {new_width}x{new_height} pixels"
            self.resized_canvas.create_text(
                canvas_width//2, canvas_height - 20,
                text=resize_info,
                fill="black",
                font=("Arial", 10)
            )
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for width and height.")
    
    def save_image(self):
        if not self.resized_image:
            messagebox.showinfo("Info", "Please preview an image resize first.")
            return
        
        filetypes = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        
        save_path = filedialog.asksaveasfilename(
            title="Save Resized Image",
            filetypes=filetypes,
            defaultextension=".jpg"
        )
        
        if save_path:
            try:
                self.resized_image.save(save_path)
                messagebox.showinfo("Success", f"Image saved successfully to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageReSizerApp(root)
    
    # Update canvas on window resize
    def on_resize(event):
        if app.original_image:
            app.display_original_image()
        if app.resized_image:
            app.preview_resize()
    
    root.bind("<Configure>", on_resize)
    root.mainloop()