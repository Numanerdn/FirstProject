from tkinter import *
import base64
import hashlib
from tkinter import messagebox

from cryptography.fernet import Fernet

window = Tk()
window.title("Secret Notes")
window.minsize(300, 530)


def olustur ():
    baslik = entry.get()
    icerik = text.get("1.0",END)
    sifre = entry1.get()

    if baslik.strip() == "" or icerik.strip() == "" or sifre.strip() == "" :
        messagebox.showerror("Hata","Bos Birakilan Yerleri Doldurunuz")
        return

    anahtar = hashlib.sha256(sifre.encode()).digest()
    anahtar = base64.urlsafe_b64encode(anahtar)

    sifreleyici = Fernet(anahtar)
    sifreli_metin = sifreleyici.encrypt(icerik.encode())
    try:
        with open (baslik,"xb", ) as dosya:
            dosya.write(sifreli_metin)
            text.delete("1.0", "end")
            entry.delete(0, "end")
            entry1.delete(0, "end")
            messagebox.showinfo("Başarılı", "Dosya şifrelenerek oluşturuldu!")
    except Exception as hata:
        messagebox.showerror("Hata",str(hata))


def dosya_ac():
    sifre = entry1.get()

    try:
        with open(entry.get(), "rb") as dosya:
            sifreli_metin = dosya.read()

        anahtar = hashlib.sha256(sifre.encode()).digest()
        anahtar = base64.urlsafe_b64encode(anahtar)

        sifreleyici = Fernet(anahtar)
        mesaj = sifreleyici.decrypt(sifreli_metin).decode()

        text.delete("1.0", "end")
        text.insert("1.0", mesaj)

    except :
        messagebox.showinfo("Hata","Şifre yanlış veya dosya okunamadı.")




photo = PhotoImage(file="secret.png")
photo = photo.subsample(10, 8)
label = Label(image=photo,)
label.pack(pady=50,padx=10)

label = Label(text="Enter your title", font=("Times New Roman", 10, "bold"))
label.pack()

entry = Entry(width=30)
entry.pack()

label1 = Label(text="Enter your secret", font=("Times New Roman", 12, "bold"))
label1.pack()

text = Text(width=30, height=10)
text.pack()

label2 = Label(text="Enter master key", font=("Times New Roman", 12, "bold"))
label2.pack()

entry1 = Entry(show="*",width=30)

entry1.pack(pady=10)

button = Button(text="Save & Encrypt",command=olustur)
button.pack(pady=10)

button1 = Button(text= "Decrypt",command=dosya_ac)
button1.pack()



window.mainloop()