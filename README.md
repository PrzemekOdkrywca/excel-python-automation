
# auto_fix_webxls.py

Ten skrypt automatycznie naprawia pliki, które udają pliki Excela (np. pliki HTML zapisane jako .xls) i konwertuje je do prawdziwego formatu XLS (Excel 97–2003).

## Co robi skrypt?
- Skanuje bieżący folder (tam, gdzie znajduje się skrypt) i wyszukuje pliki:
	- z rozszerzeniem: `.xls`, `.html`, `.htm`, `.web`
	- bez rozszerzenia
- Dla każdego pliku wykrywa jego format na podstawie nagłówka:
	- OLE2  → prawdziwy XLS (pomijany, chyba że nie ma rozszerzenia .xls, wtedy tworzy kopię z tym rozszerzeniem)
	- ZIP   → XLSX/ZIP (konwertuje do .xls)
	- HTML  → strona WWW (konwertuje do .xls)
	- CSV/tekst → konwertuje do .xls
	- nieznany → próbuje konwersji przez Excel/LibreOffice/pandas
- Kolejność prób konwersji: Excel COM → LibreOffice → pandas
- Na końcu wypisuje podsumowanie konwersji.

## Wymagania
- Python 3.x
- Biblioteki: `pandas`, `xlwt`, `win32com` (opcjonalnie), LibreOffice (opcjonalnie)

## Uruchomienie
1. Umieść skrypt w folderze z plikami do naprawy.
2. Uruchom w terminalu:
	 ```bash
	 python auto_fix_webxls.py
	 ```
3. Skrypt utworzy prawdziwe pliki `.xls` w tym samym folderze.

## Autor
OdkrywcaAI, 2026

## Licencja
MIT License

# Excel + Python Automation

Zestaw narzędzi do automatyzacji powtarzalnych zadań biznesowych z użyciem Excela i Pythona.

Projekt pokazuje praktyczne podejście do usprawniania pracy operacyjnej:
mniej ręcznych czynności, mniej błędów i realna oszczędność czasu.

---

## 🔴 Problem

W wielu firmach codzienna praca opiera się na:
- ręcznej obróbce plików Excel,
- powtarzalnym czyszczeniu danych,
- konwersjach plików (HTML / CSV / XLS),
- monotonnych czynnościach wykonywanych według tego samego schematu.

Procesy te są:
- czasochłonne,
- podatne na błędy,
- obciążające psychicznie pracowników.

---

## 🟢 Rozwiązanie

Automatyzacje napisane w Pythonie, współpracujące z Excelem, które:
- wykonują zadania „na klik”,
- nie wymagają wiedzy technicznej od użytkownika końcowego,
- działają lokalnie (bez chmury i zewnętrznych usług),
- mogą być uruchamiane przez proste pliki `.bat` / `.vbs`.

Każde narzędzie rozwiązuje **konkretny problem biznesowy**, a nie abstrakcyjny przykład.

---

## 📈 Efekt

W zależności od przypadku:
- skrócenie czasu pracy z kilkudziesięciu minut do kilku sekund,
- eliminacja błędów ręcznych,
- większa powtarzalność i przewidywalność procesu,
- odciążenie pracowników od monotonnych zadań.

---

## 🧰 Technologie

- Python
- Excel (COM / pliki XLS, XLSX)
- pandas
- pywin32
- skrypty `.bat` / `.vbs`

---

## ▶️ Jak korzystać

Każde narzędzie w repozytorium:
- posiada własny opis,
- zawiera instrukcję uruchomienia,
- jest przygotowane z myślą o użytkownikach nietechnicznych.

Repozytorium będzie rozwijane o kolejne przykłady automatyzacji.


## 🎮 Color Learning Game – uruchamianie

Aby uruchomić grę bez problemów z PowerShellem:

1. Otwórz terminal cmd (nie PowerShell) i wpisz:
	.\.venv\Scripts\activate.bat
	python color_learning_game.py

2. Lub bez aktywacji środowiska:
	.\.venv\Scripts\python.exe color_learning_game.py

Więcej szczegółów znajdziesz w pliku [README_GAME_URUCHOMIENIE.md](README_GAME_URUCHOMIENIE.md).

---
## 📂 Przykładowe automatyzacje

Repozytorium będzie stopniowo uzupełniane o konkretne przypadki, m.in.:
- automatyczna konwersja plików HTML / CSV do Excela,
- czyszczenie i standaryzacja danych handlowych,
- masowe operacje na plikach Excel,
- proste narzędzia uruchamiane „na klik” przez użytkownika biznesowego.
---

## 👤 Autor

Przemek Sawicki  
Projekt: **Odkrywca AI**

> Automatyzuję to, co powtarzalne – by odzyskać czas.
