"""
Gra Edukacyjna - Kolory i Angielski dla Początkujących
Ta gra jest przeznaczona zarówno dla dzieci, jak i dla wszystkich początkujących uczących się angielskiego.
Uczestnicy głośno wypowiadają nazwę koloru, który widzą na ekranie, po angielsku.
Color Learning Game - For beginners and children learning English
This game is designed for both children and anyone starting to learn English.
Participants say the color name they see on the screen out loud, in English.
"""

import tkinter as tk
import random
import winsound

# ===== USTAWIENIA / SETTINGS =====
CZAS_ZMIANY = 7      # sekundy / seconds
DZWIEK_HZ = 900      # częstotliwość beep / beep frequency
DZWIEK_MS = 200      # długość beep / beep duration
# =================================

# Lista kolorów (kolor_tła, "NAZWA_ANGIELSKA")
KOLORY = [
    ("#FF0000", "RED"),         # czerwony
    ("#00FF00", "GREEN"),       # zielony
    ("#0000FF", "BLUE"),        # niebieski
    ("#FFFF00", "YELLOW"),      # żółty
    ("#FFA500", "ORANGE"),      # pomarańczowy
    ("#800080", "PURPLE"),      # fioletowy
    ("#FF69B4", "PINK"),        # różowy
    ("#FFFFFF", "WHITE"),       # biały
    ("#000000", "BLACK"),       # czarny
]


