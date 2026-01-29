# 🎨 Gra w Kolory i Nauka Angielskiego / Color Learning Game

## 📖 Opis / Description

Interaktywna gra edukacyjna dla dzieci w wieku przedszkolnym, która uczy kolorów i podstawowych słów angielskich w zabawny sposób.

Interactive educational game for preschool children that teaches colors and basic English words in a fun way.

## ✨ Funkcje / Features

- 🌈 **10 Kolorów do Nauki** - Czerwony, Niebieski, Żółty, Zielony, Pomarańczowy, Fioletowy, Różowy, Brązowy, Czarny, Biały
- 🎮 **Tryb Gry** - Quiz z pytaniami wielokrotnego wyboru
- 📚 **Tryb Nauki** - Przeglądaj wszystkie kolory z tłumaczeniami
- 🏆 **System Punktacji** - Śledź postępy dziecka
- 🎨 **Kolorowy Interfejs** - Przyjazny dla dzieci design
- 🔊 **Wsparcie dla Dźwięków** - Gotowe do dodania efektów dźwiękowych

## 🚀 Jak Uruchomić / How to Run

### Wymagania / Requirements

- Python 3.7 lub nowszy / Python 3.7 or newer
- Biblioteka pygame (dla dźwięków)

### Instalacja / Installation

1. Zainstaluj wymagane biblioteki:
```bash
pip install pygame
```

2. Uruchom grę:
```bash
python color_learning_game.py
```

## 🎯 Jak Grać / How to Play

1. **Nowa Gra** - Kliknij "Nowa Gra / New Game" aby rozpocząć
2. **Odpowiadaj** - Zobacz kolor i wybierz poprawną nazwę angielską
3. **Ucz się** - Kliknij "Tryb Nauki / Learn Mode" aby zobaczyć wszystkie kolory

### Tryb Gry / Game Mode
- Gra zadaje 10 pytań
- Każde poprawne odpowiedź = 1 punkt
- Po każdym pytaniu widzisz informację zwrotną
- Na końcu gry widzisz wynik końcowy

### Tryb Nauki / Learn Mode
- Przeglądaj wszystkie kolory
- Zobacz nazwy polskie i angielskie
- Idealne do zapamiętywania przed grą

## 🎨 Kolory w Grze / Colors in the Game

| Polski | English | Kolor / Color |
|--------|---------|---------------|
| Czerwony | Red | 🔴 |
| Niebieski | Blue | 🔵 |
| Żółty | Yellow | 🟡 |
| Zielony | Green | 🟢 |
| Pomarańczowy | Orange | 🟠 |
| Fioletowy | Purple | 🟣 |
| Różowy | Pink | 🩷 |
| Brązowy | Brown | 🟤 |
| Czarny | Black | ⚫ |
| Biały | White | ⚪ |

## 🎓 Korzyści Edukacyjne / Educational Benefits

✅ Nauka kolorów w dwóch językach
✅ Rozwijanie pamięci wzrokowej
✅ Nauka podstawowego słownictwa angielskiego
✅ Koordynacja ręka-oko (klikanie myszką)
✅ Budowanie pewności siebie przez gamifikację
✅ Natychmiastowa informacja zwrotna

## 🔧 Personalizacja / Customization

Możesz łatwo dostosować grę:

- **Dodaj więcej kolorów** - Edytuj słownik `self.colors`
- **Zmień liczbę pytań** - Zmień wartość `self.max_questions`
- **Dodaj dźwięki** - Dodaj pliki .mp3/.wav i zaktualizuj funkcję `play_sound()`
- **Zmień kolory interfejsu** - Dostosuj wartości kolorów w kodzie

## 📝 Przykład Dodania Dźwięków / Adding Sounds Example

Aby dodać dźwięki:

1. Stwórz folder `sounds/`
2. Dodaj pliki: `correct.mp3` i `wrong.mp3`
3. Zaktualizuj funkcję `play_sound()`:

```python
def play_sound(self, sound_type):
    try:
        sound = pygame.mixer.Sound(f"sounds/{sound_type}.mp3")
        sound.play()
    except:
        pass
```

## 👨‍👩‍👧‍👦 Dla Rodziców / For Parents

Ta gra jest zaprojektowana aby:
- Być bezpieczną dla dzieci (bez reklam, bez internetu)
- Wspierać naukę dwujęzyczną
- Dostarczać pozytywne wzmocnienia
- Być prostą i intuicyjną w obsłudze

## 🐛 Znane Problemy / Known Issues

- Brak plików dźwiękowych (opcjonalna funkcja)
- Wymaga zainstalowania pygame

## 📄 Licencja / License

Ten projekt jest dostępny na licencji MIT.

## 🤝 Wkład / Contributing

Sugestie i ulepszenia są mile widziane!

---

**Miłej Zabawy i Nauki! / Have Fun Learning!** 🌈🎉
