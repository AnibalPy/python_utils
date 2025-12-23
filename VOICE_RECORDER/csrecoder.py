from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import sounddevice as sound #pip install sounddevice
from scipy.io.wavfile import write # pip install scipy
import time
import wavio as wv # pip install wavio

root = Tk()
root.geometry("600x700+400+80")
root.resizable(False, False)
root.title("Voice Recorder Aníbal Ruiz")
root.configure(background="#01101F")


def record_audio():
    frequency = 44100
    dur=int(duration.get())
    recording = sound.rec(dur * frequency, samplerate=frequency, channels=2)

    #timer
    try:
        temp=int(duration.get())
    except:
        print("Por favor ingrese la duración en segundos (número entero).")
        
    while temp>0:
        root.update()
        time.sleep(1)
        temp-= 1
        if (temp == 0): 
            messagebox.showinfo("Time Countdown", "Time's up")
            Label(text=f"{str(temp)}", font=("Arial", 30), width=4, background="#01101F").place(x=240, y=590)
            

    

    sound.wait()
    write("recording.wav", frequency, recording)
   # messagebox.showinfo("Información", "Grabación finalizada y guardada como 'recording.wav'")  
# contaodor inverso
def countdown(temp):
    if temp > 0:
        counter_label.config(text=str(temp))
        label_recording .config(text="Grabando ...")
        root.after(1000, countdown, temp-1)
    else:
        counter_label.config(text="0")
        messagebox.showinfo("Time Countdown", "Time's up")



#icon
image_icon=PhotoImage(file="./img/microphone_446282.png")
root.iconphoto(False, image_icon)

#logo
# Cargar y redimensionar la imagen
img = Image.open("./img/record.png")
img = img.resize((150, 150))  # Cambia (50, 50) al tamaño que quieras
photo = ImageTk.PhotoImage(img)

# Usar en un Label, Button, etc.
label = tk.Label(root, image=photo, bg="#01101F")
label.pack(padx=20, pady=100)
label.pack()

#name
label = tk.Label(root, text="Voice Recorder", font=("Arial", 30, "bold"), bg="#01101F", fg="white").pack()

#entry box
duration = StringVar()
entry = Entry(root, textvariable=duration, font=("Arial", 30), width=15).pack(pady=10)
#entry.pack(pady=10)
Label(text="Enter duration in seconds", font=("Arial", 15), bg="#01101F", fg="white", justify="center").pack()

#button
record=Button(root, text="Record", font=("Arial", 20), bg="#E94E1B", fg="white", border=0,command=record_audio) 
record.pack(pady=20) 

#label grabando
label_recording = tk.Label(root, text="", font=("Arial", 20), bg="#01101F", fg="white")
label_recording.place(x=220, y=520)
#timer label
counter_label = tk.Label(root, text="", font=("Arial", 30), bg="#01101F", fg="white")
counter_label.place(x=240, y=590)



root.mainloop()