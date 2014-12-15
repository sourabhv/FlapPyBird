
Instructions to Run the Game:

This project includes a folder named "assets" which contains all the objects in the form of PNG files necessary to create an environment for Flappy Bird game. The game is built on python 2.7 and requires the pygame library install on the user's machine. The game is divided into three parts - assets, flappy.py and learning.py.

As mentioned earlier, the game objects are contained in the "assets" folder. This includes pipes, bird (with up flap, mid flap and low flap), background and welcome screen. flappy.py contains the code which imports all the objects form the assets and the logic to create an illusion that game is dynamic and the bird is flying. It imports pygame library and it's functions which controls the motion of the bird and laws of physics which are governing the environment. Lastly, learning.py contains the code which creates an Artificial Agent that controls the bird  and helps it to take precise decisions to act based on the data acquired while training episodes. This file in imported in game.py.

How to manually control the game speed?
To control the game speed, change the value of FPS global 
variable declared in game.py. More the value, much faster the game will be. 

To Run the game, just type this on the terminal:

> python flappy.py

To exit out of the game just press ESC key on the keyboard and you will be returned back to the terminal.

Thank you for using Flappy Bird: Learning to Fly.

