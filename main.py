import pyttsx3
import openai
import random
import time
import pyaudio
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

interval_min = 3
interval_max = 10



openai.api_key = "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"

engine = pyttsx3.init()

root = tk.Tk()

prompt = "Welcome to the drinking game! I am soBOT and I will be your host of this game. Here are the rules:\n\n\
1. I will pose a question with four different answers.\n\
2. If you answer correctly, another player must answer the next question.\n\
3. If the answer is incorrect, you must drink.\n\
4. At random times in the game, everyone has to drink.\n\n\
Is everyone ready for the drinking game? Let's start! \n\n\
Enter the number of players"

def numeric_value(text):
    """Returns numeric value of players"""
    try:
        number = int(text)
    except ValueError as e:
        text = 'one'
        print(e)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f"exsctract the numeric value from this text: {text} and use word-to-number conversion and return only the number"}]
    )
    print(completion)
    return completion['choices'][0]['message']['content']





def ask_question():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": "Ask me one funny trivia and print 4 numbered answers without the final answer"}]
    )

    print(completion)
    return completion['choices'][0]['message']['content']


def answer_funny_question(answer):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f"Respond funny to these message, then offer to return to the game: {answer}"}]
    )
    print(completion)
    return completion['choices'][0]['message']['content']


def answer_question(content, answer):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f"{content} and the answer is {answer}. Write only 'correct' if the answer is correct or 'not correct' otherwise"}]
    )

    return completion['choices'][0]['message']['content']

def ask_trivia():
    global text
    global question
    replied = False
    wrong_answer = 'Wrong answer. Now drink'
    correct_answer = 'Correct answer, next person'
    ask_question_flag = True


    while ask_question_flag:
        question = ask_question()

        print(question)

        question_label = tk.Label(root, text=question, bg='#333333', fg='white')
        question_label.pack()

        engine.say(question)
        engine.runAndWait()

        time.sleep(1)

        r = sr.Recognizer()
        mic = sr.Microphone()

        attempts = 0
        while attempts < 3:
            with mic as source:
                print("Speak now:")
                audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                break
            except sr.UnknownValueError:
                attempts += 1
                if attempts < 3:
                    print("Sorry, I did not understand that. Please try again.")
                else:
                    print("Sorry, I still did not understand that. Please type your answer.")
                    text = input()
                    break
            except sr.RequestError as e:
                print(f"Sorry, something went wrong: {e}")
                break

        answer_split = question.split()  # sprawdza odpowiedzi zamiast pytań
        answer_split = [i.lower() for i in answer_split]
        question_split = text.split()
        question_split = [i.lower() for i in question_split]
        for i in question_split:
            if i in answer_split:
                replied = True

        if replied:
            answer = answer_question(question, text)
            print(answer)
            engine.say(answer)
            engine.runAndWait()

            time.sleep(1)

            if 'not correct' in answer:
                print(wrong_answer)
                engine.say(wrong_answer)
            elif 'correct' in answer:
                print(correct_answer)
                engine.say(correct_answer)
            engine.runAndWait()

            time.sleep(10)
            ask_question_flag = False
        else:
            funny_answer = answer_funny_question(text)
            print(funny_answer)
            engine.say(funny_answer)
            engine.runAndWait()

def manually_input_number_of_players():
    def submit_number_of_players():
        try:
            number = int(entry.get())
            if number > 1:
                raise ValueError("Number of players must be greater than 1")
            number_of_players.set(number)
            number_window.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    number_window = tk.TopLevel()
    number_window.title("Number of players")
    label = tk.Label(number_window, text="Enter the number of players")
    label.pack()
    entry = tk.Entry(number_window)
    entry.pack()
    submit_button = tk.Button(number_window, text="Submit", command=submit_number_of_players)
    submit_button.pack()


def drinking_game():

    messages = []

    engine.say(prompt)
    engine.runAndWait()
    time.sleep(1)

    r = sr.Recognizer()
    mic = sr.Microphone()
    text = 'one'

    with mic as source:
        attempts = 0
        while attempts < 3:  # po 3 nierozpoznanych próbach voice recognition input pisany
            print("Speak now:")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                break
            except sr.UnknownValueError:
                attempts += 1
                if attempts < 3:
                    print("Sorry, I did not understand that. Please try again.")
                else:
                    print("Sorry, I did not understand that. Please input the answer on the keyboard.")
                    #manually_input_number_of_players()
            except sr.RequestError as e:
                print(f"Sorry, something went wrong: {e}")



    number_of_players = numeric_value(text)
    #number_of_players = '1'
    print("Number of players: " + number_of_players)
    number_of_players = int(number_of_players)
    print(number_of_players)

    list_of_players = []
    for i in range(number_of_players):
        ask_name = "Input the name of player " + str(i + 1) + ": "
        flag = True
        unrecognized_counter = 0  # nierozpoznane imiona graczy
        while flag:
            engine.say(ask_name)
            engine.runAndWait()
            time.sleep(1)
            r = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                print("Speak now:")
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(f"You said: {text}")
                unrecognized_counter = 0  # wyzerowanie niezrozumianych słów jeśli recognizer wychywci
            except sr.UnknownValueError:
                unrecognized_counter += 1
                if unrecognized_counter == 3:  # 3 nieudane próby input pisany
                    text = input("Sorry, I didn't understand that. Please enter the name on the keyboard: ")
                    print(f"You entered: {text}")
                    unrecognized_counter = 0
                    print("Sorry, I didn't understand that.")
            except sr.RequestError as e:
                print(f"Sorry, something went wrong: {e}")

            flag = False
            list_of_players.append(text)

    time.sleep(2)
    players = list_of_players

    while True:
        options = [1, 2, 3]

        question = random.choice(options)

        player = random.choice(players)

        if question == 1:
            engine.say("Everyone drinks")
            engine.runAndWait()
        elif question == 2:
            engine.say(f"Player {player} should drink")
            engine.runAndWait()
        elif question == 3:
            engine.say(f"This is a question for player {player}")
            # podaj jedną odpowiedz
            # zmiana odpowiediz podczas pytania
            # Ostateczna odpowiedz
            engine.runAndWait()
            ask_trivia()

def start_game():
    try:
        drinking_game()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def main():
    root.title("Drinking game")
    root.configure(bg='#333333')

    label = tk.Label(root, text="Welcome to the Drinking Game!", font=("Arial", 20), fg="#ffffff", bg="#333333")
    label.pack(padx=20, pady=20)

    start_button = tk.Button(root, text="Start", command=start_game, font=("Arial", 18), width=15, height=2, bg="#007bff", fg="#ffffff")
    start_button.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == '__main__':
    main()