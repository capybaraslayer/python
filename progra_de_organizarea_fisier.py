"""
organizer_pc.py — Organizator complet pentru PC
Scanează toate locațiile importante și organizează fișierele în foldere specifice.
Utilizare: python organizer_pc.py
"""

import os
import shutil
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# ─── Culori pentru terminal ────────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    CYAN   = "\033[96m"
    BLUE   = "\033[94m"
    GRAY   = "\033[90m"

# ─── Locații de scanat pe PC ───────────────────────────────────────────────────
def get_locatii_pc() -> dict:
    """Returnează locațiile principale de pe PC în funcție de sistemul de operare."""
    home = Path.home()

    if sys.platform == "win32":
        locatii = {
            "Desktop":      home / "Desktop",
            "Downloads":    home / "Downloads",
            "Documents":    home / "Documents",
            "Pictures":     home / "Pictures",
            "Videos":       home / "Videos",
            "Music":        home / "Music",
        }
        # Adăugăm OneDrive dacă există
        onedrive = home / "OneDrive"
        if onedrive.exists():
            locatii["OneDrive"] = onedrive
    else:
        # macOS / Linux
        locatii = {
            "Desktop":      home / "Desktop",
            "Downloads":    home / "Downloads",
            "Documents":    home / "Documents",
            "Pictures":     home / "Pictures",
            "Videos":       home / "Videos",
            "Music":        home / "Music",
        }

    # Filtrăm doar cele care există
    return {nume: cale for nume, cale in locatii.items() if cale.exists()}


# ─── Reguli de organizare ──────────────────────────────────────────────────────
CATEGORII = {
    "Documente": [
        ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt",
        ".xls", ".xlsx", ".ods", ".csv",
        ".ppt", ".pptx", ".odp",
        ".md", ".tex", ".epub", ".pages", ".numbers", ".key",
    ],
    "Imagini": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".webp", ".svg", ".ico", ".heic", ".heif", ".raw", ".cr2",
        ".nef", ".arw",
    ],
    "Video": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpeg", ".mpg", ".3gp", ".ts",
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ".opus", ".aiff", ".mid", ".midi",
    ],
    "Python": [
        ".py", ".pyw", ".ipynb", ".pyx",
    ],
    "Cod_Sursa": [
        ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss",
        ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rs",
        ".rb", ".php", ".swift", ".kt", ".r", ".m", ".sh", ".bat",
        ".ps1", ".lua", ".dart",
    ],
    "Date_Config": [
        ".sql", ".db", ".sqlite", ".sqlite3", ".json", ".xml",
        ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
    ],
    "Arhive": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tar.gz", ".tar.bz2", ".iso", ".dmg",
    ],
    "Executabile_Instalare": [
        ".exe", ".msi", ".deb", ".rpm", ".apk", ".app", ".pkg",
    ],
    "Fonturi": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ],
    "Design_3D": [
        ".psd", ".ai", ".xd", ".fig", ".sketch", ".blend",
        ".obj", ".fbx", ".stl", ".dxf",
    ],
    "Altele": [],
}

# Dicționar invers: extensie → categorie
EXTENSIE_LA_CATEGORIE = {}
for _cat, _exts in CATEGORII.items():
    for _ext in _exts:
        EXTENSIE_LA_CATEGORIE[_ext.lower()] = _cat

# Fișiere sistem de ignorat complet
IGNORAT_NUME = {
    "desktop.ini", "thumbs.db", ".ds_store", ".localized",
    "ntuser.dat", "ntuser.ini", "bootmgr", "pagefile.sys",
    "hiberfil.sys", "swapfile.sys",
}
IGNORAT_PREFIX = {"~$", "._"}  # fișiere temporare Office / macOS


# ─── Funcții de bază ───────────────────────────────────────────────────────────

def gaseste_categorie(fisier: Path) -> str:
    sufixe = "".join(fisier.suffixes).lower()
    if sufixe in EXTENSIE_LA_CATEGORIE:
        return EXTENSIE_LA_CATEGORIE[sufixe]
    ext = fisier.suffix.lower()
    return EXTENSIE_LA_CATEGORIE.get(ext, "Altele")


def trebuie_ignorat(fisier: Path) -> bool:
    nume = fisier.name.lower()
    if nume in IGNORAT_NUME:
        return True
    for prefix in IGNORAT_PREFIX:
        if nume.startswith(prefix):
            return True
    return False


