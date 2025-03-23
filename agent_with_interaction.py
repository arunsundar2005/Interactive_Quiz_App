import tkinter as tk
from ttkbootstrap import Style
import random
import pyttsx3
from tkinter import messagebox
import pygame
import speech_recognition as sr
import threading
from PIL import Image, ImageTk

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.style = Style(theme='superhero')
        master.title("🎉 AI Quiz Game 🎉")
        master.geometry("700x600")
        master.resizable(True, True)

        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Set Microsoft Zira
        self.engine.setProperty('rate', 180)  # Natural speaking speed
        self.engine.setProperty('volume', 0.9) 

        self.image_label = tk.Label(master, bg="#1c1c1c")
        self.image_label.place(relx=0.5, rely=0.55, anchor='center')  # Below question
        self.image_label.place_forget()  # Hide initially

        pygame.mixer.init() 
        self.dice_sound = pygame.mixer.Sound("picker_wheel.wav")
        self.chosen = pygame.mixer.Sound("chosen.wav")

        # Load Questions
        self.questions = [
           
            {
                "question": "What incident does the image remind you in the history of AI?",
                "options": ["DeepBlue", "AlphaGo", "ChatGPT", "Watson"],
                "answer": "DeepBlue",
                "image" : "images\deepBlue.png"
            },
            {
                "question": "The test that determines if a machine can exhibit human-like intelligence is:",
                "options": ["McCarthy Test", "Turing Test", "Allen Test", "Leobner Test"],
                "answer": "Turing Test",
                "image" : None
            },
            {
                "question": "Which AI defeated world champion Go player Lee Sedol?",
                "options": ["DeepBlue", "DeepSeek", "Watson", "AlphaGo"],
                "answer": "AlphaGo",
                "image" : None
            },
            {
                "question": "Which AI agent is shown in the image?",
                "options": ["Spot", "Asimo", "Optimus", "Atlas"],
                "answer": "Asimo",
                "image" : "images\Asimo.png"
            },
            {
                "question": "The AI subfield that deals with computers to see is:",
                "options": ["Computer Vision", "Natural Language Processing", "Deep Learning", "Vision Transformers (ViT)"],
                "answer": "Computer Vision",
                "image" : None
            },
            {
                "question": "Which of the following is an example of unsupervised learning?",
                "options": ["Clustering", "Image classification", "Speech Recognition", "Object Detection"],
                "answer": "Clustering",
                "image" : None
            },
            {
                "question": "Which two AI fields are crucial for making cars work autonomously?",
                "options": ["Datamining & Chatbots", "NLP & Expert Systems", "Computer Vision & Reinforcement Learning", "Speech Recognition & Robotics"],
                "answer": "Computer Vision & Reinforcement Learning",
                "image" : None
            },
            {
                "question": "Which of these movies presents a dystopian view of AI?",
                "options": ["RoboCop", "I, Robot", "Oblivion", "Ex Machina"],
                "answer": "Ex Machina",
                "image" : "images\ex_machina.png"
            },
            {
                "question": "Which robot is represented in the image?",
                "options": ["Ameca", "Apollo", "Atlas", "Alter 3"],
                "answer": "Ameca",
                "image" : "images\Ameca.png"
            },
            {
                "question": "Which of the following applications is most likely to involve NLP?",
                "options": ["Chatbots", "Face Recognition", "Speech Recognition", "Autonomous Driving"],
                "answer": "Chatbots", 
                "image" : None
            },
            {
                "question": "Which concept allows the AI agent to perform the shown task?",
                "options": ["Blockchain", "Fuzzy Logic", "Computer Vision", "Neural Networks"],
                "answer": "Computer Vision",
                "image" : "images\task.png"
            },
            {
                "question": "The AI agent that is trained for only one specific task is:",
                "options": ["Artificial General Intelligence (AGI)", "Artificial Narrow Intelligence (ANI)", "Artificial Super Intelligence (ASI)", "Strong AI"],
                "answer": "Artificial Narrow Intelligence (ANI)",
                "image" : None
            },
            {
                "question": "Which AI system beat humans in the complex strategy game 'StarCraft II'?",
                "options": ["AlphaGo", "DeepBlue", "AlphaStar", "Watson"],
                "answer": "AlphaStar",
                "image" : None
            },
            {
                "question": "Which of the following best represents Isaac Asimov's 'Zeroth Law of Robotics'?",
                "options": [
                    "A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.",
                    "A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
                    "A robot may not harm humanity, or, by inaction, allow humanity to come to harm.",
                    "A robot must obey the orders given by human beings, except where such orders would conflict with the First Law."
                ],
                "answer": "A robot may not harm humanity, or, by inaction, allow humanity to come to harm.", 
                "image" : None
            },
            {
                "question": "What is the name of the recently observed AI-to-AI communication mode where AI agents develop their own language to interact, often incomprehensible to humans?",
                "options": ["Neural Exchange Protocol", "Agent Communication Language", "Machine Dialogue Standards", "The Gibberlink Protocol"],
                "answer": "The Gibberlink Protocol", 
                "image" : None
            }
        
        ]

        self.available_roll_numbers = list(range(33, 92))  # 33 to 91

        # GUI Components
        self.roll_label = tk.Label(master, text="", font=("Arial Black", 22), fg="yellow", bg="#1c1c1c")
        # self.roll_label.pack(pady=15)
        # self.roll_label.pack_forget()
        # self.roll_label.place(relx=0.5, y=20, anchor='n')

        self.question_label = tk.Label(master, text="", wraplength=650, font=("Arial", 16), fg="white", bg="#1c1c1c", justify="center")
        # self.question_label.pack(pady=20)
        # self.question_label.pack_forget()
        # self.question_label.place(relx=0.5, rely=0.3, anchor='center')  # Fixed center

        self.var = tk.StringVar()
        self.options = [tk.Radiobutton(master, text="", variable=self.var, value="", font=("Arial", 14), fg="white", bg="#1c1c1c", selectcolor="#444444", anchor="w", padx=10) for _ in range(4)]
        # for opt in self.options:
        #     opt.pack(fill="x", padx=40, pady=5)

        self.timer_label = tk.Label(master, text="Time left: 30", font=("Arial Black", 20), fg="#ff3333", bg="#1c1c1c")
        # self.timer_label.pack(pady=20)
        # self.timer_label.pack_forget()
        # self.timer_label.place(relx=0.9, y=20, anchor='ne')

        self.feedback_label = tk.Label(master, text="", font=("Arial Black", 16), fg="cyan", bg="#1c1c1c")
        # self.feedback_label.pack(pady=10)
        # self.feedback_label.pack_forget()
        # self.feedback_label.place(relx=0.5, rely=0.8, anchor='center')  # Bottom center

        self.answer_button = tk.Button(master, text="✔ Submit Answer", font=("Arial Black", 10), command=lambda: self.listen_for_voice_command("lock"), bg="#009933", fg="white", relief="groove", padx=20, pady=10)
        
        # self.answer_button.pack_forget()

        # self.start_button = tk.Button(master, text="🎲 Start Quiz", font=("Arial Black", 14), command=lambda: self.listen_for_voice_command("start"), bg="#3366cc", fg="white", relief="groove", padx=20, pady=10)
        # self.start_button.place(relx=0.5, rely=0.90, anchor='center')

        master.configure(bg="#1c1c1c")

        # Internal state
        self.q_index = -1
        self.roll_number = None
        self.time_left = 30
        self.timer_running = False

        self.master.update_idletasks()
        self.welcome_message()
        self.master.after(2000, lambda:self.listen_for_voice_command("start"))

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

    def welcome_message(self):
        message = (
            "Welcome to the AI Quiz Game! "
            "This is a fair and exciting competition where each participant is selected randomly. "
            "To start the game, say 'Agent Start Quiz'. "
            "You will be asked a question, and after selecting your answer, you must say 'Agent Lock Option' to lock in your answer. "
            "Each question has a time limit of 15 seconds. "
            "If you don't answer in time, the next question will be asked automatically. "
            "Good luck, and may the best participant win!"
        )
        
        self.speak(message)



    def start_quiz(self):
        # self.start_button.config(state=tk.DISABLED)
        random.shuffle(self.questions)
        self.roll_label.place(relx=0.5, y=20, anchor='n')
        self.next_question()

    def suspense_roll_picker(self, steps=15, delay=100):
        if steps == 15:
            self.dice_sound.play(-1)

        if steps > 0:
            self.roll_number = random.choice(self.available_roll_numbers)
            
            self.roll_label.config(text=f"🎲 Rolling: {self.roll_number}")
            self.master.after(delay, lambda: self.suspense_roll_picker(steps - 1, delay + 30))  # Increase delay for slowing effect
        else:
            self.dice_sound.stop()
            self.chosen.play(-1)
            # self.roll_number = random.choice(self.available_roll_numbers)
            self.available_roll_numbers.remove(self.roll_number)
            self.roll_label.config(text=f"🎉 Roll Number Selected: {self.roll_number}")
            self.speak(f"Selected roll number is {self.roll_number}")
            self.master.after(5000, self.ask_question)

    def next_question(self):
        if not self.available_roll_numbers:
            
            self.roll_label.config(text="🎉 All participants selected!")
            self.end_quiz()
            return

        self.q_index += 1
        if self.q_index < len(self.questions):
            self.suspense_roll_picker()  # Add thrill before each question
        else:
            self.end_quiz()

    def ask_question(self):
        q = self.questions[self.q_index]
        self.chosen.stop()

        self.question_label.place(relx=0.1, rely=0.2, anchor='w')  # Fixed center
        self.question_label.config(text=q["question"])

        self.answer_button.place(relx=0.5, rely = 0.64, anchor='center')
        self.var.set(None)
        # self.feedback_label.place(relx=0.5, rely=0.8, anchor='center')  # Bottom center
        # self.feedback_label.config(text="")  # Clear previous feedback
        i = 0
        for idx, opt in enumerate(q["options"]):
            self.options[idx].place(relx=0.1, rely=0.28 + i * 0.08, anchor='w')  # Even vertical spacing
            # place(relx=0.5, rely=0.35 + i * 0.08, anchor='center')  # Even vertical spacing
            self.options[idx].config(text=opt, value=opt, state=tk.NORMAL)
            i = i+1

        if q.get("image"):  # Check if image exists in question
            image = Image.open(q["image"])  # Open image
            image = image.resize((250, 200),  Image.Resampling.LANCZOS)  # Resize image for display
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep reference to avoid garbage collection
            self.image_label.place(relx=0.8, rely=0.4, anchor='center')  # Show image
        else:
            self.image_label.place_forget()

        self.master.update_idletasks()
        # Speak
        self.speak(f"Roll number {self.roll_number}, your question is: {q['question']}")
        for opt in q["options"]:
            self.speak(opt)

        # Start timer
        self.time_left = 15
        self.timer_running = True
        self.listen_for_voice_command("lock")
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            
            self.timer_label.place(relx=0.5, rely=0.75, anchor='center')
            if self.time_left > 0:
                self.timer_label.config(text=f"⏰ Time left: {self.time_left}")
                self.time_left -= 1
                self.master.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="⏰ Time's up!")
                self.speak("Time's up! Moving to next question.")
                self.disable_options()
                self.master.after(3000, self.next_question)

    def disable_options(self):
        for opt in self.options:
            opt.config(state=tk.DISABLED)
        self.timer_running = False

    def check_answer(self):
        if not self.timer_running:
            return

        selected = self.var.get()
        if not selected:
            return  # If nothing selected, do nothing

        correct_answer = self.questions[self.q_index]["answer"]
        self.timer_running = False  # Stop timer

        if selected == correct_answer:
            
            self.feedback_label.place(relx=0.5, rely=0.8, anchor='center')  # Bottom center
            self.feedback_label.config(text="")  # Clear previous feedback
            self.feedback_label.config(text="✅ Correct!", fg="lightgreen")
            self.master.update_idletasks()
            self.speak("Correct answer! Well done.")
            if self.q_index == len(self.questions):
                self.speak("Moving to the next Question")  # Add thrill before each question
            # else:
            #     self.end_quiz()
        else:
            self.feedback_label.config(text=f"❌ Wrong! Correct: {correct_answer}", fg="red")
            self.master.update_idletasks()
            self.speak(f"Wrong answer! Correct is {correct_answer}.")
            if self.q_index == len(self.questions):
                self.speak("Moving to the next Question")
            

        self.feedback_label.place_forget()
        self.disable_options()
        self.master.after(3000, self.next_question)  # Wait before next

    def end_quiz(self):
        self.question_label.config(text="🎉 Quiz Over! Thank you!")
        self.timer_label.config(text="")
        self.feedback_label.config(text="")
        self.speak("OK now that all the questions are answered the Quiz is over. Great job everyone!")
        self.speak("Special Congrats to the winners. Bye..")
        for opt in self.options:
            opt.pack_forget()
        self.answer_button.pack_forget()

# ---- Run App ----
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
