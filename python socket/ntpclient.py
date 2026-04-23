import ntplib
from datetime import datetime,timezone,timedelta

zona = input("Introdu zona geografica (ex: GMT+2, GMT-5): ")

offset_str = zona.replace("GMT", "").replace("UTC", "")
offset_ore = int(offset_str)
c = ntplib.NTPClient()
rasp = c.request('pool.ntp.org')
tz = timezone(timedelta(hours=offset_ore))  # cream fusul orar
ora_utc = datetime.fromtimestamp(rasp.tx_time, tz=timezone.utc)
ora_locala = ora_utc.astimezone(tz)  # convertim in zona dorita

print(f'Ora exacta pentru {zona}: {ora_locala.strftime("%Y-%m-%d %H:%M:%S")}')
