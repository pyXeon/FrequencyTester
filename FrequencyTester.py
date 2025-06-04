import pygame
import random
import time
import numpy as np
from tkinter import Tk, Button, Label, Entry, StringVar

pygame.init()

frequencies = [80, 120, 200, 300, 500, 1000, 2000, 3000, 5000, 8000, 10000, 14000]
score, tests_taken, accuracy, frequency  = 0, 0, 0, None

root = Tk()
root.title("Frequency Tester")

score_label = Label(root, text=f"Score: {score}"); score_label.grid(row=0, column=0)
tests_label = Label(root, text=f"Tests Taken: {tests_taken}"); tests_label.grid(row=0, column=1)

accuracy_label = Label(root, text=f"Accuracy: {accuracy}%")
accuracy_label.grid(row=0, column=2)

answer_var = StringVar()

answer_entry = Entry(root, textvariable=answer_var)
answer_entry.grid(row=1, column=0, columnspan=2)

from_submit = False

def play_sound():
    global score, tests_taken, accuracy, frequency, from_submit

    frequency = random.choice(frequencies)

    sound_array = 4096 * pygame.sndarray.numpy.sin(44100 * pygame.sndarray.numpy.arange(44100) * frequency * pygame.sndarray.numpy.pi / 44100)
    sound_array = sound_array.astype(np.int16)
    sound_array = np.repeat(sound_array[:, np.newaxis], 2, axis=1)

    sound = pygame.sndarray.make_sound(sound_array)
    sound.play()
    time.sleep(.5)
    sound.stop()

    answer_entry.delete(0, 'end')

    if not from_submit:
        tests_taken += 1
        tests_label.config(text=f"Tests Taken: {tests_taken}")

def check_answer():
    global score, tests_taken, accuracy, frequency, from_submit

    from_submit = True

    answer = answer_var.get()

    if answer:
        if int(answer) == frequency:
            score += 1
            score_label.config(text=f"Score: {score}")

        if tests_taken > 0:
            accuracy = (score / tests_taken) * 100
            accuracy = round(accuracy)
            accuracy_label.config(text=f"Accuracy: {accuracy}%")
    
    tests_taken += 1
    tests_label.config(text=f"Tests Taken: {tests_taken}")

    answer_entry.delete(0, 'end')
    
    play_sound()

play_button = Button(root, text="Play Sound", command=play_sound)
play_button.grid(row=2, column=0, columnspan=2)

submit_button = Button(root, text="Submit", command=check_answer)
submit_button.grid(row=1, column=2)

freq_label = Label(root, text="Frequencies: " + ", ".join(map(str, sorted(frequencies))))
freq_label.grid(row=3, column=0, columnspan=2)

root.bind('<Return>', lambda event: check_answer())

root.mainloop()
