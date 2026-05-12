# import requests

# # ============================================================
# #                    LIBRARIA REQUESTS
# # ============================================================
# # Libraria "requests" permite Python-ului sa comunice cu internetul.
# # Cu ea poti: lua date de pe site-uri, trimite date, autentifica, etc.
# # Instalare: pip install requests
# # ============================================================


# # ============================================================
# # PROGRAMUL 1: Cerere simpla GET
# # ============================================================
# # GET = ceri date de la server. Datele sunt vizibile in URL.
# # requests.get(url) trimite cererea si returneaza un "response"
# # cu tot ce a raspuns serverul.
# # ============================================================

# url = "https://jsonplaceholder.typicode.com/posts/1"
# response = requests.get(url)

# # status_code = codul de raspuns al serverului
# # 200 = succes | 404 = negasit | 401 = neautorizat | 500 = eroare server
# print("Status code:", response.status_code)

# # headers = informatii despre raspuns (tip de date, lungime, etc.)
# print("Content-Type:", response.headers.get("Content-Type"))

# # .json() = transforma raspunsul JSON intr-un dictionar Python
# data = response.json()

# # acum accesezi datele ca un dictionar Python normal
# print("Titlul postarilor:", data["title"])
# print("Tot raspunsul:", data)


# # ============================================================
# # PROGRAMUL 2: Cerere GET cu parametrii (params)
# # ============================================================
# # params = informatii extra trimise serverului prin URL
# # Fara params: site.com/posts
# # Cu params:   site.com/posts?page=2
# #
# # In loc sa construiesti URL-ul manual cu "?" si "&",
# # dai un dictionar Python si requests construieste URL-ul automat.
# #
# # IMPORTANT pentru proiectul tau meteo:
# # params = {"q": "Chisinau", "appid": "cheia_ta", "units": "metric"}
# # → construieste automat: ?q=Chisinau&appid=cheia_ta&units=metric
# # ============================================================

# url = "https://jsonplaceholder.typicode.com/posts"
# params = {"userId": 1}  # vrem doar postarile userului cu id=1

# response = requests.get(url, params=params)

# # .url = arata URL-ul final construit de requests cu parametrii
# print("URL final construit:", response.url)

# data = response.json()

# # data este o lista de postari → parcurgem cu for
# for post in data:
#     print("Titlu:", post["title"])


# # ============================================================
# # PROGRAMUL 3: Cerere POST
# # ============================================================
# # POST = trimiti date catre server (ascunse, nu in URL)
# # Se foloseste pentru: creare date, autentificare, formulare
# #
# # Diferenta GET vs POST:
# # GET  → ceri date    → vizibil in URL  → ex: cautare
# # POST → trimiti date → ascuns in URL   → ex: login, creare
# #
# # payload = datele pe care le trimiti serverului (ca un dictionar)
# # json=payload → requests le transforma automat in format JSON
# # ============================================================

# url = "https://jsonplaceholder.typicode.com/posts"
# payload = {
#     "title": "Hello from Python",
#     "body": "Acesta este un test",
#     "userId": 1,
# }

# response = requests.post(url, json=payload)

# # 201 = Created → serverul a creat resursa cu succes
# print("Status code:", response.status_code)
# data = response.json()
# print("Raspuns server:", data)


# # ============================================================
# # PROGRAMUL 4: Timeout si tratarea erorilor (try/except)
# # ============================================================
# # timeout = cat timp sa astepti raspunsul serverului (in secunde)
# # Daca serverul nu raspunde in timp → Timeout error
# #
# # raise_for_status() = arunca eroare automata daca status != 200
# # In loc sa verifici manual "if status_code == 404",
# # raise_for_status() face asta automat pentru orice eroare.
# #
# # try/except = incerci ceva, iar daca da eroare o prinzi si o gestionezi
# # Fara try/except → programul se opreste la eroare
# # Cu try/except    → prinzi eroarea si afisezi un mesaj frumos
# #
# # IMPORTANT pentru proiectul tau meteo:
# # Daca userul scrie un oras gresit → 404 → prinzi eroarea
# # Daca internetul e slab → Timeout → prinzi eroarea
# # ============================================================

# try:
#     response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)

#     # arunca eroare automata daca status code nu e 200
#     response.raise_for_status()

#     print("Succes!", response.json())

# except requests.exceptions.Timeout:
#     # serverul nu a raspuns in 5 secunde
#     print("Eroare: Serverul nu raspunde (timeout)")

# except requests.exceptions.HTTPError as e:
#     # status code a fost 4xx sau 5xx (ex: 404, 401, 500)
#     print("Eroare HTTP:", e)

# except requests.exceptions.RequestException as e:
#     # orice alta eroare legata de requests (internet cazut, URL gresit, etc.)
#     print("Eroare generala:", e)
import requests

url = "https://geocoding-api.open-meteo.com/v1/search?name=Chisinau&count=1&language=ro"
response=requests.get(url)
data_loc=response.json()
lat = data_loc["results"][0]["latitude"]
long = data_loc["results"][0]["longitude"]
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
response = requests.get(url)
data_meteo = response.json()
viteza_vant = data_meteo["current_weather"]["windspeed"]
temperatura = data_meteo["current_weather"]["temperature"]
directie_vant = data_meteo["current_weather"]["winddirection"]
print(f"Vremea de afara temperatura:{temperatura} viteza vantului:{viteza_vant} directia vantului:{directie_vant}")
