import sqlite3
from Model import Model

class Database():
    def __init__(self) -> None:
        self.model = Model()
        self.db_name = './database/wfc_database.db'


    def save_to_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Create table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS maps
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    map_grid TEXT,
                    player_x INTEGER,
                    player_y INTEGER)''')

        # Save the map grid as a string
        map_grid_str = str([str(row) for row in self.model.wfc.grid])

        # Save the player position
        player_x, player_y = self.model.player.x, self.model.player.y

        # Insert the data into the table
        c.execute("INSERT INTO maps (map_grid, player_x, player_y) VALUES (?, ?, ?)", (map_grid_str, player_x, player_y))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()


    def load_from_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        # Fetch the last saved map and player position
        c.execute("SELECT * FROM maps ORDER BY id DESC LIMIT 1")
        result = c.fetchone()

        if result:
            map_grid_str, player_x, player_y = result
            map_grid = [list(map(int, row.strip("{}").split(","))) for row in map_grid_str.strip("[]").split("),(")]

            # Create a new model with the loaded map and player position
            self.model.wfc.grid = map_grid
            self.model.player.x = player_x
            self.model.player.y = player_y

            # Add trees, houses, and other objects to the map as needed

            return self.model
        else:
            return Model()
        

