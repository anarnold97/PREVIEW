# Introduction to C++ (Part 15 Project)

## Robot Maze: Complete Solution

This version uses a 2D character array for the maze, a Robot class for the robot’s position, functions for printing and movement, strings for commands, and a vector to record successful moves.

```cpp

#include <iostream>
#include <string>
#include <vector>

class Robot {
public:
    int row;
    int column;
};

void printMaze(const char maze[5][8], const Robot& robot) {
    for (int row = 0; row < 5; row++) {
        for (int column = 0; column < 7; column++) {
            if (row == robot.row && column == robot.column) {
                std::cout << 'R';
            } else {
                std::cout << maze[row][column];
            }
        }

        std::cout << "\n";
    }
}

bool moveRobot(const char maze[5][8], Robot& robot,
               const std::string& command) {
    int nextRow = robot.row;
    int nextColumn = robot.column;

    if (command == "w") {
        nextRow--;
    } else if (command == "s") {
        nextRow++;
    } else if (command == "a") {
        nextColumn--;
    } else if (command == "d") {
        nextColumn++;
    } else {
        std::cout << "Unknown command. Use w, a, s, d, or q.\n";
        return false;
    }

    if (maze[nextRow][nextColumn] == '#') {
        std::cout << "There's a wall there. The robot stays put.\n";
        return false;
    }

    robot.row = nextRow;
    robot.column = nextColumn;
    return true;
}

int main() {
    const char maze[5][8] = {
        "#######",
        "#.....#",
        "#.###.#",
        "#...G.#",
        "#######"
    };

    Robot robot;
    robot.row = 1;
    robot.column = 1;

    std::vector<std::string> moveHistory;
    std::string command;
    bool quit = false;

    std::cout << "Robot Maze\n";
    std::cout << "Move with w (up), a (left), s (down), d (right).\n";
    std::cout << "Type q to quit.\n\n";

    while (!quit) {
        printMaze(maze, robot);

        std::cout << "Command: ";
        std::cin >> command;

        if (command == "q") {
            quit = true;
        } else if (moveRobot(maze, robot, command)) {
            moveHistory.push_back(command);
        }

        if (maze[robot.row][robot.column] == 'G') {
            printMaze(maze, robot);
            std::cout << "You reached the goal!\n";
            break;
        }

        std::cout << "\n";
    }

    std::cout << "Successful moves: " << moveHistory.size() << "\n";

    return 0;
}
```

---

## Step-by-Step Walkthrough

1. Include the tools the program uses.
  	
  	At the top of the code:
    
    ```cpp

    #include <iostream>
    #include <string>
    #include <vector>
    ```
    
    <iostream> provides std::cout and std::cin. <string> lets the program store commands as strings. <vector> provides the move-history list.

 2. Define what a robot stores.

	This class defines a robot’s position:
    
    ```cpp

    class Robot {
    public:
        int row;
        int column;
    };
    ```

	Each Robot object has a row number and a column number. The class is a description; the actual robot object is created later in main.

3. Set up the maze.
  
	Inside main, the maze is stored in a 2D character array:
  	
  	```cpp

    const char maze[5][8] = {
        "#######",
        "#.....#",
        "#.###.#",
        "#...G.#",
        "#######"
    };
    ```

	There are five rows. Each row has seven maze symbols, plus a terminating character stored at the end of the row, so each row has space for eight characters. The `const` means the maze layout will not be changed by the program. # represents a wall, . an open square, and G the goal.

4. Create the robot and its move history.

	These lines create the robot, place it at row 1, column 1, and make an empty vector to hold successful moves:
  
  	```cpp

    Robot robot;
    robot.row = 1;
    robot.column = 1;

    std::vector<std::string> moveHistory;
    std::string command;
    bool quit = false;
    ```

	The robot starts on an open square. command will hold what the player types, and quit tracks whether the player has chosen to exit.