def muta_fisier(sursa: Path, dest_folder: Path) -> Path:
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest = dest_folder / sursa.name
    if dest.exists() and dest.resolve() != sursa.resolve():
        stem, suffix, contor = sursa.stem, sursa.suffix, 1
        while dest.exists():
            dest = dest_folder / f"{stem}_{contor}{suffix}"
            contor += 1
    shutil.move(str(sursa), str(dest))
    return dest


def scaneaza_folder(folder: Path, recursiv: bool = False):
    """Generează fișierele dintr-un folder (opțional recursiv, fără subfoldere de categorii)."""
    if recursiv:
        for item in folder.rglob("*"):
            if item.is_file():
                yield item
    else:
        for item in folder.iterdir():
            if item.is_file():
                yield item


# ─── Interfața interactivă ─────────────────────────────────────────────────────

def afiseaza_header():
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   🗂  ORGANIZATOR COMPLET PC{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"   Data: {datetime.now().strftime('%d.%m.%Y  %H:%M:%S')}\n")


def alege_locatii(locatii: dict) -> dict:
    """Lasă utilizatorul să aleagă ce locații să organizeze."""
    print(f"{C.BOLD}   Locații detectate pe PC:{C.RESET}\n")
    lista = list(locatii.items())
    for i, (nume, cale) in enumerate(lista, 1):
        nr_fisiere = sum(1 for f in cale.iterdir() if f.is_file()) if cale.exists() else 0
        print(f"   {C.YELLOW}[{i}]{C.RESET} {nume:<20} {C.GRAY}{cale}  ({nr_fisiere} fișiere){C.RESET}")
    print(f"   {C.YELLOW}[A]{C.RESET} Toate locațiile de mai sus")
    print(f"   {C.YELLOW}[X]{C.RESET} Adaugă o cale personalizată\n")

    ales = input(f"   {C.BOLD}Alege (ex: 1 2 3 sau A): {C.RESET}").strip().upper()

    if ales == "A":
        return dict(lista)

    if ales == "X":
        cale_custom = input("   Introdu calea: ").strip()
        p = Path(cale_custom)
        if p.exists() and p.is_dir():
            return {"Custom": p}
        else:
            print(f"{C.RED}   Calea nu există!{C.RESET}")
            sys.exit(1)

    selectate = {}
    for nr in ales.split():
        try:
            idx = int(nr) - 1
            if 0 <= idx < len(lista):
                selectate[lista[idx][0]] = lista[idx][1]
        except ValueError:
            pass

    if not selectate:
        print(f"{C.RED}   Nicio selecție validă.{C.RESET}")
        sys.exit(1)

    return selectate


def alege_mod() -> tuple:
    """Returnează (recursiv, dry_run)."""
    print(f"\n{C.BOLD}   Mod de scanare:{C.RESET}")
    print(f"   {C.YELLOW}[1]{C.RESET} Doar fișierele din rădăcina fiecărui folder (recomandat)")
    print(f"   {C.YELLOW}[2]{C.RESET} Recursiv — inclusiv subfoldere\n")
    mod = input(f"   {C.BOLD}Alege (1/2): {C.RESET}").strip()
    recursiv = mod == "2"

    print(f"\n{C.BOLD}   Mod de execuție:{C.RESET}")
    print(f"   {C.YELLOW}[1]{C.RESET} REAL — mută efectiv fișierele")
    print(f"   {C.YELLOW}[2]{C.RESET} SIMULARE (dry-run) — arată ce s-ar face, fără să mute nimic\n")
    exec_mod = input(f"   {C.BOLD}Alege (1/2): {C.RESET}").strip()
    dry = exec_mod == "2"

    return recursiv, dry


# ─── Organizare propriu-zisă ───────────────────────────────────────────────────

