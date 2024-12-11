import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from fpdf import FPDF
import os
from PIL import Image, ImageTk
import serial  # Library for serial communication
import threading  # For handling serial reading in the background

# Configure the serial port (Adjust the port and baud rate as needed)
SERIAL_PORT = "COM3"  # Replace with the actual COM port used
BAUD_RATE = 9600
serial_connection = None

# Velocity reading thread function
def read_velocity_from_serial():
    global serial_connection
    try:
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            # if serial_connection.in_waiting > 0:
            data = serial_connection.readline().decode('utf-8').strip()
            try:
                velocity = float(data)
                root.after(0, update_velocity_display, velocity)
            except ValueError:
                messagebox.showerror("Error", "Invalid data received!")
                # pass  # Ignore invalid data
    except Exception as e:
        print(f"Error in serial communication: {e}")
    finally:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()

# Function to update velocity display and save to the table
def update_velocity_display(velocity):
    muzzle_velocity_var.set(f"{velocity} m/s")
    velocity_table.append(velocity)
    rd_number_var.set(len(velocity_table))
# Function to manually enter velocity
def manual_entry():
    try:
        velocity = float(manual_velocity_entry.get())
        muzzle_velocity_var.set(f"{velocity} m/s")
        velocity_table.append(velocity)
        rd_number_var.set(len(velocity_table))
    except ValueError:
        messagebox.showerror("Error", "Invalid velocity entered. Please enter a valid number.")

def restart_firing():
    global velocity_table
    velocity_table = []  # Clear the velocity data
    rd_number_var.set(1)  # Reset the round number to 1
    messagebox.showinfo("Info", "Firing restarted. Velocity values cleared.")

def print_results():
    if not velocity_table:
        messagebox.showwarning("Warning", "No velocity data available!")
        return

    # Gather input details
    amk_no = amk_no_entry.get()
    nomenclature = nomenclature_entry.get()
    weapon = weapon_entry.get()
    lot_no = lot_no_entry.get()
    vintage = vintage_entry.get()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    directory = r"C:\Users\prave\OneDrive\Desktop\Muzzle Velocity Results"

    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"Muzzle_Velocity_Results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Draw Logos
    pdf.image(r"C:\Users\prave\OneDrive\Desktop\Ord Logo.png", x=10, y=10, w=20)  # Top left
    pdf.image(r"C:\Users\prave\OneDrive\Desktop\cmm logo.png", x=170, y=10, w=20)  # Top right
    pdf.image(r"C:\Users\prave\OneDrive\Desktop\Picture5.png", x=30, y=10, w=138)   # Top center

    # Add spacing below logos
    pdf.set_y(50)  # Move the cursor down to ensure space below the logos

    # Header with a box
    pdf.set_font("Arial", size=14, style="B")
    pdf.set_fill_color(220, 220, 220)  # Light gray for the background of the header box
    pdf.rect(10, pdf.get_y(), 190, 10)  # Draw a rectangle
    pdf.cell(0, 10, "Muzzle Velocity Results", ln=True, align="C", fill=True)

    pdf.ln(10)  # Add spacing

    # Add details
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Date and Time of Firing: {timestamp}", ln=True)
    pdf.cell(0, 10, f"AMK No: {amk_no}", ln=True)
    pdf.cell(0, 10, f"Nomenclature: {nomenclature}", ln=True)
    pdf.cell(0, 10, f"Weapon Used: {weapon}", ln=True)
    pdf.cell(0, 10, f"Lot No: {lot_no}", ln=True)
    pdf.cell(0, 10, f"Vintage: {vintage}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(40, 10, "Rd No", border=1, align="C")
    pdf.cell(60, 10, "Velocity (m/s)", border=1, align="C")
    pdf.cell(80, 10, "Standard Parameter (900+/-50 m/s)", border=1, align="C")
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", size=12)
    for rd_no, velocity in enumerate(velocity_table, 1):
        pdf.cell(40, 10, str(rd_no), border=1, align="C")
        pdf.cell(60, 10, f"{velocity}", border=1, align="C")
        pdf.cell(80, 10, "900+/-50", border=1, align="C")
        pdf.ln()

    # Result Summary
    pdf.ln(10)
    if all(v > 900 for v in velocity_table):
        pdf.set_fill_color(0, 255, 0)  # Green
        pdf.set_text_color(255, 255, 255)  # White
        pdf.cell(0, 10, "PASS", align="C", ln=True, fill=True)
    else:
        pdf.set_fill_color(255, 0, 0)  # Red
        pdf.set_text_color(255, 255, 255)  # White
        pdf.cell(0, 10, "FAIL", align="C", ln=True, fill=True)

    # Add "Tested By" at bottom right
    pdf.set_text_color(0, 0, 0)  # Reset text color to black
    pdf.set_font("Arial", size=12)
    pdf.set_y(-30)  # Move to bottom
    pdf.cell(0, 10, "Tested By: ________", align="R")

    # Save PDF
    pdf.output(file_path)
    messagebox.showinfo("Success", f"Results saved to: {file_path}")

# Initialize GUI application
root = tk.Tk()
root.title("Muzzle Velocity Chronometer")
root.state("zoomed")  # Start in maximized mode

# Apply a colorful theme
root.configure(bg="#f0f8ff")  # Light blue background
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f0f8ff")  # Frame background
style.configure("TLabel", font=("Arial", 12), background="#f0f8ff", foreground="#333333")
style.configure("TButton", font=("Arial", 14, "bold"), foreground="white", background="#4682b4")
style.map("TButton", background=[("active", "#5a9bd4")])  # Hover effect

# Main container
main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=1, column=0, sticky="nsew")
main_frame.grid_rowconfigure(0, weight=2)  # Details frame gets 2x space
main_frame.grid_rowconfigure(1, weight=1)  # Velocity frame gets 1x space
main_frame.grid_rowconfigure(2, weight=1)  # Manual entry gets 1x space
main_frame.grid_rowconfigure(3, weight=1)  # Button frame gets 1x space
main_frame.grid_columnconfigure(0, weight=1)

