"""
repara_windows.py — Repară căutarea Windows și scurtăturile din meniul Start
Rulează ca Administrator!
Utilizare: click dreapta -> Run as Administrator -> python repara_windows.py
"""

import os
import sys
import subprocess
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

def este_administrator():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def pas(mesaj):
    print(f"\n  {C.CYAN}{C.BOLD}▶ {mesaj}{C.RESET}")

def ok(mesaj):
    print(f"  {C.GREEN}✔ {mesaj}{C.RESET}")

def err(mesaj):
    print(f"  {C.RED}✖ {mesaj}{C.RESET}")

def run(cmd, shell=True):
    try:
        subprocess.run(cmd, shell=shell, capture_output=True, timeout=60)
        return True
    except Exception:
        return False

def repara_cautare_windows():
    """Resetează și reindexează căutarea Windows."""
    pas("Opresc serviciul de căutare Windows...")
    run("net stop WSearch /y")
    time.sleep(2)
    ok("Serviciu oprit.")

    pas("Șterg indexul vechi de căutare...")
    index_path = Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData")) / "Microsoft" / "Search" / "Data"
    if index_path.exists():
        run(f'rmdir /s /q "{index_path}"')
        ok("Index vechi șters.")
    else:
        ok("Index nu a existat, trecem mai departe.")

    pas("Pornesc din nou serviciul de căutare...")
    run("net start WSearch")
    time.sleep(2)
    ok("Serviciu pornit — Windows va reindexa tot automat.")

def repara_shortcut(nume, exe_path, shortcut_name):
    """Creează o scurtătură în meniul Start."""
    start_menu = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    shortcut_path = start_menu / f"{shortcut_name}.lnk"
    exe = Path(exe_path)

    if not exe.exists():
        err(f"{nume} nu a fost găsit la: {exe_path}")
        return False

    try:
        # Folosim PowerShell pentru a crea shortcut-ul
        ps_cmd = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{exe}"
