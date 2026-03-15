"""
configureaza_vscode.py — Configurează VS Code perfect pentru programare
Utilizare: python configureaza_vscode.py
"""

import subprocess
import json
import os
import sys
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

EXTENSII = [
    ("Continue.continue",                       "🤖 Continue — AI gratuit"),
    ("Codeium.codeium",                         "🤖 Codeium — AI autocomplete 100% gratuit"),
    ("ms-python.python",                        "🐍 Python — suport complet"),
    ("ms-python.pylint",                        "🐍 Pylint — detectare erori"),
    ("ms-python.black-formatter",               "🐍 Black — formatare automată Python"),
    ("eamodio.gitlens",                         "🔀 GitLens — Git avansat"),
    ("mhutchie.git-graph",                      "🔀 Git Graph — vizualizare ramuri"),
    ("dracula-theme.theme-dracula",             "🎨 Dracula — temă întunecată"),
    ("PKief.material-icon-theme",               "🎨 Material Icons — iconițe frumoase"),
    ("esbenp.prettier-vscode",                  "✨ Prettier — formatare automată"),
    ("usernamehw.errorlens",                    "✨ Error Lens — erori pe linie"),
    ("streetsidesoftware.code-spell-checker",   "✨ Spell Checker"),
    ("christian-kohler.path-intellisense",      "✨ Path Intellisense"),
    ("ritwickdey.LiveServer",                   "🌐 Live Server — HTML live"),
    ("formulahendry.auto-rename-tag",           "🏷️  Auto Rename Tag"),
    ("oderwat.indent-rainbow",                  "🌈 Indent Rainbow"),
    ("wayou.vscode-todo-highlight",             "📌 TODO Highlight"),
    ("Gruntfuggly.todo-tree",                   "📌 Todo Tree"),
    ("alefragnani.Bookmarks",                   "🔖 Bookmarks"),
    ("yzhang.markdown-all-in-one",              "📝 Markdown All in One"),
]

SETARI = {
    "workbench.colorTheme": "Dracula",
    "workbench.iconTheme": "material-icon-theme",
    "workbench.startupEditor": "none",
    "workbench.editor.enablePreview": False,
    "editor.fontFamily": "'Cascadia Code', 'Fira Code', 'JetBrains Mono', Consolas, monospace",
    "editor.fontLigatures": True,
    "editor.fontSize": 14,
    "editor.lineHeight": 1.6,
    "editor.tabSize": 4,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": True,
    "editor.cursorBlinking": "smooth",
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.smoothScrolling": True,
    "editor.bracketPairColorization.enabled": True,
    "editor.guides.bracketPairs": True,
    "editor.formatOnSave": True,
    "editor.formatOnPaste": True,
    "editor.linkedEditing": True,
    "editor.rulers": [80, 120],
    "terminal.integrated.defaultProfile.windows": "Git Bash",
    "terminal.integrated.fontFamily": "'Cascadia Code', monospace",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.cursorBlinking": True,
    "terminal.integrated.smoothScrolling": True,
    "python.defaultInterpreterPath": "C:\\Users\\catal\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": True,
    },
    "git.enableSmartCommit": True,
    "git.confirmSync": False,
    "git.autofetch": True,
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "files.trimTrailingWhitespace": True,
    "files.insertFinalNewline": True,
    "explorer.confirmDelete": True,
    "explorer.confirmDragAndDrop": False,
    "breadcrumbs.enabled": True,
    "security.workspace.trust.untrustedFiles": "open",
    "prettier.singleQuote": True,
    "prettier.semi": True,
    "prettier.tabWidth": 4,
    "errorLens.enabledDiagnosticLevels": ["error", "warning", "info"],
}

KEYBINDINGS = [
    {"key": "ctrl+d", "command": "editor.action.copyLinesDownAction"},
    {"key": "ctrl+shift+k", "command": "editor.action.deleteLines"},
    {"key": "alt+up", "command": "editor.action.moveLinesUpAction"},
    {"key": "alt+down", "command": "editor.action.moveLinesDownAction"},
    {"key": "ctrl+shift+f", "command": "workbench.action.findInFiles"},
]


def gaseste_vscode() -> str:
    """Găsește calea spre Code.exe sau code.cmd."""
    local = Path(os.environ.get("LOCALAPPDATA", "C:\\Users\\catal\\AppData\\Local"))
    cai = [
        local / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
        local / "Programs" / "Microsoft VS Code" / "Code.exe",
        Path("C:\\Program Files\\Microsoft VS Code\\bin\\code.cmd"),
        Path("C:\\Program Files\\Microsoft VS Code\\Code.exe"),
        Path("C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"),
    ]
    for cale in cai:
        if cale.exists():
            return str(cale)
    return None


