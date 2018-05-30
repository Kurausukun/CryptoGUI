from collections import defaultdict
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import tkinter as tk

prime = 127

def encrypt(file, password, output):
    open(file, "r")
    counter = 0
    plaintext = {}
    f = defaultdict(lambda:0)
    for letter in file:
        plaintext[counter] = ord(letter)
        counter += 1
    r = 0
    for x in range(0, len(password)):
        if r == 0:
            f[1] = (plaintext[1] + ord(password[x])) % prime
            f[2] = (plaintext[2] + plaintext[1] * f[1]) % prime
            f[3] = (plaintext[3] + plaintext[1] * f[2]) % prime
            for y in range(3, len(plaintext.values())):
                if y % 4 == 3 or y % 4 == 2:
                    f[y] = (plaintext[y] + plaintext[1] * f[y - 2]) % prime
                else:
                    f[y] = (plaintext[y] + plaintext[y - 2] * f[1]) % prime
            r = 1
        else:
            plaintext[1] = (f[1] + ord(password[1])) % prime
            plaintext[2] = (f[2] - plaintext[1] * f[1]) % prime
            plaintext[3] = (f[3] - plaintext[1] * f[2]) % prime
            for y in range(3, len(plaintext.values())):
                if y % 4 == 3 or y % 4 == 2:
                    plaintext[y] = (f[y] - plaintext[1] * f[y - 2]) % prime
                else:
                    plaintext[y] = (f[y] - plaintext[y - 2] * f[1]) % prime
            r = 0
    with open(output, "w") as temp:
        for item in f.values():
            temp.write(chr(item))

def decrypt(file, password, output):
    open(file, "r")
    counter = 0
    ciphertext = {}
    p = {}
    l = defaultdict(lambda: 0)
    for letter in file:
        ciphertext[counter] = ord(letter)
        counter += 1
    if len(password) % 2 == 0:
        r = 0
        p = ciphertext
    else:
        r = 1
        l = ciphertext
    for x in range(len(password) - 1, -1, -1):
        if r == 0:
            l[1] = (p[1] - ord(password[x])) % prime
            l[2] = (p[2] + p[1] * l[1]) % prime
            l[3] = (p[3] + p[1] * l[2]) % prime
            for y in range (3, len(ciphertext.values())):
                if y % 4 == 3 or y % 4 == 2:
                    l[y] = (p[y] + p[1] * l[y - 2]) % prime
                else:
                    l[y] = (p[y] + p[y - 2] * l[1]) % prime
            r = 1
        else:
            p[1] = (l[1] - ord(password[x])) % prime
            p[2] = (l[2] - p[1] * l[1]) % prime
            p[3] = (l[3] - p[1] * l[2]) % prime
            for y in range(3, len(ciphertext.values())):
                if y % 4 == 3 or y % 4 == 2:
                    p[y] = (l[y] - p[1] * l[y - 2]) % prime
                else:
                    p[y] = (l[y] - p[y - 2] * l[1]) % prime
            r = 0
    with open(output, "w") as temp:
        for item in p.values():
            temp.write(chr(item))

def getFile():
    filename = askopenfilename()
    fileEntry.delete(0, tk.END)
    fileEntry.insert(0, filename)

def saveFile():
    filename = asksaveasfilename(filetypes = [("All files", "*.*")])
    outEntry.delete(0, tk.END)
    outEntry.insert(0, filename)

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        global fileEntry
        global outEntry
        self.master.title("Encrypt/Decrypt")
        self.pack(fill = tk.BOTH, expand = 1)
        fileEntry = tk.Entry(self)
        fileEntry.place(relx = 0.33, rely = 0.25)
        fileEntry.grid(row = 0, column = 1)
        fileEntry.bind("<Button-1>", lambda _: getFile())
        tk.Label(self, text = "Choose file").grid(row = 0, sticky = "W", padx = 25, pady = 60)
        passEntry = tk.Entry(self)
        passEntry.place(relx = 0.33, rely = 0.50)
        passEntry.grid(row = 1, column = 1)
        tk.Label(self, text = "Password").grid(row = 1, sticky = "W", padx = 25)
        outEntry = tk.Entry(self)
        outEntry.place(relx = 0.33, rely = 0.75)
        outEntry.grid(row = 2, column = 1)
        outEntry.bind("<Button-1>", lambda _: saveFile())
        tk.Label(self, text = "Save as").grid(row = 2, sticky = "W", padx = 25, pady = 60)
        encryptButton = tk.Button(self, text = "Encrypt", command = lambda: encrypt(fileEntry.get(), passEntry.get(), outEntry.get()))
        encryptButton.place(relx = 0.75, rely = 0.33)
        decryptButton = tk.Button(self, text = "Decrypt", command = lambda: decrypt(fileEntry.get(), passEntry.get(), outEntry.get()))
        decryptButton.place(relx = 0.75, rely = 0.50)

root = tk.Tk()
root.geometry("480x360")
app = Window(root)
root.mainloop()