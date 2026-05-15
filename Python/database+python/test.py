from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Creaza conexiunea cu baza de date. echo=True afiseaza SQL-ul generat in consola
engine = create_engine("sqlite:///librarie.db", echo=True)


# Test conexiune - executa un query simplu si returneaza rezultatul
# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all)


# Creeaza tabelul daca nu exista si insereaza carti
# INSERT OR IGNORE = sare peste duplicate (necesita UNIQUE pe coloana)
# conn.connect() = nu face commit automat, trebuie apelat manual
# with engine.connect() as conn:
#     conn.execute(text('create table if not exists carti(name str UNIQUE, stock int)'))
#     conn.execute(text('insert or ignore into carti(name,stock) values(:name, :stock)'),
#         [{"name":'Atomic habits',"stock":3}, {"name":'Mobby Dick',"stock":32}, {"name":'King of Thrones',"stock":10}]
#     )
#     conn.commit()


# Insereaza inca 3 carti
# engine.begin() = face commit automat la sfarsit, rollback automat la eroare
# with engine.begin() as conn:
#     conn.execute(text('insert or ignore into carti(name,stock) values(:name, :stock)'),
#         [{"name":'Tatat bogat tata sarac',"stock":4}, {"name":'Mhy hero academya',"stock":31}, {"name":'One piece',"stock":100}]
#     )


# Selecteaza toate cartile si afiseaza ultimele 4
# .all() = transforma Result intr-o lista indexabila cu []
# .scalar() = extrage o singura valoare dintr-un query (ex: COUNT)
# with engine.begin() as conn:
#     result = conn.execute(text('SELECT name,stock FROM carti')).all()
#     count = conn.execute(text('select count(name) from carti')).scalar()
#     for i in range(count-1, count-5, -1):
#         print(f'>name:{result[i].name}| stock:{result[i].stock}')


# Selecteaza toate cartile - unpacking direct din Result
# for name, stock in result = desface fiecare rand in variabile separate
# with engine.begin() as conn:
#     result = conn.execute(text('SELECT name,stock FROM carti'))
#     for name, stock in result:
#         print(f'>name:{name}| stock:{stock}')


# Selecteaza toate cartile - acces prin dictionar
# .mappings() = transforma randurile din Row in dictionar {"coloana": valoare}
# with engine.begin() as conn:
#     result = conn.execute(text('select name,stock from carti')).mappings().all()
#     for row in result:
#         print(f'name: {row["name"]} | stock: {row["stock"]}')


# Selecteaza cartile cu stoc mai mare de 23 - filtrare cu WHERE
# :y = placeholder pentru valoare, {"y": 23} = valoarea concreta
# Previne SQL injection fata de a pune direct valoarea in string
# with engine.begin() as conn:
#     result = conn.execute(text('select name,stock from carti where stock>:y'), {"y": 23}).mappings().all()
#     for row in result:
#         print(f'name: {row["name"]} | stock: {row["stock"]}')

with engine.begin() as conn:
    conn.execute(text('delete from carti where rowid not in(select min(rowid) from carti group by name)'))

msg=text('select name,stock from carti where stock<:y order by stock desc')
with Session(engine) as session:
    result= session.execute(msg,{"y":12}).mappings().all()
    for row in result:
         print(f'name: {row["name"]} | stock: {row["stock"]}')
