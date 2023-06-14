# Snake AI with Genetic Algorithm

### Description
This project implements a snake game in Pygame with a twist - the snake is controlled by an AI agent trained using a genetic algorithm. The goal is for the snake to collect as much food as possible while avoiding crashing into walls or its own body.

The genetic algorithm works by evolving a population of candidate AI agents over multiple generations. Each agent's fitness is evaluated based on its performance in the game, and the fittest individuals are selected to produce offspring for the next generation. Through this process of selection, crossover, and mutation, the AI gradually learns to navigate the game more effectively.

The project is implemented in Python, using the Pygame library for graphics and user input. The genetic algorithm is implemented from scratch, using basic concepts of population genetics.

If you're interested in AI, game development, or just want to play a fun game of snake, check out this project!

## Snake AI in Action

Watch the trained Snake AI in action! The GIF below showcases the gameplay of the Snake game controlled by the AI agent trained using a genetic algorithm. 

![snake_ai_gif](https://user-images.githubusercontent.com/75861915/236212912-ce789013-78c4-4b13-a4e1-d1a4e15bed0e.gif)

The AI agent has gone through multiple generations of evolution, gradually improving its performance in collecting food while avoiding collisions with walls or its own body. It demonstrates the capability of the genetic algorithm to train an AI to navigate the game effectively.

### Technologies Used

- Python: The project is implemented in Python programming language.
- Pygame: The Pygame library is used for graphics and user input in the snake game.
- Genetic Algorithm: The genetic algorithm is implemented from scratch using basic concepts of population genetics.

### How to Play

To play the Snake AI game:

1. Clone the project repository from [Snake AI with Genetic Algorithm](https://github.com/d-lehel/snakeAI-genetic-algorithm).
2. Make sure you have Python and Pygame installed on your machine.
3. Run the `GA_brain_test.py` file using the Python interpreter to test a single trained individual, or you can train a new individual with different parameters using the `GA_training.py` file.
4. If you prefer to train manually by playing the game and collecting gameplay data, you can use the following files: `M_data_collect.py` to collect the data, `M_network_training.py` to train the neural network from the data, and `M_brain_test.py` to test the trained network.

Feel free to explore the code and experiment with different parameters to observe the AI's learning process. If you have any questions or suggestions, feel free to reach out to me. Have fun!
