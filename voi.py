import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import urllib.parse
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import subprocess

# Tentukan path lengkap ke Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Fungsi untuk membuka file OpenCV.py ketika perintah diterima
def buka_kamera():
    speak("Baik, saya membuka kamera")
    subprocess.run(["python", r"C:\Users\carer\Downloads\OpenCV\OpenCV.py"])
    

# Buat folder rekaman jika belum ada
folder_rekaman = "rekaman"
if not os.path.exists(folder_rekaman):
    os.makedirs(folder_rekaman)

# Inisialisasi mesin suara
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Kecepatan suara
voices = engine.getProperty('voices')

# Cari suara bahasa Indonesia (jika tersedia)
for voice in voices:
    if "indonesian" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    """Fungsi untuk mengucapkan teks"""
    engine.say(text)
    engine.runAndWait()

# Fungsi untuk merekam suara dan menyimpannya ke file
def record_audio(audio_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(folder_rekaman, f"rekaman_{timestamp}.wav")
    with open(file_path, "wb") as f:
        f.write(audio_data.get_wav_data())
    speak(f"Rekaman telah disimpan sebagai {file_path}")

# Fungsi untuk mendengarkan perintah suara
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Mendengarkan...")
        update_button_state(True)
        root.update()
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            record_audio(audio)  # Simpan rekaman suara
            command = recognizer.recognize_google(audio, language="id-ID")
            status_label.config(text=f"Anda mengatakan: {command}")
            root.update()
            return command.lower()
        except sr.UnknownValueError:
            status_label.config(text="Maaf, saya tidak menangkap ucapan Anda.")
            speak("Maaf, saya tidak menangkap ucapan Anda.")
        except sr.RequestError:
            status_label.config(text="Maaf, terjadi masalah dengan layanan suara.")
            speak("Maaf, terjadi masalah dengan layanan suara.")
    return ""

# Fungsi untuk menangani perintah suara
def start_listening():
    global listening
    if listening:
        stop_listening()
    else:
        listening = True
        command = listen()
        execute_command(command)
        update_button_state(False)

# Fungsi untuk menutup voice dan kembali ke buka voice
def stop_listening():
    global listening
    listening = False
    status_label.config(text="Tekan tombol untuk berbicara")
    update_button_state(False)

# Fungsi untuk mengeksekusi perintah suara
def execute_command(command):
    if "buka youtube" in command:
        speak("Baik, saya membuka YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "tutup youtube" in command:
        speak("Baik, saya menutup YouTube.")
        os.system("taskkill /IM chrome.exe /F")
    elif "buka chatgpt" in command:
        speak("Baik, saya membuka ChatGPT.")
        webbrowser.open("https://chat.openai.com/")
    elif "buka facebook" in command:
        speak("Baik, saya membuka Facebook.")
        webbrowser.open("https://www.facebook.com/")
    elif "buka google" in command:
        speak("Baik, saya membuka Google.")
        webbrowser.open("https://www.google.com")
    elif "tutup google" in command:
        speak("Baik, saya menutup Google.")
        os.system("taskkill /IM chrome.exe /F") 
            
    elif "buka chess" in command:
        speak("Baik, saya membuka Chess")
        subprocess.run([chrome_path, "https://www.chess.com/play"]) 
        
        
    elif "buka kamera" in command:
            buka_kamera()  # Menjalankan file OpenCV.py
            
    elif "buka ph" in command:
        speak("Baik, saya membuka YouTube")
        subprocess.run([chrome_path, "https://www.pornhub.com/"])
        
    elif "buka film" in command:
        speak("Baik, saya membuka film")
        subprocess.run([chrome_path, "https://tv5.lk21official.pics/grotesque-2009/"])
        
    elif "tutup chess" in command:
        speak("Baik, saya menutup Chess.com di Google Chrome.")
        os.system("taskkill /IM chrome.exe /F")   
    elif "siapa kamu" in command:
        speak("Halo! Saya Hei, asisten virtual Anda. Saya siap membantu!")
    elif "matikan" in command:
        speak("Baik, saya akan berhenti. Sampai jumpa!")
        root.destroy()
    else:
        speak("Maaf, saya tidak mengenali perintah tersebut.")
    stop_listening()

# Fungsi untuk mengubah ikon tombol
def update_button_state(listening):
    if listening:
        listen_button.config(text=" Tutup Voice", image=close_icon, compound="left")
    else:
        listen_button.config(text=" Buka Voice", image=mic_icon, compound="left")

# GUI menggunakan Tkinter
root = tk.Tk()
root.title("Perintah Suara - Hei")
root.geometry("350x250")

listening = False  # Status mendengarkan

# Memuat ikon mikrofon
mic_icon = Image.open("mic_icon.png").resize((30, 30), Image.LANCZOS)
mic_icon = ImageTk.PhotoImage(mic_icon)

# Memuat ikon tutup suara
close_icon = Image.open("close_icon.png").resize((30, 30), Image.LANCZOS)
close_icon = ImageTk.PhotoImage(close_icon)

# Label status
status_label = tk.Label(root, text="Tekan tombol untuk berbicara", font=("Arial", 12))
status_label.pack(pady=10)

# Tombol kontrol voice
listen_button = ttk.Button(root, text=" Buka Voice", image=mic_icon, compound="left", command=start_listening)
listen_button.pack(ipadx=10, ipady=5, pady=10)

root.mainloop()
