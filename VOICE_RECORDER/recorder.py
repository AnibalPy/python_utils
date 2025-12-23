
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sounddevice as sound #pip install sounddevice
from scipy.io.wavfile import write # pip install scipy
import time
import wavio as wv # pip install wavio

root = tk.Tk()
root.geometry("600x700+400+80")
root.resizable(False, False)
root.title("Voice Recorder Aníbal Ruiz")
root.configure(bg="#01101F")
import os
import getpass

# obtener el nombre de usuario actual
current_user = getpass.getuser()
#messagebox.showinfo("Usuario Actual", f"El usuario actual es: {current_user}")  





def record_audio():
    frequency = 44100
    try:
        dur = int(duration.get())
        if dur <= 0:
            raise ValueError("Duration must be greater than 0")
    except Exception:
        messagebox.showerror("Error", "Por favor ingrese una duración válida en segundos (número entero mayor que 0).")
        duration.set("")
        return

    record.configure(bg="#F52809")  # Cambia a rojo al grabar
    label_recording.configure(text="Recording...")
    root.update()

    global recording
    recording = sound.rec(dur * frequency, samplerate=frequency, channels=2)
    start_countdown(dur)

def start_countdown(temp):
    counter_label.configure(text=str(temp))
    
    countdown(temp-1)

# contaodor inverso
def countdown(temp):
    if temp > 0:
        root.after(1000, countdown, temp-1)
        counter_label.configure(text=str(temp))
        label_recording.configure(text="Recording...")

        
        
    else:
        counter_label.configure(text="0")
        sound.wait()  # Espera a que termine la grabación
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_path, "recording.wav")
        #write("recording.wav", 44100, recording)  # Guarda el archivo
        write(file_path, 44100, recording)

        
        messagebox.showinfo("Time Countdown", "Time's up")
        counter_label.configure(text="")  # Esto limpia el contador
        label_recording.configure(text="Recording finished")
        label_recording.configure(text="")
        record.configure(bg="#1B55E9")
        duration.set("")
         



#icon
image_icon = tk.PhotoImage(file="./img/microphone_446282.png")
root.iconphoto(False, image_icon)


#logo
img = Image.open("./img/record.png")
img = img.resize((150, 150))
photo = ImageTk.PhotoImage(img)
label_img = tk.Label(root, image=photo, bg="#01101F", borderwidth=0, highlightthickness=0)
label_img.pack(padx=20, pady=100)

#name
label_title = tk.Label(root, text="Voice Recorder", font=("Arial", 30, "bold"), bg="#01101F", fg="white", borderwidth=0, highlightthickness=0)
label_title.pack()

#entry box
duration = tk.StringVar()
entry = tk.Entry(root, textvariable=duration, font=("Arial", 20), width=15)
entry.pack(pady=10)
label_duration = tk.Label(root, text="Enter duration in seconds", font=("Arial", 15), bg="#01101F", fg="white", justify="center", borderwidth=0, highlightthickness=0)
label_duration.pack()

#button
record = tk.Button(root, text="Record", font=("Arial", 20), bg="#1B55E9", fg="white", borderwidth=0, command=record_audio)
record.pack(pady=20)



#timer label
counter_label = tk.Label(root, text="", font=("Arial", 20), bg="#01101F", fg="white", borderwidth=0, highlightthickness=0)
counter_label.place(x=270, y=620)

#label grabando
label_recording = tk.Label(root, text="", font=("Arial", 20), bg="#01101F", fg="white", borderwidth=0, highlightthickness=0)
label_recording.place(x=230, y=580)



root.mainloop()
