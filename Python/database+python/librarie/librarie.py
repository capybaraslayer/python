from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy import create_engine, DateTime, text, ForeignKey, CheckConstraint
from sqlalchemy import insert
from datetime import datetime, timedelta
import re
import csv

metadata_obj = MetaData()
engine = create_engine("sqlite:///librarie.db")

user_table = Table(
    "user_acount",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Nume", String, nullable=False),
    Column("Prenume", String, nullable=False),
    Column("Data_nasterii", DateTime, nullable=False),
    Column("email", String, unique=True),
    Column("data_inregistrare", DateTime, default=datetime.now),
)
locatie_table = Table(
    "locatie",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Oras", String, nullable=False),
    Column("Comuna", String, nullable=False),
    Column("Strada_nr", String, nullable=False),
    Column("Bloc", String),
    Column("user_id", Integer, ForeignKey("user_acount.id"), nullable=False),
)
carte_table = Table(
    "carti",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Titlu", String, nullable=False),
    Column("autor", String, nullable=False),
    Column("categorie", String, nullable=False),
    Column(
        "An_aparitie",
        Integer,
        CheckConstraint("an_aparitie>0 and an_aparitie<2026"),
        nullable=False,
    ),
    Column("stock", Integer, CheckConstraint("stock>=0"), nullable=False, default=0),
)
autor_table = Table(
    "autor",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("Nume", String, nullable=False),
    Column("Prenume", String, nullable=False),
    Column("Tara", String, nullable=False),
    Column("carte_id", Integer, ForeignKey("carti.id"), nullable=False),
)
imprumut_table = Table(
    "imprumut",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("carte_id", Integer, ForeignKey("carti.id"), nullable=False),
    Column("autor_id", Integer, ForeignKey("autor.id"), nullable=False),
    Column("Data_imprumut", DateTime, default=datetime.now),
    Column("Data_return", DateTime, nullable=False),
    Column("Data_returnarii_efective", DateTime, nullable=False),
    Column("returnat", Boolean, default=False, nullable=False),
)

metadata_obj.create_all(engine)


# functie de sterge a unei tabele inca trebuie de lucrat la ea
def sterge_tabela():

    with engine.begin() as conn:
        conn.execute(text("drop table imprumut"))


# sterge_tabela()


# functie pentru validarea unui email
def validare_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


# functie pentru a introduce un utilizator al bibliotecii
def input_user():
    while True:
        nume = input("Numele dumneavoastra:").strip().title()
        prenume = input("Prenumele dumneavoastra:").strip().title()
        email = input("Introdu emailul dumneavoastra:").strip().lower()
        data_nasterii = input(
            "Introdu data nasterii dumneavoastra (DD-MM-YYYY): "
        ).strip()

        if not nume or not prenume or not email or not data_nasterii:
            print("Eroare toate campurile sunt necesar de completat reia operatiunea!")
            continue
        if validare_email(email) == False:
            print("Eroare:Adresas email nu este valida")
            continue

        try:
            data_nasterii = datetime.strptime(data_nasterii, "%d-%m-%Y").date()
        except ValueError:
            print(
                "Eroare: Formatul datei este incorect. Folosiți DD-MM-YYYY (ex: 25-12-1995).\n"
            )
            continue

        # Dacă s-a ajuns aici, înseamnă că toate datele sunt valide
        print("\nSucces! Datele au fost introduse corect.")
        break

    try:
        with engine.begin() as conn:
            conn.execute(
                insert(user_table).values(
                    Nume=nume, Prenume=prenume, Data_nasterii=data_nasterii, email=email
                )
            )
        print("Datele au fost salvate cu succes în baza de date!")
    except Exception as e:
        print(  # ce se întâmplă dacă pică conexiunea la BD
            f"A apărut o eroare la salvarea în baza de date: {e}"
        )

    input_user()


# fuctie pentru a citi dintrun fisier csv(cartile) in baza mea de date
def csv_cart():
    with open("carti.csv", "r") as carti:
        cititor = csv.reader(carti)
        for rand in cititor:
            if not rand:
                continue
            with engine.begin() as conn:
                conn.execute(
                    insert(carte_table)
                    .prefix_with("or ignore")
                    .values(
                        Titlu=rand[0],
                        autor=rand[1],
                        categorie=rand[2],
                        An_aparitie=int(rand[3]),
                        stock=int(rand[4]),
                    )
                )


# def main():


# main()
