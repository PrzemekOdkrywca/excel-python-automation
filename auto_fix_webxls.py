#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_fix_webxls.py (v3)
-------------------------------------------------
Naprawia pliki z folderu skryptu, które *udają* Excela (np. HTML zapisany jako .xls)
i konwertuje je do prawdziwego XLS (Excel 97–2003, FileFormat=56).

Skanuje TYLKO bieżący folder (gdzie leży skrypt) i bierze pliki:
- *.xls, *.html, *.htm, *.web
- pliki bez rozszerzenia

Dla każdego pliku wykrywa format po nagłówku treści:
- OLE2  -> to prawdziwy XLS (pomijany, chyba że rozszerzenie nie .xls, wtedy tworzy kopię .xls)
- ZIP   -> to XLSX/ZIP (konwertuje do .xls)
- HTML  -> to strona WWW (konwertuje do .xls)
- CSV/tekst -> konwertuje do .xls
- nieznany -> próbuje przez Excel/LibreOffice/pandas

Kolejność prób konwersji: Excel COM -> LibreOffice -> pandas
Na końcu wypisuje: gotowe
"""
import os
import subprocess
from pathlib import Path
import sys
import csv
from io import StringIO
import shutil

SCRIPT_DIR = Path(__file__).resolve().parent

OLE_HEADER = bytes.fromhex("D0 CF 11 E0 A1 B1 1A E1")
ZIP_HEADER = b"PK\x03\x04"

def read_head(path: Path, n=4096):
    try:
        with open(path, "rb") as f:
            return f.read(n)
    except Exception:
        return b""

def is_html(head: bytes) -> bool:
    sample = head.lstrip().lower()
    return sample.startswith(b"<!doctype") or sample.startswith(b"<html")

def is_text_like(head: bytes) -> bool:
    try:
        txt = head.decode("utf-8", errors="ignore")
        return any(t in txt for t in [";", ",", "\t", "|", "\n"])
    except Exception:
        return False

def detect_kind(path: Path):
    head = read_head(path, n=4096)
    if not head:
        return "unknown"
    if head.startswith(OLE_HEADER):
        return "ole"
    if head.startswith(ZIP_HEADER):
        return "zip"
    if is_html(head):
        return "html"
    if is_text_like(head):
        return "text"
    return "unknown"

def sniff_delimiter(sample_bytes: bytes):
    try:
        sample = sample_bytes.decode("utf-8", errors="ignore")
        dialect = csv.Sniffer().sniff(sample, delimiters=";,|\t")
        return dialect.delimiter
    except Exception:
        return ";"

def convert_with_excel(src: Path, dst: Path):
    try:
        import win32com.client as win32
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.DisplayAlerts = False
        excel.Visible = False
        wb = excel.Workbooks.Open(str(src))
        wb.SaveAs(str(dst), FileFormat=56)  # .xls (Excel 97-2003)
        wb.Close(SaveChanges=False)
        excel.Quit()
        return True, "excel"
    except Exception as e:
        return False, f"Excel COM error: {e}"

def convert_with_libreoffice(src: Path, dst: Path):
    try:
        outdir = dst.parent
        cmd = ["soffice", "--headless", "--convert-to", "xls", "--outdir", str(outdir), str(src)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            return False, f"LibreOffice error: {res.stderr.strip()}"
        produced = outdir / (src.stem + ".xls")
        if produced.exists() and produced != dst:
            try:
                if dst.exists():
                    dst.unlink()
                produced.rename(dst)
            except Exception:
                pass
        return dst.exists(), "libreoffice"
    except FileNotFoundError:
        return False, "LibreOffice (soffice) not found on PATH"
    except Exception as e:
        return False, f"LibreOffice error: {e}"

def convert_with_pandas(src: Path, dst: Path, kind_hint: str):
    try:
        import pandas as pd
        if kind_hint == "html":
            # Spróbuj wyciągnąć pierwszą tabelę z HTML
            tables = pd.read_html(str(src))
            if len(tables) == 0:
                return False, "brak tabel w HTML"
            with pd.ExcelWriter(dst, engine="xlwt") as writer:
                for i, t in enumerate(tables, start=1):
                    sheet = f"Tabela{i}" if i > 1 else "Arkusz1"
                    t.to_excel(writer, index=False, sheet_name=sheet)
            return True, "pandas-html"
        elif kind_hint in ("zip", "ole"):
            # Spróbuj odczytać jako Excel (xls/xlsx)
            df = pd.read_excel(src, engine=None)
            with pd.ExcelWriter(dst, engine="xlwt") as writer:
                df.to_excel(writer, index=False, sheet_name="Arkusz1")
            return True, "pandas-excel"
        else:
            # CSV/tekst/nieznany
            try:
                df = pd.read_excel(src, engine=None)
            except Exception:
                raw = src.read_bytes()
                delim = sniff_delimiter(raw)
                df = pd.read_csv(StringIO(raw.decode("utf-8", errors="ignore")), delimiter=delim)
            with pd.ExcelWriter(dst, engine="xlwt") as writer:
                df.to_excel(writer, index=False, sheet_name="Arkusz1")
            return True, "pandas"
    except Exception as e:
        return False, f"pandas error: {e}"

def ensure_xls_copy_if_needed(src: Path):
    """Jeśli to prawdziwy XLS (OLE) a brak rozszerzenia .xls, zrób kopię .xls."""
    if src.suffix.lower() == ".xls":
        return False, "already-xls"
    kind = detect_kind(src)
    if kind == "ole":
        dst = src.with_suffix(".xls")
        try:
            if dst.exists():
                dst.unlink()
            shutil.copy2(src, dst)
            return True, "copy-ole->xls"
        except Exception as e:
            return False, f"copy error: {e}"
    return False, f"kind={kind}"

def convert_one(src: Path):
    kind = detect_kind(src)
    dst = src.with_suffix(".xls")

    # Jeśli to prawdziwy XLS i już ma .xls -> pomiń
    if kind == "ole" and src.suffix.lower() == ".xls":
        return ("skip", src.name, "prawdziwy XLS (pomijam)")

    # Jeśli to prawdziwy XLS ale bez .xls -> tylko dodaj rozszerzenie (kopia)
    if kind == "ole" and src.suffix.lower() != ".xls":
        ok, info = ensure_xls_copy_if_needed(src)
        return ("ok" if ok else "fail", src.name, info)

    # Konwersja (html, zip/xlsx, text, unknown)
    # 1) Excel COM
    ok, info = convert_with_excel(src, dst)
    if ok:
        return ("ok", src.name, info)

    # 2) LibreOffice
    ok, info = convert_with_libreoffice(src, dst)
    if ok:
        return ("ok", src.name, info)

    # 3) pandas (z podpowiedzią formatu)
    ok, info = convert_with_pandas(src, dst, kind)
    if ok:
        return ("ok", src.name, info)

    return ("fail", src.name, info)

def main():
    # Kandydaci: *.xls, *.html, *.htm, *.web, brak rozszerzenia
    candidates = []
    for p in SCRIPT_DIR.iterdir():
        if not p.is_file():
            continue
        suf = p.suffix.lower()
        if suf in (".xls", ".html", ".htm", ".web") or suf == "":
            candidates.append(p)

    if not candidates:
        print("Brak plików *.xls/*.html/*.htm/*.web lub plików bez rozszerzenia w folderze skryptu:", SCRIPT_DIR)
        print("gotowe")
        return

    for f in sorted(candidates):
        status, name, info = convert_one(f)
        print(f"[{status}] {name} -> {info}")

    print("gotowe")

if __name__ == "__main__":
    main()
