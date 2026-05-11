import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from compressor import compress_image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageCompressionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DCT Image Compression")
        self.geometry("900x600")
        
        self.image_path = None

        # --- Sidebar (Controls) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="DCT Compressor", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)
        
        self.select_btn = ctk.CTkButton(self.sidebar_frame, text="Select Image (.bmp)", command=self.select_image)
        self.select_btn.pack(pady=10, padx=20)
        
        self.path_label = ctk.CTkLabel(self.sidebar_frame, text="No image selected", font=ctk.CTkFont(size=10))
        self.path_label.pack(pady=(0, 10), padx=20)

        # F Entry
        self.f_label = ctk.CTkLabel(self.sidebar_frame, text="Macro-block size (F):")
        self.f_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.f_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 8")
        self.f_entry.pack(pady=5, padx=20)
        
        # d Entry
        self.d_label = ctk.CTkLabel(self.sidebar_frame, text="Cutoff threshold (d):")
        self.d_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.d_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 4")
        self.d_entry.pack(pady=5, padx=20)
        
        self.process_btn = ctk.CTkButton(self.sidebar_frame, text="Compress", command=self.process_image)
        self.process_btn.pack(pady=30, padx=20)

        # --- Main Area (Images) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        
        self.lbl_orig_title = ctk.CTkLabel(self.main_frame, text="Original Image", font=ctk.CTkFont(weight="bold"))
        self.lbl_orig_title.grid(row=0, column=0, pady=10)
        
        self.lbl_comp_title = ctk.CTkLabel(self.main_frame, text="Compressed Image", font=ctk.CTkFont(weight="bold"))
        self.lbl_comp_title.grid(row=0, column=1, pady=10)
        
        self.lbl_orig_img = ctk.CTkLabel(self.main_frame, text="")
        self.lbl_orig_img.grid(row=1, column=0, padx=10, pady=10)
        
        self.lbl_comp_img = ctk.CTkLabel(self.main_frame, text="")
        self.lbl_comp_img.grid(row=1, column=1, padx=10, pady=10)

    def select_image(self):
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("BMP Files", "*.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.image_path = filename
            self.path_label.configure(text=os.path.basename(filename))
            
            # Show original immediately if wanted, but processing will update both
            img = Image.open(self.image_path)
            img.thumbnail((350, 350))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.lbl_orig_img.configure(image=ctk_img, text="")
            self.lbl_comp_img.configure(image="", text="Run compression to see result")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
            
        try:
            F = int(self.f_entry.get())
            d = int(self.d_entry.get())
        except ValueError:
            messagebox.showerror("Error", "F and d must be integers.")
            return
            
        if F <= 0:
            messagebox.showerror("Error", "F must be greater than 0.")
            return
            
        if not (0 <= d <= 2 * F - 2):
            messagebox.showerror("Error", f"d must be between 0 and {2*F - 2}")
            return
            
        try:
            orig_img, comp_img = compress_image(self.image_path, F, d)
            
            # Resize for display
            orig_img.thumbnail((350, 350))
            comp_img.thumbnail((350, 350))
            
            ctk_orig = ctk.CTkImage(light_image=orig_img, dark_image=orig_img, size=orig_img.size)
            ctk_comp = ctk.CTkImage(light_image=comp_img, dark_image=comp_img, size=comp_img.size)
            
            self.lbl_orig_img.configure(image=ctk_orig, text="")
            self.lbl_comp_img.configure(image=ctk_comp, text="")
            
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

if __name__ == "__main__":
    app = ImageCompressionApp()
    app.mainloop()
