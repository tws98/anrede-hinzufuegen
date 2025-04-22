import mariadb
import tkinter as tk
from tkinter import ttk
import sys

class Artikel:
    def __init__(self, artikel, bestand, lieferant):
        self.name = artikel
        self.bestand = bestand
        self.lieferant = lieferant

# --- Datenbankverbindung ---
try:
    conn = mariadb.connect(
        user="admin",
        password="admin",
        host="localhost",
        port=3306,  
        database="schlumpfshop3"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

# --- GUI ---
root = tk.Tk()
root.geometry("1000x600")
root.title("Mindestbestand prüfen")

label = ttk.Label(root, text="Mindestbestand eingeben:")
entry = ttk.Entry(root)

# --- Treeview als Tabelle ---
columns = ("Artikel", "Bestand", "Lieferant")
tree = ttk.Treeview(root, columns=columns, show="headings", height=25)

# Spaltenüberschriften setzen
tree.heading("Artikel", text="Artikelname")
tree.heading("Bestand", text="Bestand")
tree.heading("Lieferant", text="Lieferant")


# Spaltenbreite setzen
tree.column("Artikel", width=50)
tree.column("Bestand", width=100, anchor="center")
tree.column("Lieferant", width=100)

def anzeigen():
    # Tabelle leeren
    for row in tree.get_children():
        tree.delete(row)

    # Überprüfung ob gültige Zahl eingegeben wird
    try:
        min_bestand = int(entry.get())
    except ValueError:
        tree.insert("", "end", values=("Bitte gültige Zahl eingeben.", "", ""))
        return

    # SQL-Abfrage
    try:
        cur.execute("""
            SELECT artikel.Artikelname, artikel.Lagerbestand, lieferant.Lieferantenname
            FROM artikel
            INNER JOIN lieferant
            ON artikel.Lieferant = lieferant.ID_Lieferant
        """)
    except mariadb.Error as e:
        tree.insert("", "end", values=(f"Datenbankfehler: {e}", "", ""))
        return

    # Liste anlegen, indem die Objekte gespeichert werden
    artikel_liste = []

    # Schleife um die Objekte anzulegen und in die Liste zu speichern
    for a, b, c in cur:
        artikel = Artikel(a, b, c)
        if artikel.bestand <= min_bestand:
            artikel_liste.append(artikel)

    # Schleife um die Objekte in der Liste in die Tree-View der GUI zu integrieren
    if artikel_liste:
        for item in artikel_liste:
            tree.insert("", "end", values=(item.name, item.bestand, item.lieferant))
    else:
        tree.insert("", "end", values=("Keine Artikel unter dem Mindestbestand.", "", ""))

label.pack(pady=10)
entry.pack(pady=5)
ttk.Button(root, text="Anzeigen", command=anzeigen).pack(pady=5)
tree.pack(pady=10, fill="both", expand=True)

root.mainloop()
