from Model import Model
from View import View
import sqlite3


class Controller:
    def __init__(self):
        """
        Initializes the controller with an instance of Model and an instance of View.
        """
        self.model = Model(50)  # Create an instance of Model with a size of 50
        self.view = View()  # Create an instance of View

    def init(self):
        """
        Initializes the map by adding water, running WFC collapse, and adding roads.
        """
        self.model.add_water()
        self.model.wfc.run_collapse()
        self.model.add_road(20)
        # self.model.add_bridges_with_spacing()  # Method to call for adding bridges

    def run(self, isNewMap=True):
        """
        Executes the program by initializing or loading a map, then displaying the map.

        :param isNewMap: Boolean indicating whether to initialize a new map (default True)
        """
        if isNewMap:
            self.init()  # Initializes a new map
        else:
            self.load("test3")  # Loads an existing map

        # Adds trees and houses to the map based on the WFC grid
        self.model.addTrees(self.model.wfc.grid)
        self.model.addHouses(self.model.wfc.grid)

        # Updates the view with the terrain changes and displays the map
        self.view.changeLand(self.model)
        self.view.displayMap(self.model)

    def save(self):
        """
        Saves the map data to a SQLite database.
        """
        # Connect to the SQLite database
        conn = sqlite3.connect('ma_base_de_donnees.db')
        cur = conn.cursor()

        # Create the maps table if it doesn't exist
        cur.execute('''
        CREATE TABLE IF NOT EXISTS maps (
            map_id INTEGER PRIMARY KEY AUTOINCREMENT,
            map_name TEXT UNIQUE,
            grid_size INTEGER
        )
        ''')
        conn.commit()

        # Create the lands_layer table if it doesn't exist
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

        # Insert map information into the maps table
        map_name = "test3"  # Replace this with the actual name of your map
        cur.execute('INSERT INTO maps (map_name, grid_size) VALUES (?,?)', (map_name, self.model.n_))
        map_id = cur.lastrowid  # Get the ID of the newly added map

        # Prepare data to insert into the lands_layer table
        data_to_insert = [(map_id, rowIndex, columnIndex, value)
                          for rowIndex, row in enumerate(self.model.wfc.grid)
                          for columnIndex, valueSet in enumerate(row) for value in valueSet]

        # Insert grid data into the lands_layer table
        cur.executemany('INSERT INTO lands_layer (map_id, rowIndex, columnIndex, value) VALUES (?, ?, ?, ?)',
                        data_to_insert)
        conn.commit()

        # Close the database connection
        conn.close()

    def load(self, map_name):
        """
        Loads map data from a SQLite database.

        :param map_name: Name of the map to load
        """
        # Connect to the SQLite database
        conn = sqlite3.connect('ma_base_de_donnees.db')
        cur = conn.cursor()

        # Select the map ID by its name
        cur.execute('SELECT map_id, grid_size  FROM maps WHERE map_name = ?', (map_name,))
        map_id, grid_size = cur.fetchone()

        # Select the grid data for this map
        cur.execute('SELECT rowIndex, columnIndex, value FROM lands_layer WHERE map_id = ?', (map_id,))
        grid_elements = cur.fetchall()

        # Close the database connection
        conn.close()

        # Reconstruct the grid from the retrieved data
        grid = [[set() for _ in range(grid_size)] for _ in range(grid_size)]

        for rowIndex, columnIndex, value in grid_elements:
            grid[rowIndex][columnIndex] = {value}

        self.model.wfc.grid = grid


# Create an instance of Controller and run the program
c = Controller()
c.run(isNewMap=True)
# c.save()  # Uncomment to save the map to the database
