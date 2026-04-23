import pyodbc
import customtkinter as c

c.set_appearance_mode("system")
c.set_default_color_theme("blue")

app = c.CTk()
app.geometry("200x300")
app.title("Creata\Connect MS DATABASE")

entry_database = c.CTkEntry(app, placeholder_text="Numele datei de baza")
entry_database.place(relx=0.1, rely=0.1)


def create_db():
    pass

create_button = c.CTkButton(app, text="Create", command=create_db, fg_color="green")

create_button.place(relx=0.1, rely=0.2)


def conect_db():
    try:
        conection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=localhost;"
            f"Database={entry_database.get()};"
            "Trusted_Connection=yes;"
        )
        info_label.configure(text='Conexiunea a avut succes')
    except pyodbc.Error as ex:
        info_label.configure(text="Conexiunea a esuat")


conect_button = c.CTkButton(app, text="Connect", command=conect_db, fg_color="blue")
conect_button.place(relx=0.1, rely=0.3)
info_label=c.CTkLabel(app,text='turtle')
info_label.place(relx=0.1,rely=0.4)
app.mainloop()


