#----------------------
# Nydia Almudena Rojas Pompa
# Greenie - ESG Assistant / CODE IN PLACE 2026
# :)

from tkinter import *
from PIL import Image, ImageTk
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- Funciones al nivel raíz ---

def load_image(image_file, size=(150, 150)):
    if PIL_AVAILABLE:
        image = Image.open(image_file)
        image = image.resize(size, Image.LANCZOS)
        if image.mode in ("RGBA", "P"):
            background = Image.new("RGB", image.size, (240, 240, 240))
            background.paste(image, mask=image.split()[3] if image.mode == "RGBA" else None)
            image = background
        return ImageTk.PhotoImage(image)
    return PhotoImage(file=image_file)

def calculate_risk(electricity, transport, waste):
    total_co2 = (electricity * 0.45) + (transport * 0.21) + (waste * 1.5)
    if total_co2 <= 100:
        return total_co2, "LOW", "greenie_stars.png", "AMAZING JOB! Your impact is low, keep up the good work!"
    elif total_co2 <= 300:
        return total_co2, "MEDIUM", "greenie_ush.png", "Your impact is medium, consider implementing more sustainable practices."
    else:
        return total_co2, "HIGH", "greenie_sad.png", " Your impact is high, it's crucial to take immediate action!!!!!!!!!!"

def show_intro(intro_text):
    intro_text.config(
        text=(" Welcome to Greenie a mini ESG Assistant \n\n"
              "This project helps companies estimate their environmental impact.\n"
              "Greenie analyzes electricity use, transport, and waste production \n\n"
              "After entering your data, Greenie will calculate a risk level \n"
              "and change its mood depending on your results")
    )

def analyze():
    try:
        electricity = float(electricity_entry.get())
        transport = float(transport_entry.get())
        waste = float(waste_entry.get())
    except ValueError:
        result_label.config(text="Please enter valid numeric values.")
        return

    co2, risk, image_file, message = calculate_risk(electricity, transport, waste)

    # ← Aquí cambia la imagen según el resultado
    try:
        new_photo = load_image(image_file, size=(150, 150))
        mascot.config(image=new_photo)
        mascot.image = new_photo  # Guarda referencia para que no se borre
    except Exception as e:
        print(f"Error cargando imagen: {e}")

    result_label.config(
        text=(f"Estimated Carbon Footprint: {round(co2, 2)} kg CO2/month \n"
              f"Risk Level: {risk} \n\n"
              f"Greenie says: {message}")
    )

# --- Ventana PRIMERO ---
window = Tk()
window.title("Greenie - ESG Assistant")
window.geometry("500x700")

title = Label(window, text="Greenie - Your ESG Assistant", font=("Arial", 22, "bold"))
title.pack(pady=10)

intro_text = Label(window, text="", font=("Arial", 11), wraplength=480, justify="center")
intro_text.pack(pady=10)
show_intro(intro_text)

try:
    photo = load_image("greenie_og.png", size=(150, 150))
except Exception as e:
    print(f"Error cargando greenie_og: {e}")
    photo = None

mascot = Label(window, image=photo)
mascot.image = photo
mascot.pack(pady=10)

Label(window, text="Electricity Use (kWh/month):").pack()
electricity_entry = Entry(window)
electricity_entry.pack()

Label(window, text="Transport (km/month):").pack()
transport_entry = Entry(window)
transport_entry.pack()

Label(window, text="Waste Production (kg/month):").pack()
waste_entry = Entry(window)
waste_entry.pack()

Button(window, text="Analyze ESG impact", command=analyze).pack(pady=20)

result_label = Label(window,
    text="Enter your data and click Analyze to see Greenie's reaction!",
    font=("Arial", 12), wraplength=450, justify="center")
result_label.pack(pady=10)

window.mainloop()
