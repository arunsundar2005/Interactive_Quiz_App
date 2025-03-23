import tkinter as tk
from ttkbootstrap import Style
import random
import pyttsx3
import speech_recognition as sr
import threading
import pygame
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.style = Style(theme='superhero')
        master.title("🎉 AI Quiz Game 🎉")
        master.geometry("700x600")
        master.resizable(False, False)

        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Use Microsoft Zira
        self.engine.setProperty('rate', 160)  
        self.engine.setProperty('volume', 0.9)

        pygame.mixer.init()
        self.dice_sound = pygame.mixer.Sound("picker_wheel.wav")

        self.questions = [
            # {"question": "Which robot is shown in the image?", "options": ["Atlas", "Spot", "Asimo", "Optimus"], "answer": "Atlas", "image": "images/atlas.jpg"},
            {"question": "Which AI defeated world champion Go player Lee Sedol?", "options": ["DeepBlue", "DeepSeek", "Watson", "AlphaGo"], "answer": "AlphaGo", "image": None}
        ]

        self.available_roll_numbers = list(range(33, 92))

        self.roll_label = tk.Label(master, text="", font=("Arial Black", 22), fg="yellow", bg="#1c1c1c")
        self.roll_label.place(relx=0.5, y=20, anchor='n')
        self.roll_label.place_forget()

        self.timer_label = tk.Label(master, text="", font=("Arial Black", 20), fg="#ff3333", bg="#1c1c1c")
        self.timer_label.place(relx=0.9, y=20, anchor='ne')
        self.timer_label.place_forget()

        self.question_label = tk.Label(master, text="", wraplength=650, font=("Arial", 16), fg="white", bg="#1c1c1c", justify="center")
        self.question_label.place(relx=0.5, rely=0.25, anchor='center')
        self.question_label.place_forget()

        self.var = tk.StringVar()
        self.options = []
        for i in range(4):
            opt = tk.Radiobutton(master, text="", variable=self.var, value="", font=("Arial", 14), fg="white", bg="#1c1c1c", 
                                 selectcolor="#444444", anchor="w", padx=10, width=40, indicatoron=0, relief="ridge")
            opt.place(relx=0.5, rely=0.35 + i * 0.08, anchor='center')
            opt.place_forget()
            self.options.append(opt)

        self.feedback_label = tk.Label(master, text="", font=("Arial Black", 16), fg="cyan", bg="#1c1c1c")
        self.feedback_label.place(relx=0.5, rely=0.85, anchor='center')
        self.feedback_label.place_forget()

        self.answer_button = tk.Button(master, text="✔ Lock Answer", font=("Arial Black", 14), command=lambda: self.listen_for_voice_command("lock"), bg="#009933", fg="white", relief="groove", padx=20, pady=10)
        self.answer_button.place(relx=0.5, rely=0.7, anchor='center')
        self.answer_button.place_forget()

        self.image_label = tk.Label(master, bg="#1c1c1c")
        self.image_label.place(relx=0.5, rely=0.55, anchor='center')
        self.image_label.place_forget()

        self.start_button = tk.Button(master, text="🎲 Start Quiz", font=("Arial Black", 14), command=lambda: self.listen_for_voice_command("start"), bg="#3366cc", fg="white", relief="groove", padx=20, pady=10)
        self.start_button.place(relx=0.5, rely=0.95, anchor='center')

        self.q_index = -1
        self.roll_number = None
        self.time_left = 30
        self.timer_running = False

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_voice_command(self, mode):
        def voice_thread():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.speak(f"Listening for {'start command' if mode == 'start' else 'lock command'}...")
                print("🎤 Listening...")  
                try:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()
                    print(f"🔊 Heard: {command}")  

                    if mode == "start" and "quiz" and "agent" in command:
                        self.speak("Starting the quiz!")
                        self.start_quiz()
                    elif mode == "lock" and "option" and "agent" in command:
                        self.speak("Answer locked!")
                        self.check_answer()
                    else:
                        self.speak("Invalid command. Please try again.")

                except sr.UnknownValueError:
                    self.speak("Could not understand. Try again.")
                except sr.RequestError:
                    self.speak("Speech service error.")
                except sr.WaitTimeoutError:
                    self.speak("No command detected. Try again.")

        threading.Thread(target=voice_thread, daemon=True).start()

    def start_quiz(self):
        self.start_button.place_forget()
        self.next_question()

    def suspense_roll_picker(self, steps=20, delay=100):
        if steps == 20:
            self.dice_sound.play(-1)

        if steps > 0:
            roll_number = random.choice(self.available_roll_numbers)
            self.roll_label.config(text=f"🎲 Rolling: {roll_number}")
            self.master.after(delay, lambda: self.suspense_roll_picker(steps - 1, delay + 30))
        else:
            self.dice_sound.stop()
            self.roll_number = random.choice(self.available_roll_numbers)
            self.available_roll_numbers.remove(self.roll_number)
            self.roll_label.config(text=f"🎉 Roll Number Selected: {self.roll_number}")
            self.speak(f"Selected roll number is {self.roll_number}")
            self.master.after(5000, self.ask_question)

    def next_question(self):
        if not self.available_roll_numbers:
            self.end_quiz()
            return
        self.q_index += 1
        if self.q_index < len(self.questions):
            self.suspense_roll_picker()
        else:
            self.end_quiz()

    def ask_question(self):
        q = self.questions[self.q_index]
        self.question_label.config(text=q["question"])
        self.question_label.place(relx=0.5, rely=0.25, anchor='center')

        for idx, opt in enumerate(q["options"]):
            self.options[idx].config(text=opt, value=opt, state=tk.NORMAL)
            self.options[idx].place(relx=0.5, rely=0.35 + idx * 0.08, anchor='center')

        if q.get("image"):
            image = Image.open(q["image"]).resize((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.image_label.place(relx=0.5, rely=0.55, anchor='center')
        else:
            self.image_label.place_forget()

        self.answer_button.place(relx=0.5, rely=0.7, anchor='center')

root = tk.Tk()
app = QuizApp(root)
root.mainloop()
