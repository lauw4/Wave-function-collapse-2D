# Wave Collapse Map

This project is a 2D map generator in Python3 that utilizes the wave collapse algorithm. It creates a game environment with a player and characters. The player can be controlled using direction keys, while the characters move randomly. The objective is for the player to avoid getting caught by the characters, as being caught will result in the player being deleted from the map.
We used sql database to save the map so that the user can have a choice to use the saved map

## Installation

To run the game, make sure you have Python3 installed on your system. You can install the required libraries by running:
>> pip install -r requirements.txt

## Usage

Run the game by executing the following command:
>> Python3 Controller.py

Once the game is running, control the player using the arrow keys. The objective is to navigate the player across the map without getting caught by the randomly moving characters.

### Generation of Map and Props

The map and props in the game are generated using the wave collapse algorithm, ensuring coherence and adherence to specified constraints:

1. **Initialization**: Initialize a grid with cells representing different terrains.
  
2. **Wave Collapse Algorithm**: Apply the wave collapse algorithm to the grid to determine the final configuration of the map.
  
3. **Generation of Props**: Additional props such as tree and buildings are randomly placed on the map with a ration of presence to enhance gameplay.

4. **Finalization**: After generating the map and props, the game environment is ready for interaction.


## Gameplay

- Use the arrow keys (up, down, left, right) to move the player.
- Avoid getting caught by the characters moving randomly on the map.
- If the player gets caught by a character, the game ends.
- The objective is to survive as long as possible without getting caught.

## File Structure

- `Controller.py`: Main Python script to run the game.
- `WFC.py`: Contains classes and functions for generating the game map.
- `character.py`: Contains classes for defining the player and characters.
- `Model.py`: Handles the backend tasks.
- `Props.py`,`Tree.py` and `Houses`: Contains classes for defining Trees and houses in the map
- `View.py`: Main Visualization( frontend) of the game.
- `requirements.txt`: Specifies the required libraries for the project.

## Credits

This project was created by `Victor`, `Wael`, `Prince`.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).