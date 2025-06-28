import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import random

class SimpleEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Pixel Manipulation Program")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.image = None
        self.processed_image = None
        self.photo = None

        self.create_widgets()

    def create_widgets(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        btn_load = tk.Button(frame_top, text="Load Image", command=self.load_image)
        btn_load.pack(side=tk.LEFT, padx=5)

        self.operation_var = tk.StringVar(value="swap")
        op_swap = tk.Radiobutton(frame_top, text="Swap Pixels", variable=self.operation_var, value="swap")
        op_invert = tk.Radiobutton(frame_top, text="Invert Colors", variable=self.operation_var, value="invert")
        op_brightness = tk.Radiobutton(frame_top, text="Increase Brightness", variable=self.operation_var, value="brightness")

        op_swap.pack(side=tk.LEFT, padx=5)
        op_invert.pack(side=tk.LEFT, padx=5)
        op_brightness.pack(side=tk.LEFT, padx=5)

        btn_apply = tk.Button(frame_top, text="Apply Operation", command=self.apply_operation)
        btn_apply.pack(side=tk.LEFT, padx=5)

        btn_save = tk.Button(frame_top, text="Save Image", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5)

        # Canvas to display image
        self.canvas = tk.Canvas(self.root, width=760, height=480, bg="#ddd")
        self.canvas.pack(pady=10)

    def load_image(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        filepath = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
        if not filepath:
            return
        try:
            self.image = Image.open(filepath).convert("RGB")
            self.processed_image = self.image.copy()
            self.show_image(self.processed_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image:\n{e}")

    def show_image(self, img):
        # Resize image to fit canvas if needed
        w, h = img.size
        max_w, max_h = 760, 480
        scale = min(max_w/w, max_h/h, 1)
        new_w, new_h = int(w*scale), int(h*scale)
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.canvas.create_image(max_w//2, max_h//2, image=self.photo, anchor=tk.CENTER)

    def apply_operation(self):
        if self.processed_image is None:
            messagebox.showwarning("No image", "Please load an image first.")
            return

        operation = self.operation_var.get()
        img = self.processed_image.copy()
        pixels = img.load()
        w, h = img.size

        if operation == "swap":
            # Swap random pixels pairs in the image (1000 swaps)
            num_swaps = 1000
            for _ in range(num_swaps):
                x1 = random.randint(0, w-1)
                y1 = random.randint(0, h-1)
                x2 = random.randint(0, w-1)
                y2 = random.randint(0, h-1)
                pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

        elif operation == "invert":
            # Invert colors (mathematical operation)
            img = ImageOps.invert(img)

        elif operation == "brightness":
            # Increase brightness by simple add to each channel (clamp at 255)
            factor = 50  # brightness increment
            for x in range(w):
                for y in range(h):
                    r, g, b = pixels[x, y]
                    r = min(255, r + factor)
                    g = min(255, g + factor)
                    b = min(255, b + factor)
                    pixels[x, y] = (r, g, b)

        else:
            messagebox.showerror("Unknown operation", f"Operation '{operation}' is not supported.")
            return

        self.processed_image = img
        self.show_image(self.processed_image)

    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("No image", "No processed image to save.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Image", "*.png"),
                                                           ("JPEG Image", "*.jpg;*.jpeg"),
                                                           ("BMP Image", "*.bmp")],
                                                title="Save Image As")
        if not filepath:
            return
        try:
            self.processed_image.save(filepath)
            messagebox.showinfo("Saved", f"Image saved successfully:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleEncryptionTool(root)
    root.mainloop()

