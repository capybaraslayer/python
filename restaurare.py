"""
restaurare.py — Restaurează toate fișierele mutate de organizator înapoi la locul lor
Utilizare: python restaurare.py
"""

import os
import shutil
import sys
import string
import time
from pathlib import Path

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    CYAN    = "\033[96m"
    GRAY    = "\033[90m"

def get_discuri():
    discuri = []
    if sys.platform == "win32":
        for litera in string.ascii_uppercase:
            disc = Path(f"{litera}:\\")
            if disc.exists():
                discuri.append(disc)
    else:
        discuri = [Path("/")]
    return discuri

def gaseste_foldere_organizat(discuri: list) -> list:
    """Găsește toate folderele _Organizat de pe discuri."""
    foldere = []
    print(f"\n  {C.CYAN}Caut foldere '_Organizat' pe toate discurile...{C.RESET}\n")

    for disc in discuri:
        try:
            for root, dirs, files in os.walk(disc):
                root_path = Path(root)
                # Sare foldere sistem
                dirs[:] = [d for d in dirs if d.lower() not in {
                    "windows", "program files", "program files (x86)",
                    "programdata", "system volume information", "$recycle.bin"
                } and not d.startswith("$")]

                if root_path.name == "_Organizat":
                    foldere.append(root_path)
                    print(f"  {C.GREEN}[GĂSIT]{C.RESET} {root_path}")
        except Exception:
            continue

    return foldere

def restaureaza(foldere_organizat: list, dry: bool) -> dict:
    """Mută fișierele din _Organizat înapoi în folderul părinte."""
    stats = {"restaurate": 0, "sarite": 0, "erori": 0}

    for folder_org in foldere_organizat:
        # Folderul părinte al lui _Organizat = locația originală
        folder_original = folder_org.parent
        print(f"\n  {C.CYAN}Restaurez din: {folder_org}{C.RESET}")
        print(f"  {C.CYAN}Înapoi în:     {folder_original}{C.RESET}")
        print(f"  {'─'*56}")

        # Iterăm prin toate subfoldere de categorii din _Organizat
        try:
            categorii = [f for f in folder_org.iterdir() if f.is_dir()]
        except Exception:
            continue

        for categorie in categorii:
            try:
                fisiere = list(categorie.iterdir())
            except Exception:
                continue

            for fisier in fisiere:
                if not fisier.is_file():
                    continue

                dest = folder_original / fisier.name

                # Gestionăm coliziuni de nume
                if dest.exists():
                    stem, suffix, contor = fisier.stem, fisier.suffix, 1
                    while dest.exists():
                        dest = folder_original / f"{stem}_restaurat_{contor}{suffix}"
                        contor += 1

                try:
                    if dry:
                        print(f"  {C.GRAY}[SIM]{C.RESET}  {fisier.name[:50]:<52} → {folder_original}")
                    else:
                        shutil.move(str(fisier), str(dest))
                        print(f"  {C.GREEN}[OK]{C.RESET}   {fisier.name[:50]:<52} ✔")
                    stats["restaurate"] += 1
                except Exception as e:
                    print(f"  {C.RED}[ERR]{C.RESET}  {fisier.name[:50]:<52} — {e}")
                    stats["erori"] += 1

        # Șterge folderul _Organizat dacă e gol
        if not dry:
            try:
                shutil.rmtree(folder_org, ignore_errors=True)
                print(f"  {C.GRAY}  Folder _Organizat șters (era gol).{C.RESET}")
            except Exception:
                pass

    return stats

def main():
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   ↩️  RESTAURARE — Pune totul înapoi la loc{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

    discuri = get_discuri()
    foldere_organizat = gaseste_foldere_organizat(discuri)

    if not foldere_organizat:
        print(f"\n  {C.YELLOW}Nu s-au găsit foldere '_Organizat' pe niciun disc.{C.RESET}")
        print(f"  {C.YELLOW}Fie fișierele sunt deja la loc, fie organizatorul nu a rulat.{C.RESET}\n")
        return

    print(f"\n  {C.BOLD}Găsite {len(foldere_organizat)} folder(e) '_Organizat'.{C.RESET}")

    print(f"\n{C.BOLD}  Mod de execuție:{C.RESET}")
    print(f"  {C.YELLOW}[1]{C.RESET} SIMULARE — arată ce s-ar face, fără să mute nimic")
    print(f"  {C.YELLOW}[2]{C.RESET} REAL — restaurează efectiv toate fișierele\n")
    dry = input(f"  {C.BOLD}Alege (1/2): {C.RESET}").strip() != "2"

    if not dry:
        print(f"\n  {C.RED}{C.BOLD}⚠️  Toate fișierele vor fi mutate înapoi la locul original!{C.RESET}")
        confirmare = input(f"  {C.BOLD}Ești sigur? Scrie DA: {C.RESET}").strip().upper()
        if confirmare != "DA":
            print(f"\n  {C.YELLOW}Anulat.{C.RESET}\n")
            return

    start = time.time()
    stats = restaureaza(foldere_organizat, dry)
    elapsed = time.time() - start

    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   RAPORT FINAL{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")
    print(f"  Fișiere restaurate : {C.GREEN}{stats['restaurate']}{C.RESET}")
    print(f"  Erori              : {C.RED}{stats['erori']}{C.RESET}")
    print(f"  Timp               : {elapsed:.1f} secunde")

    if dry:
        print(f"\n  {C.YELLOW}⚠️  Mod simulare — niciun fișier nu a fost mutat.")
        print(f"     Rulează din nou și alege 2 (REAL) pentru a restaura efectiv.{C.RESET}")
    else:
        print(f"\n  {C.GREEN}{C.BOLD}✅ Gata! Toate fișierele sunt înapoi la locul lor.{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

if __name__ == "__main__":
    main()
