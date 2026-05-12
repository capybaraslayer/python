from sqlalchemy import create_engine, text

engine = create_engine(
    "mssql+pyodbc://@CATALIN/Magazin"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)


def adauga_produs():
    print("====Adauga un produs====")
    with engine.begin() as conn:
        produs = input("Ce produs doresti sa adaugi:")
        stock = int(input("Ce stock sa aiba:"))
        price = int(input("Ce pret sa aiba:"))
        category_id = int(input("Ce catogorie id sa fie:"))
        conn.execute(
            text(
                """
                            INSERT INTO products (name, price, stock, category_id) VALUES
                            (:produs,:price,:stock,:category_id)"""
            ),
            {
                "produs": produs,
                "price": price,
                "stock": stock,
                "category_id": category_id,
            },
        )
        res = conn.execute(
            text(
                """
                            SELECT * FROM products WHERE name=:produs"""
            ),
            {
                "produs": produs,
                "price": price,
                "stock": stock,
                "category_id": category_id,
            },
        )
        print("====Produsul nou=====")
        for row in res:
            print(row)


def modifica_produs_id():
    print("====Modifica produs dupa id====")
    with engine.begin() as conn:
        id = int(input("Ce catogorie id sa fie "))

        res_inainte = conn.execute(
            text(
                """
                                 SELECT * FROM products WHERE id=:id"""
            ),
            {"id": id},
        )
        print("====Produsul modificat inainte de modificare=====")
        for row in res_inainte:
            print(row)
        price = int(input("Ce pret sa aiba"))
        conn.execute(
            text(
                """
                            UPDATE products SET price=:price WHERE id =:id"""
            ),
            {"price": price, "id": id},
        )
        res = conn.execute(
            text(
                """
                            SELECT * FROM products WHERE id=:id"""
            ),
            {"id": id},
        )

        print("====Produsul modificat dupa modificare=====")
        for row in res:
            print(row)


def sterge():
    while True:
        with engine.begin() as conn:
            disponibile = conn.execute(
                text(
                    """
                SELECT p.id, p.name
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                WHERE oi.product_id IS NULL
            """
                )
            )

            print("Produse care pot fi sterse:")
            for row in disponibile:
                print(f"  ID: {row.id} | Nume: {row.name}")
            id = int(input("Ce catogorie id sa fie "))
            res = conn.execute(
                text(
                    """
                                    SELECT * FROM order_items WHERE product_id=:id"""
                ),
                {"id": id},
            ).fetchone()
            if res is not None:
                print("eroare alege alt produs")
                continue
            produs = conn.execute(
                text("SELECT name FROM products WHERE id=:id"), {"id": id}
            ).fetchone()

            if produs is None:
                print("Nu exista niciun produs cu acest id!")
                continue

            conn.execute(text("DELETE FROM products WHERE id=:id"), {"id": id})

            print(f"Produsul '{produs.name}' a fost sters cu succes!")
            break


def actualizeaza():
    print("====Actualizez stockul unui produs====")
    with engine.begin() as conn:
        name = input("ce nume are:")

        res_inainte = conn.execute(
            text(
                """
                                    SELECT * FROM products WHERE name=:name"""
            ),
            {"name": name},
        )
        print("====Produsul inainte actualizarii=====")
        for row in res_inainte:
            print(row)
        stock = int(input("Ce stock sa aiba:"))
        conn.execute(
            text(
                """
                                UPDATE products SET stock=:stock WHERE name =:name"""
            ),
            {"stock": stock, "name": name},
        )
        res = conn.execute(
            text(
                """
                                SELECT * FROM products WHERE name=:name"""
            ),
            {"name": name},
        )

        print("====Produsul modificat dupa modificare=====")
        for row in res:
            print(row)


def gestioneaza_client():
    print("====Gestioneaza o comanda====")
    with engine.begin() as conn:
        id = int(input("Introdu id-ul comenzii:"))
        total = int(input("Introdu totalul"))
        res = conn.execute(
            text(
                "INSERT INTO orders (customer_id, order_date,total) OUTPUT Inserted.id VALUES (:cid, GETDATE(),:total)"
            ),
            {"cid": id, "total": total},
        ).fetchone()
        print(f"A fost creat comanda {res[0]}")


def adauga_produs():
    print("====Adauga un produs la comanda====")
    with engine.begin() as conn:
        cantitate = int(input("Introdu cantitate:"))
        produs = conn.execute(
            text(
                """SELECT * FROM products
                WHERE stock>=:cantitate
                """
            ),
            {"cantitate": cantitate},
        ).fetchall()
        for row in produs:
            print(f'{row.id}.{row.name}={row.stock}')
        produs_id = int(input("Introdu produs_id:"))
        produs_ales = None
        for row in produs:
            if row.id == produs_id:
                produs_ales = row
        if produs_ales is None:
            print("Produsul nu exista")
            return
        order_id = int(input("Introdu order_id:"))

        conn.execute(
            text(
                """INSERT INTO order_items(order_id,product_id,quantity,price)
                VALUES(:order_id,:produs_id,:cantitate,:price)
                """
            ),
            {"produs_id":produs_id,
             "order_id":order_id,
             "cantitate":cantitate,
             "price":produs_ales.price}
        )
        conn.execute(
            text(
                """UPDATE products SET stock = stock - :cantitate WHERE id = :produs_id
                """
            ),
            {
                "produs_id": produs_id,
                "cantitate": cantitate,
            },
        )
        conn.execute(
            text(
                """UPDATE orders SET total = total + (:price * :cantitate) WHERE id = :order_id
                """
            ),
            {   "price": produs_ales.price,
                "cantitate": cantitate,
                "order_id":order_id
            },
        )
        print(f"Produsul {produs_ales.name} a fost adaugat la comanda {order_id}!")
while True:
    print("====Start program====")
    print("1.Gestionare produs")
    print("2.Gestioneaza comenzile")
    comanda = int(input("Introdu numarul comenzii:"))
    if comanda == 1:
        while True:
            print("_____________________")
            print("1.Adauga un produs ")
            print("2.Modifica pretul unui produs dupa id")
            print("3.Sterge un produs dupa id ")
            print("4.Actualizeaza stocul unui produs")
            comanda = int(input("Care este numarul comenzii:"))
            if comanda == 1:
                adauga_produs()
            elif comanda == 2:
                modifica_produs_id()
            elif comanda == 3:
                sterge()
            elif comanda == 4:
                actualizeaza()
    if comanda == 2:
        while True:
            print("_____________________")
            print("1.Creează o comandă nouă pentru un client ")
            print("2.Adaugă produse la comandă")
            comanda = int(input("Care este numarul comenzii:"))
            if comanda == 1:
                gestioneaza_client()
            elif comanda == 2:
                adauga_produs()
