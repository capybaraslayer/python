import socket
import threading

port_meu = int(input("Introdu portul tau: "))
IP_MEU = socket.gethostbyname(socket.gethostname())

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
soc.bind(("", port_meu))

soc_g = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_g.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc_g.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
soc_g.bind(("", 9000))

utilizatori = {}
mod_activ = None
DEST = (None, None)


def print_msg(prefix, mesaj):
    prompt = "  Tu: " if mod_activ in ("privat", "general") else "> "
    print(f"\r{prefix} {mesaj}\n", end="", flush=True)


def receptor():
    while True:
        try:
            data, (ip, port) = soc.recvfrom(4096)
            mesaj = data.decode()
            if mod_activ == "privat" and (ip, port) == DEST:
                print_msg(f"[PRIVAT {ip}:{port}]", mesaj)
            elif mod_activ != "privat":
                print_msg(f"[MESAJ {ip}:{port}]", mesaj)
        except Exception as e:
            print(f"[EROARE] {e}")


def discovery():
    while True:
        try:
            data, (ip, port) = soc_g.recvfrom(4096)
            mesaj = data.decode()
            este_eu = ip in (IP_MEU, "127.0.0.1") and (
                mesaj == f"JOIN:{port_meu}" or mesaj == f"HELLO:{port_meu}"
            )
            if este_eu:
                continue
            if mesaj.startswith("JOIN:"):
                p = int(mesaj.split(":")[1])
                utilizatori[ip] = p
                print_msg("[+]", f"{ip}:{p}")
                soc_g.sendto(f"HELLO:{port_meu}".encode(), (ip, 9000))
            elif mesaj.startswith("HELLO:"):
                utilizatori[ip] = int(mesaj.split(":")[1])
                print_msg("[+]", f"{ip}:{utilizatori[ip]}")
            elif mesaj.startswith("MSG:"):
                print_msg(f"[GENERAL {ip}]", mesaj[4:])
        except Exception as e:
            print(f"[EROARE] {e}")


def main():
    global mod_activ, DEST
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            if cmd == "privat":
                DEST = (input("  IP: ").strip(), int(input("  Port: ").strip()))
                mod_activ = "privat"
                print(f"[PRIVAT] -> {DEST[0]}:{DEST[1]} | exit pentru a iesi")
                while True:
                    msg = input("  Tu: ")
                    if msg.strip().lower() == "exit":
                        mod_activ = None
                        break
                    soc.sendto(msg.encode(), DEST)
            elif cmd == "general":
                mod_activ = "general"
                print(
                    f"[GENERAL] -> {len(utilizatori)} utilizatori | exit pentru a iesi"
                )
                while True:
                    msg = input("  Tu: ")
                    if msg.strip().lower() == "exit":
                        mod_activ = None
                        break
                    soc_g.sendto(f"MSG:{msg}".encode(), ("255.255.255.255", 9000))
            elif cmd == "lista":
                print(
                    "\n".join(f"  {ip}:{p}" for ip, p in utilizatori.items())
                    or "  (gol)"
                )
            elif cmd == "end":
                break
            elif cmd:
                print("[SISTEM] Comenzi: privat | general | lista | end")
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"[EROARE] {e}")
    print("[SISTEM] Deconectat.")


threading.Thread(target=receptor, daemon=True).start()
threading.Thread(target=discovery, daemon=True).start()

soc_g.sendto(f"JOIN:{port_meu}".encode(), ("255.255.255.255", 9000))
print(f"[SISTEM] Port: {port_meu} | IP: {IP_MEU}")
print("[SISTEM] Comenzi: privat | general | lista | end")
main()