def organizeaza_locatie(nume_loc: str, folder: Path, recursiv: bool, dry: bool) -> dict:
    """Organizează o singură locație și returnează statistici."""
    print(f"\n{C.BOLD}{C.BLUE}  📁 {nume_loc}{C.RESET}  {C.GRAY}{folder}{C.RESET}")
    print(f"  {'─'*58}")

    stats = {cat: 0 for cat in CATEGORII}
    stats["_total"] = 0
    stats["_sarite"] = 0
    stats["_erori"] = 0

    try:
        fisiere = list(scaneaza_folder(folder, recursiv))
    except PermissionError:
        print(f"  {C.RED}[ACCES REFUZAT]{C.RESET} Nu am permisiuni pentru acest folder.")
        return stats

    if not fisiere:
        print(f"  {C.GRAY}  (niciun fișier găsit){C.RESET}")
        return stats

    for fisier in fisiere:
        # Ignorăm fișierele sistem
        if trebuie_ignorat(fisier):
            stats["_sarite"] += 1
            continue

        # Ignorăm dacă e deja într-un subfolder de categorie al nostru
        if fisier.parent != folder:
            if fisier.parent.name in CATEGORII:
                stats["_sarite"] += 1
                continue

        categorie = gaseste_categorie(fisier)
        dest_folder = folder / categorie

        try:
            if dry:
                print(f"  {C.GRAY}[SIM]{C.RESET}  {fisier.name[:45]:<46} → {categorie}/")
            else:
                muta_fisier(fisier, dest_folder)
                print(f"  {C.GREEN}[OK]{C.RESET}   {fisier.name[:45]:<46} → {categorie}/")
            stats[categorie] += 1
            stats["_total"] += 1
        except Exception as e:
            print(f"  {C.RED}[ERR]{C.RESET}  {fisier.name[:45]:<46} — {e}")
            stats["_erori"] += 1

    return stats


# ─── Raport final ──────────────────────────────────────────────────────────────

def afiseaza_raport(toate_stats: dict):
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   RAPORT FINAL{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

    total_global = 0
    categorii_globale = {cat: 0 for cat in CATEGORII}

    for loc, stats in toate_stats.items():
        t = stats.get("_total", 0)
        e = stats.get("_erori", 0)
        s = stats.get("_sarite", 0)
        print(f"  {C.BOLD}{loc:<20}{C.RESET}  {t} mutat(e)  |  {s} sărit(e)  |  {e} erori")
        total_global += t
        for cat in CATEGORII:
            categorii_globale[cat] += stats.get(cat, 0)

    print(f"\n  {C.BOLD}{'─'*40}{C.RESET}")
    print(f"  {C.BOLD}Total fișiere mutate: {total_global}{C.RESET}\n")
    print(f"  {C.BOLD}Detalii pe categorii:{C.RESET}")
    for cat, nr in sorted(categorii_globale.items()):
        if nr > 0:
            bara = "█" * min(nr, 30)
            print(f"  {cat:<28} {C.YELLOW}{bara}{C.RESET} {nr}")

    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}  ✅ Gata! Toate fișierele au fost organizate.{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")


# ─── Salvare jurnal ────────────────────────────────────────────────────────────

def salveaza_jurnal(toate_stats: dict):
    jurnal = {
        "data": datetime.now().isoformat(),
        "statistici": {loc: {k: v for k, v in s.items()} for loc, s in toate_stats.items()}
    }
    cale_jurnal = Path.home() / "organizer_jurnal.json"
    with open(cale_jurnal, "w", encoding="utf-8") as f:
        json.dump(jurnal, f, ensure_ascii=False, indent=2)
    print(f"  {C.GRAY}Jurnal salvat: {cale_jurnal}{C.RESET}\n")


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    afiseaza_header()

    locatii_pc = get_locatii_pc()
    if not locatii_pc:
        print(f"{C.RED}  Nu s-au găsit locații standard pe acest PC.{C.RESET}")
        sys.exit(1)

    locatii_alese = alege_locatii(locatii_pc)
    recursiv, dry = alege_mod()

    if not dry:
        print(f"\n  {C.RED}{C.BOLD}⚠️  ATENȚIE: Fișierele vor fi MUTATE efectiv!{C.RESET}")
        confirmare = input(f"  {C.BOLD}Ești sigur? Scrie DA pentru a continua: {C.RESET}").strip().upper()
        if confirmare != "DA":
            print(f"\n  {C.YELLOW}Anulat. Niciun fișier nu a fost mutat.{C.RESET}\n")
            sys.exit(0)

    toate_stats = {}
    start = time.time()

    for nume, cale in locatii_alese.items():
        stats = organizeaza_locatie(nume, cale, recursiv, dry)
        toate_stats[nume] = stats

    elapsed = time.time() - start
    print(f"\n  {C.GRAY}Timp total: {elapsed:.1f} secunde{C.RESET}")

    afiseaza_raport(toate_stats)

    if not dry:
        salveaza_jurnal(toate_stats)


if __name__ == "__main__":
    main()