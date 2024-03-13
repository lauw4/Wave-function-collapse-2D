from Model import Model
from View import View
import sqlite3


class Controller:
    def __init__(self):
        self.model = Model(50)
        self.view = View()

    def init(self):

        self.model.add_water()
        self.model.wfc.run_collapse()
        self.model.add_road(30)

    def run(self, is_new_map=True):
        if is_new_map:
            self.init()
        else:
            self.load("test3")

        self.model.addTrees()
        self.model.addHouses()
        self.view.changeLand(self.model)
        self.view.displayMap(self.model)

    def save(self, map_name):

        # Connexion à la base de données SQLite
        conn = sqlite3.connect('ma_base_de_donnees.db')
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS maps (
            map_id INTEGER PRIMARY KEY AUTOINCREMENT,
            map_name TEXT UNIQUE,
            grid_size INTEGER
        )
        ''')

        conn.commit()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS lands_layer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            map_id INTEGER,
            rowIndex INTEGER,
            columnIndex INTEGER,
            value INTEGER,
            FOREIGN KEY (map_id) REFERENCES maps(map_id)
        )
        ''')
        conn.commit()

        cur.execute('INSERT INTO maps (map_name, grid_size) VALUES (?,?)', (map_name, self.model.n_))
        map_id = cur.lastrowid  # Récupérer l'ID de la nouvelle carte ajoutée

        donnees_a_inserer = [(map_id, rowIndex, columnIndex, value)
                             for rowIndex, row in enumerate(self.model.wfc.grid)
                             for columnIndex, valueSet in enumerate(row) for value in valueSet]

        cur.executemany('INSERT INTO lands_layer (map_id, rowIndex, columnIndex, value) VALUES (?, ?, ?, ?)',
                        donnees_a_inserer)

        conn.commit()

        # Fermer la connexion
        conn.close()

    def load(self, map_name):
        # Connexion à la base de données SQLite
        conn = sqlite3.connect('ma_base_de_donnees.db')
        cur = conn.cursor()

        # Sélectionner l'ID de la carte par son nom
        nom_de_la_carte = map_name  # Remplacez par le nom réel de votre carte
        cur.execute('SELECT map_id, grid_size  FROM maps WHERE map_name = ?', (nom_de_la_carte,))
        map_id, grid_size = cur.fetchone()

        # Sélectionner les données de la grille pour cette carte
        cur.execute('SELECT rowIndex, columnIndex, value FROM lands_layer WHERE map_id = ?', (map_id,))
        elements_de_la_grille = cur.fetchall()

        # Fermer la connexion
        conn.close()

        grille = [[set() for _ in range(grid_size)] for _ in range(grid_size)]

        for rowIndex, columnIndex, value in elements_de_la_grille:
            grille[rowIndex][columnIndex] = {value}

        self.model.wfc.grid = grille


c = Controller()
c.run(is_new_map=True)
# c.save("Map1")
