from sqlalchemy import MetaData, Table,Column,Integer ,String
from sqlalchemy import create_engine,DateTime,text,ForeignKey,CheckConstraint
from sqlalchemy import insert
from datetime import datetime
metadata_obj= MetaData()
engine = create_engine("sqlite:///librarie.db")

user_table=Table(
    "user_acount",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("Nume",String,nullable=False),
    Column("Prenume",String,nullable=False),
    Column("Data_nasterii",DateTime,nullable=False),
    Column("email",String,unique=True),
    Column("data_inregistrare", DateTime, default=datetime.now),    
)
locatie_table=Table(
    "locatie",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("Oras",String,nullable=False),
    Column("Comuna",String,nullable=False),
    Column("Strada_nr",String,nullable=False),
    Column("Bloc",String),
    Column("user_id",Integer,ForeignKey('user_acount.id'),nullable=False),    

)
carte_table=Table(
    "carti",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("Titlu",String,nullable=False),
    Column("autor",String,nullable=False),
    Column("categorie",String,nullable=False),
    Column("An_aparitie",Integer,CheckConstraint('an_aparitie>1000 and an_aparitie<2026'),nullable=False),
    Column("stock",Integer,CheckConstraint("stock>=0"),nullable=False,default=0),

)
autor_table=Table(
    "autor",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("Nume",String,nullable=False),
    Column("Prenume",String,nullable=False),
    Column("Tara",String,nullable=False),
    Column("carte_id",Integer,ForeignKey("carti.id"),nullable=False),
)
imprumut_table=Table(
    "imprumut",
    metadata_obj,
    Column("id",Integer,primary_key=True,autoincrement=True),
    Column("Nume",String,nullable=False),
    Column("Prenume",String,nullable=False),
    Column("Tara",String,nullable=False),
)

metadata_obj.create_all(engine)
def sterge_tabela():
    nume=input("Introdu tabela pe care doresti so stergi")
    with engine.begin() as conn:
        conn.execute(text('drop table autor'))
        conn.execute(text('drop table :y'), {"y": nume})

def input_user():
    while(True):
        nume=input("Numele dumneavoastra:").strip().title()
        prenume=input("Prenumele dumneavoastra:").strip().title()
        email=input("Introdu emailul dumneavoastra:").strip().lower()
        
        if '@' in email and  nume and prenume:
            break
    try:
            data_nasterii=input('Introdu data nasterii dumneavoastra:')
            data_nasterii = datetime.strptime(data_nasterii,"%d-%m-%Y")
            print("Succes! Formatul este corect:",data_nasterii)
    except ValueError:
            print("Eroare: Formatul specificat nu se potrivește cu textul.")
    with engine.begin()as conn:
        comanda=conn.execute(insert(user_table).values(Nume=nume,
        Prenume=prenume,Data_nasterii=data_nasterii,
        email=email))
    

input_user()
    

# def main():








# main()
