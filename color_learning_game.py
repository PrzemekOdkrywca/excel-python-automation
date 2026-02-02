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
    ("red", "RED"),
    ("green", "GREEN"),
    ("blue", "BLUE"),
    ("yellow", "YELLOW"),
    ("#FFA500", "ORANGE"),      # pomarańczowy
    ("#9370DB", "PURPLE"),      # fioletowy
    ("#FFC0CB", "PINK"),        # różowy
    ("white", "WHITE"),
    ("black", "BLACK"),
]


class GraKolory:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Gra w Kolory – Color Game")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        # Skróty klawiszowe
        self.root.bind("<Escape>", lambda e: self.zamknij())
        self.root.bind("q", lambda e: self.zamknij())
        self.root.bind("Q", lambda e: self.zamknij())

        # Etykieta z nazwą koloru (duży tekst na górze)
        self.label_kolor = tk.Label(
            root,
            text="",
            font=("Arial Black", 140, "bold"),
            bg="black"
        )
        self.label_kolor.pack(expand=True)

        # Etykieta z odliczaniem 3-2-1 (ogromny tekst na środku)
        self.label_odliczanie = tk.Label(
            root,
            text="",
            font=("Arial Black", 300, "bold"),
            bg="black"
        )
        self.label_odliczanie.place(relx=0.5, rely=0.5, anchor="center")

        # Instrukcja na dole (mała)
        self.label_instrukcja = tk.Label(
            root,
            text="Powiedzcie razem nazwę koloru! • Say the color name together! • ESC/Q aby wyjść",
            font=("Arial", 16),
            bg="black",
            fg="gray"
        )
        self.label_instrukcja.pack(side="bottom", pady=20)

        self.aktualny_kolor = None
        self.start()

    def play_notes(self):
        """Odtwarza trzy razy plik ding.wav przy zmianie koloru"""
        import os
        wav_path = os.path.join(os.path.dirname(__file__), "dynamic_chord.wav")
        for _ in range(3):
            try:
                winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            except Exception as e:
                print(f"Błąd odtwarzania pliku wav: {e}")

    def start(self):
        """Rozpoczyna grę"""
        self.zmien_kolor()

    def zmien_kolor(self):
        """Zmienia kolor na ekranie"""
        # Wybierz losowy kolor (inny niż poprzedni)
        kolor, nazwa = random.choice(KOLORY)
        while kolor == self.aktualny_kolor:
            kolor, nazwa = random.choice(KOLORY)

        self.aktualny_kolor = kolor

        # Zmień tło całego okna
        self.root.configure(bg=kolor)

        # Dobierz kontrastowy kolor tekstu
        if kolor in ["black", "blue", "#9370DB"]:
            tekst_kolor = "white"
        else:
            tekst_kolor = "black"

        # Wyświetl nazwę koloru
        self.label_kolor.configure(
            text=nazwa,
            bg=kolor,
            fg=tekst_kolor
        )

        # Wyczyść odliczanie
        self.label_odliczanie.configure(bg=kolor, text="", fg=tekst_kolor)
        
        # Zaktualizuj instrukcję
        self.label_instrukcja.configure(bg=kolor, fg="gray" if kolor != "white" else "darkgray")

        # Odtwórz trzy nuty przy zmianie koloru
        self.play_notes()

        # Rozpocznij odliczanie po określonym czasie (CZAS_ZMIANY - 3 sekundy)
        self.root.after((CZAS_ZMIANY - 3) * 1000, lambda: self.odliczanie(3))

    def odliczanie(self, liczba):
        """Odlicza 3-2-1 przed zmianą koloru"""
        if liczba == 0:
            self.label_odliczanie.config(text="")
            self.root.after(1, self.zmien_kolor)
            return

        # Dobierz kontrastowy kolor tekstu
        if self.aktualny_kolor in ["black", "blue", "#9370DB"]:
            tekst_kolor = "white"
        else:
            tekst_kolor = "black"

        # Wyświetl liczbę
        self.label_odliczanie.config(
            text=str(liczba),
            fg=tekst_kolor
        )

        # Następna liczba po 1 sekundzie (bez dźwięku)
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
