# # Introduction to C++ (Part 9 Project)

## Project: The Little Treasure Maze

A tiny explorer is searching a maze for three treasures. Help them move around the map, avoid walls, and keep track of the treasures they find!
The map

Use a 2D array for the maze. In the array:


* **0** means an empty space.
* **1** means a wall.
* **2** means a treasure.

```cpp

int maze[5][5] = {
    {1, 1, 1, 1, 1},
    {1, 0, 2, 0, 1},
    {1, 0, 1, 2, 1},
    {1, 2, 0, 0, 1},
    {1, 1, 1, 1, 1}
};
```

The explorer starts at row 1, column 1. The outside edge is made of walls.

## Your mission

Write a program that lets the explorer search for all three treasures.

The player chooses a direction by typing W for up, A for left, S for down, or D for right. After each turn, show the maze again. Print the explorer as P, an empty space as ., a wall as #, and a treasure as T.
Your program must use

* A 2D array to store the maze.
* A 1D array to keep track of the treasures found. For example, store 10 points for each treasure.
* Nested for loops to print the maze row by row.
* A while loop to keep the game going until the explorer finds all three treasures or uses 15 turns.
* A do-while loop to keep asking for a direction until the player enters W, A, S, or D.

When the explorer tries to move into a wall, leave them where they are. When they find a treasure, add it to the treasure array and remove it from the maze so it can’t be collected twice.

At the end, use a for loop to add up the treasure points and print the total. Tell the player whether they found all three treasures or ran out of turns.
Test your game

Try these checks as you build:

* Does the maze print in five rows and five columns?
* Can the explorer collect a treasure?
* Does a wall stop the explorer?
* Does the program reject an invalid direction?
* Does the game stop after all three treasures are found or after 15 turns?

### Bonus challenge: 

Let the player choose whether to play again using another **do while** loop.
