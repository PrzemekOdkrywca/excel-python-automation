# Instrukcja uruchamiania gry Color Learning Game

Aby uniknąć problemów z polityką uruchamiania skryptów PowerShell (błąd przy Activate.ps1), możesz uruchomić projekt na dwa sposoby:

## 1. Aktywacja środowiska w cmd (zalecane)
1. Otwórz terminal cmd (nie PowerShell).
2. Wpisz:

    .\.venv\Scripts\activate.bat

3. Następnie uruchom grę:

    python color_learning_game.py

## 2. Uruchomienie bez aktywacji środowiska
1. Wpisz w terminalu (cmd lub PowerShell):

    .\.venv\Scripts\python.exe color_learning_game.py

To uruchomi grę bez konieczności aktywowania środowiska.

---

Jeśli chcesz korzystać z PowerShell i aktywować środowisko, musisz zmienić politykę uruchamiania skryptów (tylko dla tej sesji):

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Następnie:

    .\.venv\Scripts\Activate.ps1

---

W razie pytań lub problemów – sprawdź dokumentację lub skontaktuj się z autorem.
