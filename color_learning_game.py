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


        # Ramka na grafikę owocu/zwierzęcia i napis pod spodem
        self.fruit_frame = tk.Frame(root, bg="#b3e0ff")
        self.fruit_frame.place(relx=0.5, rely=0.5, anchor="center")  # wyśrodkuj ramkę
        self.fruit_image_label = tk.Label(self.fruit_frame, bg="#b3e0ff")
        self.fruit_image_label.pack()
        self.fruit_name_label = tk.Label(self.fruit_frame, text="", font=("Arial", 60, "bold"), bg="#b3e0ff", fg="#003366")
        self.fruit_name_label.pack(pady=2)

        # Punkty
        self.punkty = 0
        self.max_punkty = 10
        self.label_punkty = tk.Label(root, text="Punkty: 0", font=("Arial", 32, "bold"), bg="#b3e0ff", fg="#003366")
        self.label_punkty.place(relx=0.01, rely=0.01, anchor="nw")

        # Sukces - grafika na cały ekran
        self.sukces_label = None
        self.sukces_tekst_label = None
        self.sukces_aktywny = False

        # Obsługa klawisza Enter
        self.root.bind("<Return>", self.dodaj_punkt)

        # Inicjalizacja zmiennych
        self.aktualny_kolor = None
        self.fruit_photo = None
        self.sekwencja = 0  # indeks w KOLORY
        self.tryb_naprzemienny = 0  # 0: kolor, 1: owoc, 2: zwierzę
        self.nowa_runda()

    def dodaj_punkt(self, event=None):
        if self.sukces_aktywny:
            # Restart gry po sukcesie
            self.restart_gry()
            return
        if self.punkty < self.max_punkty:
            self.punkty += 1
            self.label_punkty.config(text=f"Punkty: {self.punkty}")
            if self.punkty == self.max_punkty:
                self.pokaz_sukces()


    def pokaz_sukces(self):
        import os
        from PIL import Image, ImageTk
        # Zatrzymaj grę i wyświetl sukces na cały ekran
        self.sukces_aktywny = True
        
        # Ukryj wszystkie elementy gry
        self.label_kolor.place_forget()
        self.label_odliczanie.place_forget()
        self.fruit_frame.place_forget()
        self.fruit_image_label.config(image="")
        self.fruit_name_label.config(text="")
        
        # Zmień tło na białe
        self.root.configure(bg="#ffffff")
        self.label_instrukcja.configure(bg="#ffffff", fg="gray", text="Naciśnij ENTER aby zagrać ponownie • Press ENTER to play again • ESC/Q aby wyjść")
        
        # Wyświetl grafikę sukcesu na cały ekran
        sukces_path = os.path.join(os.path.dirname(__file__), "success-.png")
        if hasattr(self, 'sukces_label') and self.sukces_label:
            self.sukces_label.destroy()
        if os.path.exists(sukces_path):
            try:
                img = Image.open(sukces_path).convert("RGBA")
                szer = self.root.winfo_screenwidth()
                wys = self.root.winfo_screenheight()
                img = img.resize((szer, wys), Image.LANCZOS)
                self.sukces_photo = ImageTk.PhotoImage(img)
                self.sukces_label = tk.Label(self.root, image=self.sukces_photo, bg="#ffffff")
                self.sukces_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                self.sukces_label = tk.Label(self.root, text="SUCCESS!\n🎉", font=("Arial", 120, "bold"), bg="#ffffff", fg="#00aa00")
                self.sukces_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.sukces_label = tk.Label(self.root, text="SUCCESS!\n🎉", font=("Arial", 120, "bold"), bg="#ffffff", fg="#00aa00")
            self.sukces_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Dodaj napis GRATULACJE na środku ekranu
        if hasattr(self, 'sukces_tekst_label') and self.sukces_tekst_label:
            self.sukces_tekst_label.destroy()
        self.sukces_tekst_label = tk.Label(
            self.root, 
            text="GRATULACJE ! :)", 
            font=("Arial", 100, "bold"), 
            bg="#ffffff", 
            fg="#ff6600"
        )
        self.sukces_tekst_label.place(relx=0.5, rely=0.5, anchor="center")

    def restart_gry(self):
        """Restartuje grę po sukcesie"""
        # Ukryj sukces
        if hasattr(self, 'sukces_label') and self.sukces_label:
            self.sukces_label.destroy()
            self.sukces_label = None
        
        # Ukryj tekst gratulacji
        if hasattr(self, 'sukces_tekst_label') and self.sukces_tekst_label:
            self.sukces_tekst_label.destroy()
            self.sukces_tekst_label = None
        
        # Resetuj flagi i punkty
        self.sukces_aktywny = False
        self.punkty = 0
        self.label_punkty.config(text="Punkty: 0")
        self.sekwencja = 0
        self.tryb_naprzemienny = 0
        
        # Przywróć tło i instrukcję
        self.root.configure(bg="#b3e0ff")
        self.label_instrukcja.configure(bg="#b3e0ff", fg="gray", text="Powiedzcie razem nazwę koloru! • Say the color name together! • ESC/Q aby wyjść")
        
        # Przywróć widoczność elementów
        self.label_kolor.pack(expand=True)
        self.label_punkty.place(relx=0.01, rely=0.01, anchor="nw")
        
        # Rozpocznij nową rundę
        self.nowa_runda()

    def get_animal_map(self):
        # Mapowanie: nazwa (do losowania) -> (plik_graficzny, nazwa_angielska)
        return {
            "COW": ("cow", "COW"),
            "ELEPHANT": ("elephant", "ELEPHANT"),
            "FISH": ("fish", "FISH"),
            "FROG": ("frog", "FROG"),
            "HORSE": ("horse", "HORSE"),
        }

    def nowa_runda(self):
        """Losuje i wyświetla grafikę owocu, zwierzęcia lub planszę z kolorem, potem uruchamia odliczanie."""
        # Nie uruchamiaj nowej rundy jeśli sukces jest aktywny
        if self.sukces_aktywny:
            return
        
        import os
        from PIL import Image, ImageTk
        tekst_kolor = "#003366"
        bg_color = "#b3e0ff"
        # 0: kolor, 1: owoc, 2: zwierzę
        tryb = getattr(self, 'tryb_naprzemienny', 0)
        kolor, nazwa = KOLORY[self.sekwencja % len(KOLORY)]
        if tryb == 0:
            # Gra w kolory: tło = kolor, tekst na środku
            self.aktualny_kolor = kolor
            self.root.configure(bg=kolor)
            self.label_kolor.configure(text=nazwa, bg=kolor, fg="white" if nazwa in ["BLACK","BLUE","PURPLE"] else "black")
            self.fruit_image_label.config(image="", bg=kolor)
            self.fruit_name_label.config(text="", bg=kolor)
            self.label_instrukcja.configure(bg=kolor, fg="gray")
            self.label_odliczanie.config(bg=kolor, text="", fg="gray")
            self.fruit_frame.place_forget()  # Ukryj ramkę z owocem
        elif tryb == 1:
            # Gra w owoce: tło niebieskie, owoc na środku
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
        else:
            # Gra w zwierzęta: tło niebieskie, zwierzę na środku
            self.root.configure(bg=bg_color)
            self.label_instrukcja.configure(bg=bg_color, fg="gray")
            self.label_kolor.configure(text="", bg=bg_color, fg=tekst_kolor)
            self.fruit_frame.place(relx=0.5, rely=0.5, anchor="center")
            animal_map = self.get_animal_map()
            animal_names = list(animal_map.keys())
            animal_name = random.choice(animal_names)
            animal_file_base, animal_name_en = animal_map[animal_name]
            animal_path = None
            animal_dir = os.path.join(os.path.dirname(__file__), "animal_images")
            candidate = os.path.join(animal_dir, animal_file_base + ".png")
            if os.path.exists(candidate):
                animal_path = candidate
            if animal_path:
                try:
                    img = Image.open(animal_path).convert("RGBA")
                    img = img.resize((400, 400), Image.LANCZOS)
                    self.fruit_photo = ImageTk.PhotoImage(img)
                    self.fruit_image_label.config(image=self.fruit_photo, bg=bg_color)
                    self.fruit_name_label.config(text=animal_name_en, bg=bg_color, fg=tekst_kolor)
                except Exception as e:
                    self.fruit_image_label.config(image="", bg=bg_color)
                    self.fruit_name_label.config(text="", bg=bg_color)
            else:
                self.fruit_image_label.config(image="", bg=bg_color)
                self.fruit_name_label.config(text="BRAK GRAFIKI", bg=bg_color, fg="red")
            self.label_odliczanie.config(bg=bg_color, text="", fg=tekst_kolor)
            self.sekwencja += 1
        self.tryb = tryb
        self.tryb_naprzemienny = (tryb + 1) % 3
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
