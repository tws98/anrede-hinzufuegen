#imports
 
import mariadb
import sys
import tkinter as tk
from tkinter import ttk


class Anrede():
    def __init__(self,id,anrede):
        self.id = id
        self.anrede = anrede


#connect mariadb
 
try:
    conn = mariadb.connect(
        user = "admin",
        password = "admin",
        host = "localhost",
        port = 3306,
        database = "schlumpfshop3")
 
except mariadb.Error as e:
    print(f"Error connecting to MariaDB PLatform: {e}")
    sys.exit(1)
cur = conn.cursor()



# Funktion um Daten in GUI zu integrieren

def anzeigen():
    liste_anrede = []

    for (id, anrede_str) in cur:
        anrede_obj = Anrede(id, anrede_str)
        liste_anrede.append(anrede_obj)

    for item in liste_anrede:
        tree.insert("", "end",values=(item.id, item.anrede))


#Funktion um neue Anrede hinzuzufügen

def hinzufügen ():
    for row in tree.get_children():
        tree.delete(row)


    neu = entry.get()


    try: 
        cur.execute(f"INSERT INTO anrede(anrede.Anrede)VALUES('{neu}')")

        cur.execute(f"""SELECT `ID_Anrede`, `Anrede`FROM `anrede` """)

    except mariadb.Error as e:
        print("Datenbankfehler!")


    conn.commit()

    anzeigen()

    entry.delete(0,"end")


#   GUI   

root = tk.Tk()
root.geometry("1000x600")
root.title("Anrede hinzufügen")
 
label = ttk.Label(root, text="Anrede hinzufügen: ")
entry = ttk.Entry(root)

columns = ("ID","Anrede")
tree = ttk.Treeview(root, columns=columns, show="headings", height= 25)

tree.heading("ID", text="ID")
tree.heading("Anrede", text="Anrede")

cur.execute(f"""SELECT `ID_Anrede`, `Anrede`FROM `anrede` """)


anzeigen()
label.pack(pady=10)
entry.pack(pady=5)
ttk.Button(root,text="Hinzufügen", command=hinzufügen).pack(pady=5)
tree.pack(pady=10)

root.mainloop()