# import packages
import winsound, time, io, pygame
from gtts import gTTS
import tkinter as Tk
from tkinter import StringVar, messagebox

# Morse code dictionary
morse_code: "dict[str, str]" = {
    "": "  ",
    " ": "/",
    "\n": "//",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
}

# inverse dictionary
textConverter: "dict[str, str]" = {value: key for (key, value) in morse_code.items()}

# Variables
root: Tk = Tk.Tk()
root.title("Morse Code")
text_var: StringVar = Tk.StringVar()
code_var: StringVar = Tk.StringVar()

# Text to code
def encoder() -> None:
    code_display.config(state="normal")
    code_display.delete("1.0", Tk.END)
    text: str = text_entry.get("1.0", "end-1c").upper()
    code: str = ""
    try:
        for letter in text:
            code = f"{code} {morse_code[letter]}"
    except Exception:
        messagebox.showerror("Error", "Please enter valid text")
    code_display.insert(Tk.INSERT, code)
    code_display.config(state="disabled")


# Code to text
def decoder():
    text_display.config(state="normal")
    text_display.delete("1.0", Tk.END)
    code: str = code_entry.get("1.0", "end-1c")
    groups: list[str] = [i for j in code.split() for i in (j, "  ")]
    text: str = ""
    try:
        for group in groups:
            text = text + textConverter[group]
    except Exception:
        messagebox.showerror("Error", "Please enter valid code")
    text_display.insert(Tk.INSERT, text)
    text_display.config(state="disabled")


# Code to beeps
def sound():
    code: str = code_display.get("1.0", "end-1c")
    beeps: list = []
    beeps[1:]: list = code

    for beep in beeps:
        if beep == ".":
            winsound.Beep(1000, 200)
        elif beep == "-":
            winsound.Beep(1000, 600)
        elif beep in ["/", "//"]:
            time.sleep(0.8)
        else:
            time.sleep(0.6)


# Text to audio
def speak():
    text: str = text_display.get("1.0", "end-1c")
    try:
        with io.BytesIO() as file:
            gTTS(text=text, lang="en").write_to_fp(file)
            file.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue
    except Exception:
        messagebox.showwarning("Sorry", "I only speak english :(")


# Main function
if __name__ == "__main__":
    text_label = Tk.Label(root, text="Enter text : ")
    text_entry = Tk.Text(root, width=50, height=5)
    code_output = Tk.Label(root, text="Encoded message : ")
    code_display = Tk.Text(root, width=50, height=5)

    code_label = Tk.Label(root, text="Enter code : ")
    code_entry = Tk.Text(root, width=50, height=5)
    text_output = Tk.Label(root, text="Decoded message : ")
    text_display = Tk.Text(root, width=50, height=5)

    text_btn = Tk.Button(root, text="Encode", command=encoder, width=50)
    sound_btn = Tk.Button(root, text="Beep", command=sound, width=50)
    code_btn = Tk.Button(root, text="Decode", command=decoder, width=50)
    speak_btn = Tk.Button(root, text="Audio", command=speak, width=50)

    text_label.grid(row=0, column=0, padx=2, pady=2)
    text_entry.grid(row=1, column=0, padx=2, pady=2)
    text_btn.grid(row=2, column=0, padx=2, pady=2)
    code_output.grid(row=3, column=0, padx=2, pady=2)
    code_display.grid(row=4, column=0, padx=2, pady=2)
    sound_btn.grid(row=5, column=0, padx=2, pady=2)

    code_label.grid(row=0, column=1, padx=2, pady=2)
    code_entry.grid(row=1, column=1, padx=2, pady=2)
    code_btn.grid(row=2, column=1, padx=2, pady=2)
    text_output.grid(row=3, column=1, padx=2, pady=2)
    text_display.grid(row=4, column=1, padx=2, pady=2)
    speak_btn.grid(row=5, column=1, padx=2, pady=2)

    code_display.config(state="disabled")
    text_display.config(state="disabled")

    root.mainloop()