def instaleaza_extensie(vscode_cmd: str, ext_id: str, descriere: str) -> bool:
    try:
        result = subprocess.run(
            [vscode_cmd, "--install-extension", ext_id, "--force"],
            capture_output=True, text=True, timeout=90
        )
        if result.returncode == 0:
            print(f"  {C.GREEN}[OK]{C.RESET}  {descriere}")
            return True
        else:
            print(f"  {C.RED}[ERR]{C.RESET} {descriere}")
            return False
    except Exception as e:
        print(f"  {C.RED}[ERR]{C.RESET} {descriere} — {e}")
        return False


def salveaza_setari(setari: dict):
    cale = Path(os.environ["APPDATA"]) / "Code" / "User" / "settings.json"
    cale.parent.mkdir(parents=True, exist_ok=True)
    existente = {}
    if cale.exists():
        try:
            with open(cale, "r", encoding="utf-8") as f:
                existente = json.load(f)
        except Exception:
            pass
    existente.update(setari)
    with open(cale, "w", encoding="utf-8") as f:
        json.dump(existente, f, indent=4, ensure_ascii=False)
    print(f"  {C.GREEN}[OK]{C.RESET}  Setări salvate.")


def salveaza_keybindings(keybindings: list):
    cale = Path(os.environ["APPDATA"]) / "Code" / "User" / "keybindings.json"
    cale.parent.mkdir(parents=True, exist_ok=True)
    with open(cale, "w", encoding="utf-8") as f:
        json.dump(keybindings, f, indent=4, ensure_ascii=False)
    print(f"  {C.GREEN}[OK]{C.RESET}  Keybindings salvate.")


def configureaza_git_bash():
    cai_bash = [
        Path("C:\\Program Files\\Git\\bin\\bash.exe"),
        Path("C:\\Program Files (x86)\\Git\\bin\\bash.exe"),
    ]
    for bash in cai_bash:
        if bash.exists():
            SETARI["terminal.integrated.profiles.windows"] = {
                "Git Bash": {
                    "path": str(bash),
                    "args": ["--login", "-i"],
                    "icon": "terminal-bash"
                }
            }
            print(f"  {C.GREEN}[OK]{C.RESET}  Git Bash configurat: {bash}")
            return
    print(f"  {C.YELLOW}[SKIP]{C.RESET} Git Bash nu a fost găsit.")


def main():
    print(f"\n{C.BOLD}{C.CYAN}{'='*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   CONFIGURARE VS CODE — Setup Complet Programator{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'='*62}{C.RESET}\n")

    # Găsește VS Code
    vscode_cmd = gaseste_vscode()
    if not vscode_cmd:
        print(f"  {C.RED}VS Code nu a fost găsit!{C.RESET}")
        print(f"  {C.YELLOW}Reinstalează de la code.visualstudio.com{C.RESET}\n")
        input("  Apasă Enter pentru a ieși...")
        sys.exit(1)

    print(f"  {C.GREEN}VS Code gasit:{C.RESET} {vscode_cmd}\n")

    # PASUL 1: Extensii
    print(f"{C.BOLD}{C.CYAN}  PASUL 1 — Instalare {len(EXTENSII)} extensii{C.RESET}\n")

    instalate = 0
    for ext_id, descriere in EXTENSII:
        if instaleaza_extensie(vscode_cmd, ext_id, descriere):
            instalate += 1
        time.sleep(0.3)

    print(f"\n  {C.GREEN}{instalate}/{len(EXTENSII)} extensii instalate.{C.RESET}")

    # PASUL 2: Git Bash
    print(f"\n{C.BOLD}{C.CYAN}  PASUL 2 — Git Bash terminal{C.RESET}\n")
    configureaza_git_bash()

    # PASUL 3: Setări
    print(f"\n{C.BOLD}{C.CYAN}  PASUL 3 — Setari{C.RESET}\n")
    salveaza_setari(SETARI)

    # PASUL 4: Keybindings
    print(f"\n{C.BOLD}{C.CYAN}  PASUL 4 — Scurtaturi tastatura{C.RESET}\n")
    salveaza_keybindings(KEYBINDINGS)

    # RAPORT FINAL
    print(f"\n{C.BOLD}{C.CYAN}{'='*62}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}  VS Code configurat perfect!{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'='*62}{C.RESET}\n")
    print(f"  AI gratuit — Codeium + Continue")
    print(f"  Tema Dracula + iconite Material")
    print(f"  GitLens + Git Graph")
    print(f"  Python + formatare automata Black")
    print(f"  Error Lens — erori vizibile pe linie")
    print(f"  Salvare automata la 1 secunda")
    print(f"  Git Bash terminal")
    print(f"\n  {C.YELLOW}Inchide si redeschide VS Code pentru a aplica tot!{C.RESET}\n")

    input("  Apasa Enter pentru a iesi...")


if __name__ == "__main__":
    main()
