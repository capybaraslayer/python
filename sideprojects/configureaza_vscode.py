"""
configureaza_vscode.py — Configurează VS Code perfect pentru programare
Instalează extensiile cele mai bune și configurează setările automat.
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
    MAGENTA = "\033[95m"

# ─── Extensii de instalat ──────────────────────────────────────────────────────
EXTENSII = [
    # AI - Completare cod GRATUIT
    ("Continue.continue",           "🤖 Continue — AI gratuit (folosește modele free)"),
    ("Codeium.codeium",             "🤖 Codeium — AI autocomplete 100% gratuit"),

    # Python
    ("ms-python.python",            "🐍 Python — suport complet"),
    ("ms-python.pylint",            "🐍 Pylint — detectare erori Python"),
    ("ms-python.black-formatter",   "🐍 Black — formatare automată cod Python"),

    # Git
    ("eamodio.gitlens",             "🔀 GitLens — Git super-powered"),
    ("mhutchie.git-graph",          "🔀 Git Graph — vizualizare ramuri Git"),

    # Teme frumoase
    ("dracula-theme.theme-dracula",  "🎨 Dracula — temă întunecată populară"),
    ("PKief.material-icon-theme",    "🎨 Material Icons — iconițe frumoase"),

    # Calitate cod
    ("esbenp.prettier-vscode",       "✨ Prettier — formatare automată"),
    ("streetsidesoftware.code-spell-checker", "✨ Spell Checker — verificare ortografie"),
    ("usernamehw.errorlens",         "✨ Error Lens — erori direct pe linie"),
    ("christian-kohler.path-intellisense", "✨ Path Intellisense — completare căi"),

    # Utilități
    ("ritwickdey.LiveServer",        "🌐 Live Server — server local pentru HTML"),
    ("ms-vscode.live-share",         "👥 Live Share — colaborare în timp real"),
    ("formulahendry.auto-rename-tag","🏷️  Auto Rename Tag — HTML/XML"),
    ("oderwat.indent-rainbow",       "🌈 Indent Rainbow — indentare colorată"),
    ("mechatroner.rainbow-csv",      "📊 Rainbow CSV — CSV colorat"),
    ("yzhang.markdown-all-in-one",   "📝 Markdown All in One"),
    ("wayou.vscode-todo-highlight",  "📌 TODO Highlight — evidențiază TODO-urile"),
    ("Gruntfuggly.todo-tree",        "📌 Todo Tree — lista de TODO-uri"),
    ("alefragnani.Bookmarks",        "🔖 Bookmarks — marchează linii importante"),
    ("ms-vscode-remote.remote-wsl",  "💻 Remote WSL — Linux în Windows"),
]

# ─── Setări VS Code ────────────────────────────────────────────────────────────
SETARI = {
    # Temă și aspect
    "workbench.colorTheme": "Dracula",
    "workbench.iconTheme": "material-icon-theme",
    "workbench.startupEditor": "none",
    "workbench.editor.enablePreview": False,

    # Font frumos pentru cod
    "editor.fontFamily": "'Cascadia Code', 'Fira Code', 'JetBrains Mono', Consolas, monospace",
    "editor.fontLigatures": True,
    "editor.fontSize": 14,
    "editor.lineHeight": 1.6,
    "editor.fontWeight": "400",

    # Editor
    "editor.tabSize": 4,
    "editor.insertSpaces": True,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": True,
    "editor.minimap.renderCharacters": False,
    "editor.cursorBlinking": "smooth",
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.smoothScrolling": True,
    "editor.renderWhitespace": "boundary",
    "editor.rulers": [80, 120],
    "editor.bracketPairColorization.enabled": True,
    "editor.guides.bracketPairs": True,
    "editor.formatOnSave": True,
    "editor.formatOnPaste": True,
    "editor.suggestSelection": "first",
    "editor.linkedEditing": True,
    "editor.multiCursorModifier": "ctrlCmd",

    # Terminal — Git Bash
    "terminal.integrated.defaultProfile.windows": "Git Bash",
    "terminal.integrated.fontFamily": "'Cascadia Code', monospace",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.cursorBlinking": True,
    "terminal.integrated.smoothScrolling": True,

    # Python
    "python.defaultInterpreterPath": "C:\\Users\\catal\\AppData\\Local\\Programs\\Python\\Python314\\python.exe",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": True,
    },

    # Git
    "git.enableSmartCommit": True,
    "git.confirmSync": False,
    "git.autofetch": True,
    "gitlens.hovers.currentLine.over": "line",

    # Altele
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "files.trimTrailingWhitespace": True,
    "files.insertFinalNewline": True,
    "explorer.confirmDelete": True,
    "explorer.confirmDragAndDrop": False,
    "breadcrumbs.enabled": True,
    "security.workspace.trust.untrustedFiles": "open",

    # Prettier
    "prettier.singleQuote": True,
    "prettier.semi": True,
    "prettier.tabWidth": 4,

    # Error Lens
    "errorLens.enabledDiagnosticLevels": ["error", "warning", "info"],

    # Todo highlight
    "todohighlight.keywords": [
        {"text": "TODO:", "color": "#fff", "backgroundColor": "#f90"},
        {"text": "FIXME:", "color": "#fff", "backgroundColor": "#e00"},
        {"text": "NOTE:", "color": "#fff", "backgroundColor": "#00a"},
    ],
}

# ─── Keybindings utile ─────────────────────────────────────────────────────────
KEYBINDINGS = [
    {"key": "ctrl+d", "command": "editor.action.copyLinesDownAction"},
    {"key": "ctrl+shift+k", "command": "editor.action.deleteLines"},
    {"key": "alt+up", "command": "editor.action.moveLinesUpAction"},
    {"key": "alt+down", "command": "editor.action.moveLinesDownAction"},
    {"key": "ctrl+`", "command": "workbench.action.terminal.toggleTerminal"},
    {"key": "ctrl+shift+f", "command": "workbench.action.findInFiles"},
]


def instaleaza_extensie(extensie_id: str, descriere: str) -> bool:
    try:
        result = subprocess.run(
            ["code", "--install-extension", extensie_id, "--force"],
            capture_output=True, text=True, timeout=60
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
    """Salvează setările în settings.json al VS Code."""
    cale_setari = Path(os.environ["APPDATA"]) / "Code" / "User" / "settings.json"
    cale_setari.parent.mkdir(parents=True, exist_ok=True)

    # Citim setările existente dacă există
    setari_existente = {}
    if cale_setari.exists():
        try:
            with open(cale_setari, "r", encoding="utf-8") as f:
                setari_existente = json.load(f)
        except Exception:
            pass

    # Combinăm cu cele noi
    setari_existente.update(setari)

    with open(cale_setari, "w", encoding="utf-8") as f:
        json.dump(setari_existente, f, indent=4, ensure_ascii=False)

    print(f"  {C.GREEN}[OK]{C.RESET}  Setări salvate în {cale_setari}")


def salveaza_keybindings(keybindings: list):
    """Salvează keybinding-urile în keybindings.json."""
    cale = Path(os.environ["APPDATA"]) / "Code" / "User" / "keybindings.json"
    cale.parent.mkdir(parents=True, exist_ok=True)

    with open(cale, "w", encoding="utf-8") as f:
        json.dump(keybindings, f, indent=4, ensure_ascii=False)

    print(f"  {C.GREEN}[OK]{C.RESET}  Keybindings salvate.")


def configureaza_git_bash():
    """Adaugă Git Bash ca terminal implicit în VS Code."""
    git_bash_path = "C:\\Program Files\\Git\\bin\\bash.exe"
    if not Path(git_bash_path).exists():
        git_bash_path = "C:\\Program Files (x86)\\Git\\bin\\bash.exe"

    if Path(git_bash_path).exists():
        SETARI["terminal.integrated.profiles.windows"] = {
            "Git Bash": {
                "path": git_bash_path,
                "args": ["--login", "-i"],
                "icon": "terminal-bash"
            }
        }
        print(f"  {C.GREEN}[OK]{C.RESET}  Git Bash configurat ca terminal implicit.")
    else:
        print(f"  {C.YELLOW}[SKIP]{C.RESET} Git Bash nu a fost găsit — terminalul rămâne PowerShell.")


def main():
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   ⚙️  CONFIGURARE VS CODE — Setup Complet Programator{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

    # Verifică că VS Code e instalat
    try:
        subprocess.run(["code", "--version"], capture_output=True, timeout=10)
    except Exception:
        print(f"  {C.RED}VS Code nu a fost găsit în PATH!{C.RESET}")
        print(f"  {C.YELLOW}Reinstalează VS Code de la code.visualstudio.com{C.RESET}\n")
        sys.exit(1)

    print(f"  {C.GREEN}✔ VS Code găsit!{C.RESET}\n")

    # ── PASUL 1: Extensii ──────────────────────────────────────────────────────
    print(f"{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  📦 PASUL 1 — Instalare extensii ({len(EXTENSII)} extensii){C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}\n")

    instalate = 0
    for ext_id, descriere in EXTENSII:
        if instaleaza_extensie(ext_id, descriere):
            instalate += 1
        time.sleep(0.5)

    print(f"\n  {C.GREEN}✔ {instalate}/{len(EXTENSII)} extensii instalate.{C.RESET}")

    # ── PASUL 2: Git Bash ──────────────────────────────────────────────────────
    print(f"\n{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  🖥️  PASUL 2 — Configurare Git Bash terminal{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}\n")
    configureaza_git_bash()

    # ── PASUL 3: Setări ────────────────────────────────────────────────────────
    print(f"\n{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  ⚙️  PASUL 3 — Aplicare setări{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}\n")
    salveaza_setari(SETARI)

    # ── PASUL 4: Keybindings ───────────────────────────────────────────────────
    print(f"\n{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  ⌨️  PASUL 4 — Configurare scurtături tastatură{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {'═'*58}{C.RESET}\n")
    salveaza_keybindings(KEYBINDINGS)

    # ── RAPORT FINAL ───────────────────────────────────────────────────────────
    print(f"\n{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}")
    print(f"{C.BOLD}{C.GREEN}  ✅ VS Code configurat perfect!{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{'═'*62}{C.RESET}\n")

    print(f"  {C.BOLD}Ce ai acum:{C.RESET}")
    print(f"  {C.GREEN}🤖{C.RESET} AI gratuit — Codeium + Continue (fără abonament)")
    print(f"  {C.GREEN}🎨{C.RESET} Temă Dracula + iconițe Material")
    print(f"  {C.GREEN}🔀{C.RESET} GitLens + Git Graph pentru Git")
    print(f"  {C.GREEN}🐍{C.RESET} Python complet cu formatare automată")
    print(f"  {C.GREEN}✨{C.RESET} Error Lens — erori vizibile direct pe linie")
    print(f"  {C.GREEN}💾{C.RESET} Salvare automată la 1 secundă")
    print(f"  {C.GREEN}🖥️ {C.RESET} Git Bash ca terminal implicit")

    print(f"\n  {C.YELLOW}⚠️  Închide și redeschide VS Code pentru a aplica tot!{C.RESET}\n")

    input("  Apasă Enter pentru a ieși...")


if __name__ == "__main__":
    main()