5. Print the maze and show the robot.
  
	The game loop calls:
  	```cpp

    printMaze(maze, robot);
  	```  
    
	Inside printMaze, nested loops visit each maze position:
  
  	```cpp

    for (int row = 0; row < 5; row++) {
        for (int column = 0; column < 7; column++) {
   	```
    
	At each position, this condition checks whether the robot is there:
  
  	```cpp

    if (row == robot.row && column == robot.column) {
        std::cout << 'R';
    } else {
        std::cout << maze[row][column];
    }
    ```

    If so, it prints R; otherwise, it prints that position’s maze character. The robot is drawn over the maze for display, but this does not change the original maze.

6. Read the player’s command.
  
	In main, these lines ask for and read a command:
  
  	```cpp

    std::cout << "Command: ";
    std::cin >> command;
    ```

	If the player types `q`, this branch ends the loop:
    
  	```cpp

    if (command == "q") {
        quit = true;
    }
  	```
    
	Any other command is sent to the movement function:
  
  	```cpp

    else if (moveRobot(maze, robot, command)) {
        moveHistory.push_back(command);
    }
   	```
   
7. Work out whether the move is allowed.
   
	In moveRobot, the starting values for the proposed position are copied from the robot:
  
  	```cpp

    int nextRow = robot.row;
    int nextColumn = robot.column;
  	```
    
	The following if and else if statements adjust those temporary coordinates according to the command:
  
  	```cpp

    if (command == "w") {
        nextRow--;
    } else if (command == "s") {
        nextRow++;
    } else if (command == "a") {
        nextColumn--;
    } else if (command == "d") {
        nextColumn++;
    }
  	```

	For example, `w` decreases the row number, moving up; `d` increases the column number, moving right. If the command doesn’t match any of these, the final else reports an unknown command and returns false.

8. Check for a wall before moving.
  
	This line checks the maze square the robot is trying to enter:
  
  	```cpp

    if (maze[nextRow][nextColumn] == '#') {
        std::cout << "There's a wall there. The robot stays put.\n";
        return false;
    }
  	```
    
  	If that square contains #, the function returns false without changing the robot’s coordinates. Otherwise, these lines update the robot and report a successful move to main:
    
    ```cpp

    robot.row = nextRow;
    robot.column = nextColumn;
    return true;
    ```

9. Record only successful moves.
   
	Back in main, the move is added here:
    
    ```cpp

    moveHistory.push_back(command);
    ```

	This line runs only if moveRobot returned true. A wall bump or an unknown command does not get added to the vector.

10. Check whether the robot reached the goal.
    
	After handling the command, the game checks the robot’s current maze position:
    
    ```cpp

    if (maze[robot.row][robot.column] == 'G') {
        printMaze(maze, robot);
        std::cout << "You reached the goal!\n";
        break;
    }
    ```

    If that square contains G, the program displays the maze, prints the win message, and break exits the game loop.

11. Print the number of successful moves.
    
	When the loop ends—because the player quit or reached the goal—this line reports the number of moves in the vector:
    
    ```cpp

    std::cout << "Successful moves: " << moveHistory.size() << "\n";
    ```

12. Try a route to the goal.

	Starting at row 1, column 1, type:
    
    ```text

    d
    d
    d
    d
    s
    s
    a
    ```

    The robot moves right four times to column 5, down twice to row 3, then left onto the goal at row 3, column 4.

> [!NOTE]
>
> How did you do?
>
> If you could not quite get there, then look at the code.
> Ask a friend to see if they can spot anything - a friend will find that missing `;` quicker sometimes.
> Do not think this is cheating, this is how coders work - we ask people if we get stuck.
>

---

## Common Problems

* The robot seems to move through walls: Check that you test `maze[nextRow][nextColumn]` before updating the robot’s position.
* The robot appears in the wrong square: Remember that row comes first and column comes second: `maze[row][column]`.
* Wall bumps count as moves: Add a command to `moveHistory` only when moveRobot returns true.
* The robot disappears from the goal: The printing function draws R on top of the maze, so the robot hides the G while standing on it. The win check still reads G from the original maze.
* The game doesn’t recognize a command: The commands are lowercase single letters: w, a, s, d, and q.

---

## Final Message

Even expert coders make mistakes. A bug is not proof that you can’t code—it’s a clue about what to investigate next. 

Test one part at a time, read the messages carefully, and **keep going**.
