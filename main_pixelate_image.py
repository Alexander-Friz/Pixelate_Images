import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def pixelate_image(input_path, pixel_size):

    try:
        # Bild öffnen
        original_image = Image.open(input_path)
        original_size = original_image.size

        # Bild skalieren (verkleinern)
        small_image = original_image.resize(
            (original_size[0] // pixel_size, original_size[1] // pixel_size),
            Image.NEAREST
        )

        # Bild wieder auf Originalgröße skalieren (vergrößern)
        pixelated_image = small_image.resize(
            original_size,
            Image.NEAREST
        )

        return pixelated_image
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Verarbeiten des Bildes: {e}")
        return None

def open_image():
    """Öffnet den Dateidialog, um ein Bild auszuwählen."""
    global input_path, img_label
    input_path = filedialog.askopenfilename(filetypes=[("Bilder", "*.png;*.jpg;*.jpeg")])
    if input_path:
        img = Image.open(input_path)
        img.thumbnail((300, 300))  # Vorschaugröße
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img
        messagebox.showinfo("Bild geladen", "Bild erfolgreich geladen!")

def save_image(pixelated_image):
    """Speichert das pixelierte Bild."""
    if pixelated_image:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Dateien", "*.png")])
        if output_path:
            pixelated_image.save(output_path)
            messagebox.showinfo("Gespeichert", f"Pixelbild gespeichert unter: {output_path}")

def process_image():
    """Verarbeitet das Bild und zeigt das Ergebnis an."""
    global input_path, pixelated_image
    if not input_path:
        messagebox.showerror("Fehler", "Bitte zuerst ein Bild laden!")
        return

    try:
        pixel_size = int(pixel_size_entry.get())
        if pixel_size <= 0:
            raise ValueError("Pixelgröße muss größer als 0 sein!")
        pixelated_image = pixelate_image(input_path, pixel_size)

        if pixelated_image:
            img = pixelated_image.copy()
            img.thumbnail((300, 300))  # Vorschaugröße
            img = ImageTk.PhotoImage(img)
            img_label.config(image=img)
            img_label.image = img
            messagebox.showinfo("Erfolg", "Bild erfolgreich verarbeitet!")
    except ValueError as e:
        messagebox.showerror("Fehler", f"Ungültige Pixelgröße: {e}")

# GUI
root = tk.Tk()
root.title("Pixel Bild Ersteller")
root.geometry("400x500")

# Variablen
input_path = None
pixelated_image = None

# GUI-Komponenten
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Bild laden", command=open_image).grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="Pixelgröße:").grid(row=1, column=0, padx=5, pady=5)
pixel_size_entry = tk.Entry(frame, width=10)
pixel_size_entry.grid(row=1, column=1, padx=5, pady=5)
pixel_size_entry.insert(0, "10")

tk.Button(frame, text="Verarbeiten", command=process_image).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Speichern", command=lambda: save_image(pixelated_image)).grid(row=3, column=0, columnspan=2, pady=10)

img_label = tk.Label(root)
img_label.pack(pady=10)

#Anwendung starten
root.mainloop()