class GraKolory:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Gra w Kolory – Color Game")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="#b3e0ff")  # jasno niebieskie tło

        # Skróty klawiszowe
        self.root.bind("<Escape>", lambda e: self.zamknij())
        self.root.bind("q", lambda e: self.zamknij())
        self.root.bind("Q", lambda e: self.zamknij())

        # Etykieta z nazwą koloru (duży tekst na górze)
        self.label_kolor = tk.Label(
            root,
            text="",
            font=("Arial", 140, "bold"),
            bg="black"
        )
        self.label_kolor.pack(expand=True)

        # Etykieta z odliczaniem 3-2-1 (ogromny tekst na środku)
        self.label_odliczanie = tk.Label(
            root,
            text="",
            font=("Arial", 300, "bold"),
            bg="#b3e0ff"
        )
        # Licznik zawsze wyśrodkowany, place tylko podczas odliczania

        # Instrukcja na dole (mała)
        self.label_instrukcja = tk.Label(
            root,
            text="Powiedzcie razem nazwę koloru! • Say the color name together! • ESC/Q aby wyjść",
            font=("Arial", 16),
            bg="#b3e0ff",
            fg="gray"
        )
        self.label_instrukcja.pack(side="bottom", pady=20)

        # Ramka na grafikę owocu i napis pod spodem
        self.fruit_frame = tk.Frame(root, bg="#b3e0ff")
        self.fruit_frame.place(relx=0.5, rely=0.5, anchor="center")  # wyśrodkuj ramkę
        self.fruit_image_label = tk.Label(self.fruit_frame, bg="#b3e0ff")
        self.fruit_image_label.pack()
        self.fruit_name_label = tk.Label(self.fruit_frame, text="", font=("Arial", 60, "bold"), bg="#b3e0ff", fg="#003366")
        self.fruit_name_label.pack(pady=2)

        self.aktualny_kolor = None
        self.fruit_photo = None
        self.sekwencja = 0  # indeks w KOLORY
        self.tryb_naprzemienny = 0  # 0: kolor, 1: owoc
        self.nowa_runda()

    def nowa_runda(self):
        """Losuje i wyświetla grafikę owocu lub planszę z kolorem, potem uruchamia odliczanie."""
        import os
        from PIL import Image, ImageTk
        tekst_kolor = "#003366"
        kolor, nazwa = KOLORY[self.sekwencja % len(KOLORY)]
        if self.tryb_naprzemienny == 0:
            # Gra w kolory: tło = kolor, tekst na środku
            self.aktualny_kolor = kolor
            self.root.configure(bg=kolor)
            self.label_kolor.configure(text=nazwa, bg=kolor, fg="white" if nazwa in ["BLACK","BLUE","PURPLE"] else "black")
            self.fruit_image_label.config(image="", bg=kolor)
            self.fruit_name_label.config(text="", bg=kolor)
            self.label_instrukcja.configure(bg=kolor, fg="gray")
            self.label_odliczanie.config(bg=kolor, text="", fg="gray")
            self.fruit_frame.place_forget()  # Ukryj ramkę z owocem
        else:
            # Gra w owoce: tło niebieskie, owoc na środku, powiązanie kolor-owoc
            bg_color = "#b3e0ff"
            self.root.configure(bg=bg_color)
            self.label_instrukcja.configure(bg=bg_color, fg="gray")
            self.label_kolor.configure(text="", bg=bg_color, fg=tekst_kolor)
            self.fruit_frame.place(relx=0.5, rely=0.5, anchor="center")
            fruit_map = {
                "RED": ("cherry", "CHERRY"),
                "GREEN": ("lime", "LIME"),
                "BLUE": ("blueberry.", "BLUEBERRY"),
                "YELLOW": ("lemon", "LEMON"),
                "ORANGE": ("orange", "ORANGE"),
                "PURPLE": ("plum", "PLUM"),
                "PINK": ("strawberry.", "STRAWBERRY"),
                "WHITE": ("coconut", "COCONUT"),
                "BLACK": ("blackberry", "BLACKBERRY"),
            }
            fruit_info = fruit_map[nazwa]
            fruit_file_base = fruit_info[0]
            fruit_name_en = fruit_info[1]
            fruit_path = None
            fruit_dir = os.path.join(os.path.dirname(__file__), "fruit_images")
            candidate = os.path.join(fruit_dir, fruit_file_base + ".png")
            if os.path.exists(candidate):
                fruit_path = candidate
            if fruit_path:
                self.aktualny_kolor = kolor
                try:
                    img = Image.open(fruit_path).convert("RGBA")
                    img = img.resize((400, 400), Image.LANCZOS)
                    self.fruit_photo = ImageTk.PhotoImage(img)
                    self.fruit_image_label.config(image=self.fruit_photo, bg=bg_color)
                    self.fruit_name_label.config(text=fruit_name_en, bg=bg_color, fg=tekst_kolor)
                except Exception as e:
                    self.fruit_image_label.config(image="", bg=bg_color)
                    self.fruit_name_label.config(text="", bg=bg_color)
            else:
                self.fruit_image_label.config(image="", bg=bg_color)
                self.fruit_name_label.config(text="BRAK GRAFIKI", bg=bg_color, fg="red")
            self.label_odliczanie.config(bg=bg_color, text="", fg=tekst_kolor)
            self.sekwencja += 1
        self.tryb = self.tryb_naprzemienny
        self.tryb_naprzemienny = 1 - self.tryb_naprzemienny
        if self.tryb_naprzemienny == 0:
            self.sekwencja += 1
        # Po 2 sekundach ukryj wszystko i zacznij odliczanie
        self.root.after(2000, self.start_odliczanie)

    def start_odliczanie(self):
        # Ukryj grafikę i napis koloru, pokaż tylko licznik
        if self.tryb == 0:
            # Kolor: ukryj label_kolor
            self.label_kolor.config(text="", bg=self.root.cget("bg"))
        else:
            # Owoc: ukryj grafikę i napis
            self.fruit_image_label.config(image="", bg=self.root.cget("bg"))
            self.fruit_name_label.config(text="", bg=self.root.cget("bg"))
        # Pokaż licznik na środku, tło licznika zawsze jak tło okna
        self.label_odliczanie.config(bg=self.root.cget("bg"))
        self.label_odliczanie.place(relx=0.5, rely=0.5, anchor="center")
        self.label_odliczanie.config(text="3", fg="black")
        self.odliczanie(3)

    def play_notes(self):
        print("[DEBUG] play_notes wywołane!")
        try:
            winsound.Beep(DZWIEK_HZ, DZWIEK_MS)
        except Exception:
            print("[DEBUG] Beep error!")
            pass

    def odliczanie(self, liczba):
        """Odlicza 3-2-1 przed zmianą koloru. Podczas odliczania ukrywa nazwę koloru."""

        if liczba == 0:
            self.label_odliczanie.config(text="")
            self.label_odliczanie.place_forget()  # Ukryj licznik
            self.root.after(500, self.nowa_runda)
            return

        if liczba == 1:
            print(f"[DEBUG] odliczanie: {liczba} - wywołanie play_notes")
            self.play_notes()  # dźwięk dokładnie przy "1"

        # Wyświetl liczbę
        # Ustaw tło licznika na tło okna (przezroczyste w praktyce)
        # Ustaw tło licznika na tło okna (przezroczyste w praktyce)
        # Tło licznika: zawsze jak tło okna, czcionka Arial
        self.label_odliczanie.config(
            text=str(liczba),
            fg="black",
            bg=self.root.cget("bg"),
            font=("Arial", 300, "bold")
        )
        # Następna liczba po 1 sekundzie
        self.root.after(1000, lambda: self.odliczanie(liczba - 1))

    def zamknij(self):
        """Zamyka aplikację"""
        self.root.destroy()


def main():
    """Funkcja główna"""
    root = tk.Tk()
    GraKolory(root)
    root.mainloop()


if __name__ == "__main__":
    main()
