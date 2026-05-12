from sqlalchemy import create_engine, text


engine = create_engine(
    "mssql+pyodbc://@CATALIN/Magazin"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

try:
    with engine.connect() as conn:
        conn.execute(text("select @@version"))
        print("Conectat cu succes")
except Exception as e:
    print(e)

while True:
    print('====START====')
    print('1.Afiseaza toate produsele din tabel')
    print('2.Afiseaa toti clienti')
    print('3.Afiseaza doar produsele cu stoc mai mare ca 20')
    print('4.Afiseaza doar produsele cu pretul sub 200 de lei')
    print('5.Afiseaza produsele sortate dupa pret(crescator)')
    print("6.Afiseaza produsele sortate dupa pret(descrescator)")
    print('7.End')
    comanda=int(input('Introdu numarul comenzii:'))
    if comanda==1:
        print("====Toatea produsele")
        with engine.begin() as conn:
            res=conn.execute(text("""
                            SELECT * FROM products
                                """))
            for row in res:
                print(row)
            conn.commit()
    if comanda==2:
        print('====Toti clienti====')
        with engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                            SELECT * FROM customers
                                """
                )
            )
            for row in res:
                print(row)
    if comanda == 3:
        print("====Toate produsele cu stoc mai mare de 20====")
        with engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                            SELECT * FROM products WHERE stock >20
                                """
                )
            )
            for row in res:
                print(row)
    if comanda == 4:
        print("====Toate produsele cu pret mai mare de 200 lei====")
        with engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                            SELECT * FROM products WHERE price >200
                                """
                )
            )
            for row in res:
                print(row)
    if comanda == 5:
        print("====Aranjeaza produsele in ordine crescatoare====")
        with engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                            SELECT * FROM products ORDER BY stock ASC
                                """
                )
            )
            for row in res:
                print(row)
    if comanda == 6:
        print("====Aranjeaza produsele in ordine crescatoare====")
        with engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                            SELECT * FROM products ORDER BY stock DESC
                                """
                )
            )
            for row in res:
                print(row)

    if comanda==7:
        print('====END PROGRAM====')
        break
