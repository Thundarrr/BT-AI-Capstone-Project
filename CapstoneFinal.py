from typing import Self
import openai
import speech_recognition as sr
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk

# Set up OpenAI API credentials
openai.api_key = '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'

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q: {question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].text.strip()
    return message

# Function to recognize speech using microphone
def recognize_speech(): 
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BroGPT :) ")
        self.window.geometry("600x600")

        self.scroll_frame = tk.Frame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        # Set light blue background color for the chat history area
        self.chat_history = tk.Text(self.scroll_frame, wrap="word", state="disabled", bg="light blue", fg="blue")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set)

        self.question_entry = tk.Entry(self.window, width=200, font=("Times", 16))
        self.question_entry.pack(pady=10)

        # Set light blue background color for the buttons
        button_bg_color = "light blue"
        button_text_color = "blue"

        self.ask_button = tk.Button(self.window, text="Ask", width=200, command=self.ask_question, font=("Arial", 12), bg=button_bg_color, fg=button_text_color)
        self.ask_button.pack(pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", width=200, command=self.clear_all, font=("Arial", 12), bg=button_bg_color, fg=button_text_color)
        self.clear_button.pack(pady=10)

        self.listen_button = tk.Button(self.window, text="Speak", width=200, command=self.listen_question, font=("Arial", 12), bg=button_bg_color, fg=button_text_color)
        self.listen_button.pack(pady=10)

        self.window.mainloop()

    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        if self.chat_history.index('end') != None:
            self.chat_history.insert('end', "You: " + question + "\n", 'bold')
            self.chat_history.insert('end', "BroGPT: " + response + "\n\n")
            self.chat_history.tag_configure('bold', font=("Times", 16, 'bold'))
            self.chat_history.configure(state="disabled")
            self.chat_history.yview('end')







if __name__ == "__main__":
    gui = ChatbotGUI()