# Load the logos using Pillow
logo_1 = Image.open("C:/Users/prave/OneDrive/Desktop/Ord Logo.png")  # Left logo
logo_1 = logo_1.resize((100, 100))  # Resize the logo
logo_1_tk = ImageTk.PhotoImage(logo_1)

logo_2 = Image.open("C:/Users/prave/OneDrive/Desktop/cmm logo.png")  # Right logo
logo_2 = logo_2.resize((100, 100))  # Resize the logo
logo_2_tk = ImageTk.PhotoImage(logo_2)

# Load the middle image (SHASTRA)
shastra_logo = Image.open(r"C:\Users\prave\OneDrive\Desktop\Picture5.png")  # Middle image
shastra_logo = shastra_logo.resize((950, 110))  # Resize the image
shastra_logo_tk = ImageTk.PhotoImage(shastra_logo)

# Logo Frame (Top row)
logo_frame = ttk.Frame(root)
logo_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Configure the grid to make the logo frame span the entire window width
logo_frame.grid_columnconfigure(0, weight=0)  # Left logo can take any extra space
logo_frame.grid_columnconfigure(1, weight=1)  # Middle image stays fixed size
logo_frame.grid_columnconfigure(2, weight=0)  # Right logo stays fixed size

# Left logo (Ord Logo)
left_logo_label = ttk.Label(logo_frame, image=logo_1_tk)
left_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Middle image (SHASTRA)
shastra_logo_label = ttk.Label(logo_frame, image=shastra_logo_tk)
shastra_logo_label.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Right logo (CMM Logo) - Place it at the extreme right of the screen
right_logo_label = ttk.Label(logo_frame, image=logo_2_tk)
right_logo_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

# Variables
muzzle_velocity_var = tk.StringVar(value="Waiting for data...")
rd_number_var = tk.IntVar(value=1)
velocity_table = []

# Input fields
frame = ttk.LabelFrame(main_frame, text="Input Amn Details", padding=10)
frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
frame.grid_columnconfigure(1, weight=1)

ttk.Label(frame, text="AMK No:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
amk_no_entry = ttk.Entry(frame, font=("Arial", 10))
amk_no_entry.grid(row=0, column=1, sticky="ew")

ttk.Label(frame, text="Nomenclature:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
nomenclature_entry = ttk.Entry(frame, font=("Arial", 10))
nomenclature_entry.grid(row=1, column=1, sticky="ew")

ttk.Label(frame, text="Weapon Used:", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
weapon_entry = ttk.Entry(frame, font=("Arial", 10))
weapon_entry.grid(row=2, column=1, sticky="ew")

ttk.Label(frame, text="Lot No:", font=("Arial", 10)).grid(row=3, column=0, sticky="w")
lot_no_entry = ttk.Entry(frame, font=("Arial", 10))
lot_no_entry.grid(row=3, column=1, sticky="ew")

ttk.Label(frame, text="Vintage:", font=("Arial", 10)).grid(row=4, column=0, sticky="w")
vintage_entry = ttk.Entry(frame, font=("Arial", 10))
vintage_entry.grid(row=4, column=1, sticky="ew")

# Velocity display
velocity_frame = ttk.Frame(main_frame, padding=10)
velocity_frame.grid(row=1, column=0, pady=10, sticky="nsew")

ttk.Label(velocity_frame, text="Muzzle Velocity:", font=("Helvetica", 16)).pack(anchor="center")
ttk.Label(velocity_frame, textvariable=muzzle_velocity_var, font=("Helvetica", 36, "bold")).pack(anchor="center")

# Manual velocity entry
manual_entry_frame = ttk.LabelFrame(main_frame, text="Manual Entry", padding=10)
manual_entry_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(manual_entry_frame, text="Enter velocity (m/s):", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
manual_velocity_entry = ttk.Entry(manual_entry_frame, font=("Arial", 12))
manual_velocity_entry.grid(row=0, column=1, sticky="ew")

manual_velocity_button = ttk.Button(manual_entry_frame, text="Enter", command=manual_entry, style="TButton")
manual_velocity_button.grid(row=1, column=0, columnspan=2, pady=10)

# Action Buttons (Print & Save)
action_buttons_frame = ttk.Frame(main_frame)
action_buttons_frame.grid(row=3, column=0, pady=5, sticky="ew")

# Print Results button
print_button = ttk.Button(action_buttons_frame, text="Print Results", command=print_results)
print_button.pack(side="left", padx=30)

# Restart Firing button
restart_button = ttk.Button(action_buttons_frame, text="Restart Firing", command=restart_firing)
restart_button.pack(side="left", padx=30)

# Apply a larger font to the button
print_button.config(style="Large.TButton")
restart_button.config(style="Large.TButton")



# "Developed by AMM-53" in a text box at the bottom right
developer_frame = ttk.Frame(root, padding=10)
developer_frame.grid(row=1, column=0, sticky="se", padx=20, pady=20)

developer_entry = ttk.Entry(developer_frame, font=("Arial", 12), width=30, justify="center")
developer_entry.insert(0, "Developed by: Tech Team AMM-53")
developer_entry.config(state="readonly")
developer_entry.grid(row=3, column=2)

# Start the serial reading thread
serial_thread = threading.Thread(target=read_velocity_from_serial, daemon=True)
serial_thread.start()


root.mainloop()