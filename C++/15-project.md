# Introduction to C++ (Part 15 Project)

## Project: Robot Maze

Build a small text-based game where a robot moves through a maze to reach its goal without crashing into walls. The game runs in the console, but its movement rules are similar to ones you might later use with a real robot.

### What the Game Does

The maze is a grid:

* `#` is a wall.
* `.` is an empty space.
* `G` is the goal.
* `R` is the robot.

The player types `w`, `a`, `s`, or `d` to move the robot up, left, down, or right. 

Typing `q` quits. 

The robot must stay inside the maze and cannot move through walls. 

When it reaches `G`, the player wins.

Use this maze:

```text

#######
#.....#
#.###.#
#...G.#
#######
```

The robot starts at row 1, column 1. Remember, row and column indexes start at 0.

### Your Tasks

* Make a 2D array containing the maze.
* Create a Robot class to store the robot’s row and column.
* Write a function that prints the maze, showing the robot in its current position.
* Read movement commands from the player.
* Check each move before changing the robot’s position:
* If the destination is a wall, keep the robot where it is.
* Otherwise, move the robot.
* Store each successful move in a std::vector<std::string>.
* Stop the game when the robot reaches the goal or the player quits.
* At the end, print how many successful moves the robot made.

### Rules to Help You Build It

* Keep the maze’s walls around its edge so the robot can’t leave the grid.
* When checking a move, look at the maze square the robot is trying to enter.
* Add a move to the vector only if the robot successfully moves.
* Print the maze again after each command so the player can see the robot’s new position.

### Example Play

The player could type:

```text

d
d
d
d
d
s
s
a

```

That moves the robot across the top open path, down, and then left onto the goal.

### Concepts You’ll Practice

This project uses a 2D array for the maze, a class for the robot, functions to organize the game, strings for commands, and a vector to remember successful moves. 

Try to get the basic game working first, then add a feature such as counting wall bumps or letting the player choose a maze.

> [!NOTE]
>
> Do your best!
>
> Do not worry if you cannot complete it all. 
> Try to do as much as you can. 
> We will walk through it together.
> 