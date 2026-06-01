import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import io
from compressor import compress_image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ImageCompressionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DCT Image Compression")
        self.geometry("900x600")
        self.image_path = None
        self.compressed_image_data = None

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
        self.d_label = ctk.CTkLabel(self.sidebar_frame, text="Cutoff threshold (d <= 2F - 2):")
        self.d_label.pack(pady=(10, 0), padx=20, anchor="w")
        
        self.d_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 4")
        self.d_entry.pack(pady=5, padx=20)
        
        self.process_btn = ctk.CTkButton(self.sidebar_frame, text="Compress", command=self.process_image)
        self.process_btn.pack(pady=(30, 10), padx=20)
        
        self.save_btn = ctk.CTkButton(self.sidebar_frame, text="Save Compressed", command=self.save_image, state="disabled")
        self.save_btn.pack(pady=10, padx=20)

        # Zoom Slider
        self.zoom_label = ctk.CTkLabel(self.sidebar_frame, text="Zoom scale: 100%")
        self.zoom_label.pack(pady=(20, 0), padx=20, anchor="w")
        self.zoom_slider = ctk.CTkSlider(self.sidebar_frame, from_=0.1, to=5.0, command=self.update_zoom)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(pady=5, padx=20)

        # Internal references for image resizing
        self.display_orig_img = None
        self.display_comp_img = None

        # --- Main Area (Images) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=10)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Labels for Images
        self.lbl_orig_title = ctk.CTkLabel(self.main_frame, text="Original Image", font=ctk.CTkFont(weight="bold"))
        self.lbl_orig_title.grid(row=0, column=0, pady=10)
        
        self.lbl_comp_title = ctk.CTkLabel(self.main_frame, text="Compressed Image", font=ctk.CTkFont(weight="bold"))
        self.lbl_comp_title.grid(row=0, column=1, pady=10)
        
        self.frame_orig_img = ctk.CTkFrame(self.main_frame, width=350, height=350, fg_color="gray15")
        self.frame_orig_img.grid(row=1, column=0, padx=10, pady=10)
        self.frame_orig_img.pack_propagate(False)
        self.frame_orig_img.grid_propagate(False)

        self.frame_comp_img = ctk.CTkFrame(self.main_frame, width=350, height=350, fg_color="gray15")
        self.frame_comp_img.grid(row=1, column=1, padx=10, pady=10)
        self.frame_comp_img.pack_propagate(False)
        self.frame_comp_img.grid_propagate(False)
        
        self.lbl_orig_img = ctk.CTkLabel(self.frame_orig_img, text="")
        self.lbl_orig_img.place(x=175, y=175, anchor="center")
        
        self.lbl_comp_img = ctk.CTkLabel(self.frame_comp_img, text="")
        self.lbl_comp_img.place(x=175, y=175, anchor="center")
        
        # Setup panning variables and bindings
        self.pan_x = 175
        self.pan_y = 175
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        self.lbl_orig_img.bind("<ButtonPress-1>", self.on_drag_start)
        self.lbl_orig_img.bind("<B1-Motion>", self.on_drag_motion)
        self.lbl_comp_img.bind("<ButtonPress-1>", self.on_drag_start)
        self.lbl_comp_img.bind("<B1-Motion>", self.on_drag_motion)
        
        self.lbl_orig_size = ctk.CTkLabel(self.main_frame, text="")
        self.lbl_orig_size.grid(row=2, column=0, pady=(0, 10))
        
        self.lbl_comp_size = ctk.CTkLabel(self.main_frame, text="")
        self.lbl_comp_size.grid(row=2, column=1, pady=(0, 10))

    def on_drag_start(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

    def on_drag_motion(self, event):
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y
        
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
        self.pan_x += dx
        self.pan_y += dy
        
        self.lbl_orig_img.place(x=self.pan_x, y=self.pan_y, anchor="center")
        self.lbl_comp_img.place(x=self.pan_x, y=self.pan_y, anchor="center")

    def select_image(self):
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("BMP Files", "*.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.image_path = filename
            self.path_label.configure(text=os.path.basename(filename))
            
            img = Image.open(self.image_path)
            self.display_orig_img = img.copy()
            self.display_comp_img = None
            
            orig_kb = os.path.getsize(self.image_path) / 1024
            w, h = img.size
            self.lbl_orig_size.configure(text=f"Resolution: {w}x{h}\nFile Size: {orig_kb:.2f} KB")
            self.lbl_comp_size.configure(text="")
            
            self.pan_x = 175
            self.pan_y = 175
            self.lbl_orig_img.place(x=self.pan_x, y=self.pan_y, anchor="center")
            self.lbl_comp_img.place(x=self.pan_x, y=self.pan_y, anchor="center")
            
            self.zoom_slider.set(1.0)
            self.update_zoom(1.0)
            
            self.lbl_comp_img.configure(image="", text="Run compression to see result")
            self.save_btn.configure(state="disabled")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
            
        try:
            macroblock_size = int(self.f_entry.get())
            cutoff_threshold = int(self.d_entry.get())
        except ValueError:
            messagebox.showerror("Error", "F and d must be integers.")
            return
            
        if macroblock_size <= 0:
            messagebox.showerror("Error", "F must be greater than 0.")
            return
            
        if not (0 <= cutoff_threshold <= 2 * macroblock_size - 2):
            messagebox.showerror("Error", f"d must be between 0 and {2 * macroblock_size - 2}")
            return
            
        try:
            orig_img, comp_img = compress_image(self.image_path, macroblock_size, cutoff_threshold)
            
            # Save raw unmodified image data for potential saving
            self.compressed_image_data = comp_img.copy()
            self.save_btn.configure(state="normal")
            
            orig_kb = os.path.getsize(self.image_path) / 1024
            orig_w, orig_h = orig_img.size
            comp_w, comp_h = comp_img.size
            
            io_buffer = io.BytesIO()
            self.compressed_image_data.save(io_buffer, format="JPEG")
            comp_kb = len(io_buffer.getvalue()) / 1024
            
            self.lbl_orig_size.configure(text=f"Resolution: {orig_w}x{orig_h}\nFile Size: {orig_kb:.2f} KB")
            self.lbl_comp_size.configure(text=f"Resolution: {comp_w}x{comp_h}\nEst. Size (JPEG): {comp_kb:.2f} KB")
            
            self.display_orig_img = orig_img.copy()
            self.display_comp_img = comp_img.copy()
            self.update_zoom(self.zoom_slider.get())
            
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def update_zoom(self, value):
        scale = float(value)
        self.zoom_label.configure(text=f"Zoom scale: {int(scale * 100)}%")
        
        if self.display_orig_img:
            # We resize keeping aspect ratio relative to a baseline size, e.g., 350 max
            base_w, base_h = self.display_orig_img.size
            ratio = min(350 / base_w, 350 / base_h)
            new_size = (int(base_w * ratio * scale), int(base_h * ratio * scale))
            
            if new_size[0] > 0 and new_size[1] > 0:
                resized_orig = self.display_orig_img.resize(new_size, Image.LANCZOS)
                ctk_orig = ctk.CTkImage(light_image=resized_orig, dark_image=resized_orig, size=resized_orig.size)
                self.lbl_orig_img.configure(image=ctk_orig, text="")
                
        if self.display_comp_img:
            base_w, base_h = self.display_comp_img.size
            ratio = min(350 / base_w, 350 / base_h)
            new_size = (int(base_w * ratio * scale), int(base_h * ratio * scale))
            
            if new_size[0] > 0 and new_size[1] > 0:
                resized_comp = self.display_comp_img.resize(new_size, Image.LANCZOS)
                ctk_comp = ctk.CTkImage(light_image=resized_comp, dark_image=resized_comp, size=resized_comp.size)
                self.lbl_comp_img.configure(image=ctk_comp, text="")

    def save_image(self):
        if not self.compressed_image_data:
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            title="Save compressed image",
            filetypes=[("JPEG Files", "*.jpg;*.jpeg"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.compressed_image_data.save(filename)
                messagebox.showinfo("Success", f"Image saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

if __name__ == "__main__":
    app = ImageCompressionApp()
    app.mainloop()