$Shortcut.Save()
'''
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=30)
        ok(f"Scurtătură creată pentru {nume}")
        return True
    except Exception as e:
        err(f"Nu am putut crea scurtătura pentru {nume}: {e}")
        return False

def gaseste_programe_comune():
    """Găsește programele comune instalate și le recreează scurtăturile."""
    local_programs = Path(os.environ["LOCALAPPDATA"]) / "Programs"
    program_files = Path("C:\\Program Files")
    program_files_x86 = Path("C:\\Program Files (x86)")

    # Lista de programe cunoscute de căutat
    programe = [
        {
            "nume": "Visual Studio Code",
            "cai_posibile": [
                local_programs / "Microsoft VS Code" / "Code.exe",
                program_files / "Microsoft VS Code" / "Code.exe",
            ],
            "shortcut": "Visual Studio Code"
        },
        {
            "nume": "Google Chrome",
            "cai_posibile": [
                Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "Application" / "chrome.exe",
                program_files / "Google" / "Chrome" / "Application" / "chrome.exe",
            ],
            "shortcut": "Google Chrome"
        },
        {
            "nume": "Mozilla Firefox",
            "cai_posibile": [
                program_files / "Mozilla Firefox" / "firefox.exe",
                program_files_x86 / "Mozilla Firefox" / "firefox.exe",
            ],
            "shortcut": "Mozilla Firefox"
        },
        {
            "nume": "Brave Browser",
            "cai_posibile": [
                Path(os.environ["LOCALAPPDATA"]) / "BraveSoftware" / "Brave-Browser" / "Application" / "brave.exe",
            ],
            "shortcut": "Brave Browser"
        },
        {
            "nume": "Discord",
            "cai_posibile": [
                Path(os.environ["LOCALAPPDATA"]) / "Discord" / "app-*" / "Discord.exe",
                Path(os.environ["LOCALAPPDATA"]) / "Discord" / "Discord.exe",
            ],
            "shortcut": "Discord"
        },
        {
            "nume": "Spotify",
            "cai_posibile": [
                Path(os.environ["APPDATA"]) / "Spotify" / "Spotify.exe",
            ],
            "shortcut": "Spotify"
        },
        {
            "nume": "Steam",
            "cai_posibile": [
                program_files_x86 / "Steam" / "steam.exe",
                program_files / "Steam" / "steam.exe",
            ],
            "shortcut": "Steam"
        },
        {
            "nume": "Python",
            "cai_posibile": [
                Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Python" / "Python314" / "python.exe",
                Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Python" / "Python313" / "python.exe",
                Path(os.environ["LOCALAPPDATA"]) / "Programs" / "Python" / "Python312" / "python.exe",
            ],
            "shortcut": "Python"
        },
        {
            "nume": "VLC Media Player",
            "cai_posibile": [
                program_files / "VideoLAN" / "VLC" / "vlc.exe",
                program_files_x86 / "VideoLAN" / "VLC" / "vlc.exe",
            ],
            "shortcut": "VLC Media Player"
        },
        {
            "nume": "7-Zip",
            "cai_posibile": [
                program_files / "7-Zip" / "7zFM.exe",
                program_files_x86 / "7-Zip" / "7zFM.exe",
            ],
            "shortcut": "7-Zip File Manager"
        },
        {
            "nume": "Notepad++",
            "cai_posibile": [
                program_files / "Notepad++" / "notepad++.exe",
                program_files_x86 / "Notepad++" / "notepad++.exe",
            ],
            "shortcut": "Notepad++"
        },
        {
            "nume": "WhatsApp",
            "cai_posibile": [
                Path(os.environ["LOCALAPPDATA"]) / "WhatsApp" / "WhatsApp.exe",
            ],
            "shortcut": "WhatsApp"
        },
        {
            "nume": "Zoom",
            "cai_posibile": [
                Path(os.environ["APPDATA"]) / "Zoom" / "bin" / "Zoom.exe",
            ],
            "shortcut": "Zoom"
        },
    ]

    gasite = 0
    for prog in programe:
        for cale in prog["cai_posibile"]:
            # Suport pentru wildcard (Discord app-*)
            cale_str = str(cale)
            if "*" in cale_str:
                parent = cale.parent.parent
                pattern = cale.parent.name
                try:
                    matches = list(parent.glob(f"{pattern}/{cale.name}"))
                    if matches:
                        cale = matches[0]
                    else:
                        continue
                except Exception:
                    continue

            if Path(cale).exists():
                if repara_shortcut(prog["nume"], cale, prog["shortcut"]):
                    gasite += 1
                break

    return gasite

def repara_asocieri_fisiere():
    """Resetează asocierile de fișiere comune."""
    pas("Repar asocierile de fișiere...")
    # Resetează icoanele și asocierile
    run("ie4uinit.exe -show")
    run("assoc .py=Python.File 2>nul")
    ok("Asocieri reparate.")

def rebuildeaza_icon_cache():
    """Șterge cache-ul de iconițe ca să apară corect."""
    pas("Rebuildeaz cache iconițe...")
    cache = Path(os.environ["LOCALAPPDATA"]) / "IconCache.db"
    try:
        if cache.exists():
            run(f'del /f /q "{cache}"')
        run("ie4uinit.exe -show")
        ok("Cache iconițe rebuildat.")
    except Exception:
        err("Nu am putut rebuilda cache-ul de iconițe.")

def main():
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   🔧 REPARARE WINDOWS — Căutare + Meniu Start{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

    # Verifică administrator
    if not este_administrator():
        print(f"  {C.RED}{C.BOLD}⚠️  Trebuie să rulezi ca Administrator!{C.RESET}")
        print(f"\n  {C.YELLOW}Cum:{C.RESET}")
        print(f"  1. Caută 'PowerShell' în meniul Start")
        print(f"  2. Click dreapta → 'Run as Administrator'")
        print(f"  3. Scrie: python d:\\Python\\repara_windows.py\n")
        input("  Apasă Enter pentru a ieși...")
        sys.exit(1)

    print(f"  {C.GREEN}✔ Rulezi ca Administrator.{C.RESET}\n")

    # PASUL 1: Scurtături meniu Start
    pas("Caut și recreez scurtăturile programelor în Meniu Start...")
    gasite = gaseste_programe_comune()
    ok(f"{gasite} program(e) găsite și adăugate în Meniu Start.")

    # PASUL 2: Cache iconițe
    rebuildeaza_icon_cache()

    # PASUL 3: Resetare căutare Windows
    pas("Resetez indexul de căutare Windows...")
    repara_cautare_windows()

    # PASUL 4: Asocieri fișiere
    repara_asocieri_fisiere()

    # PASUL 5: Refresh Explorer
    pas("Reîmprospătez Windows Explorer...")
    run("taskkill /f /im explorer.exe")
    time.sleep(2)
    run("start explorer.exe")
    ok("Explorer reîmprospătat.")

    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}  ✅ Gata! Totul a fost reparat.{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"\n  {C.YELLOW}⚠️  Windows va reindexa programele în fundal.")
    print(f"     Poate dura 5-10 minute până apar toate în căutare.{C.RESET}\n")
    input("  Apasă Enter pentru a ieși...")

if __name__ == "__main__":
    main()
