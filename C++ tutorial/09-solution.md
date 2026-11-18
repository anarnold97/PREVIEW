# Introduction to C++ (Part 9 solution)

## Solution: The Little Treasure Maze

```cpp

#include <iostream>

int main() {
    int maze[5][5] = {
        {1, 1, 1, 1, 1},
        {1, 0, 2, 0, 1},
        {1, 0, 1, 2, 1},
        {1, 2, 0, 0, 1},
        {1, 1, 1, 1, 1}
    };

    int treasurePoints[3] = {0, 0, 0};
    int treasuresFound = 0;
    int turns = 0;

    int playerRow = 1;
    int playerColumn = 1;

    // Keep playing while treasures remain and turns are available.
    while (treasuresFound < 3 && turns < 15) {
        // Print the maze.
        for (int row = 0; row < 5; row++) {
            for (int column = 0; column < 5; column++) {
                if (row == playerRow && column == playerColumn) {
                    std::cout << "P ";
                } else if (maze[row][column] == 1) {
                    std::cout << "# ";
                } else if (maze[row][column] == 2) {
                    std::cout << "T ";
                } else {
                    std::cout << ". ";
                }
            }
            std::cout << "\n";
        }

        std::cout << "Treasures found: " << treasuresFound << " of 3\n";
        std::cout << "Turns remaining: " << 15 - turns << "\n";

        // Ask until the player enters a valid direction.
        char direction;
        do {
            std::cout << "Move with W (up), A (left), S (down), or D (right): ";
            std::cin >> direction;
        } while (direction != 'W' && direction != 'A' &&
                 direction != 'S' && direction != 'D');

        // Work out where the player would move.
        int nextRow = playerRow;
        int nextColumn = playerColumn;

        if (direction == 'W') {
            nextRow--;
        } else if (direction == 'A') {
            nextColumn--;
        } else if (direction == 'S') {
            nextRow++;
        } else if (direction == 'D') {
            nextColumn++;
        }

        turns++;

        // Move only if the next space is not a wall.
        if (maze[nextRow][nextColumn] == 1) {
            std::cout << "There's a wall there! You stay where you are.\n";
        } else {
            playerRow = nextRow;
            playerColumn = nextColumn;

            // Collect a treasure if the player landed on one.
            if (maze[playerRow][playerColumn] == 2) {
                treasurePoints[treasuresFound] = 10;
                treasuresFound++;
                maze[playerRow][playerColumn] = 0;

                std::cout << "You found a treasure worth 10 points!\n";
            }
        }

        std::cout << "\n";
    }

    // Print the final maze.
    std::cout << "Final maze:\n";
    for (int row = 0; row < 5; row++) {
        for (int column = 0; column < 5; column++) {
            if (row == playerRow && column == playerColumn) {
                std::cout << "P ";
            } else if (maze[row][column] == 1) {
                std::cout << "# ";
            } else if (maze[row][column] == 2) {
                std::cout << "T ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << "\n";
    }

    // Add up the points in the treasure array.
    int totalPoints = 0;
    for (int i = 0; i < treasuresFound; i++) {
        totalPoints += treasurePoints[i];
    }

    std::cout << "You found " << treasuresFound << " treasure(s).\n";
    std::cout << "Your total score is " << totalPoints << " points.\n";

    if (treasuresFound == 3) {
        std::cout << "You found every treasure. Great exploring!\n";
    } else {
        std::cout << "Time's up! Try the maze again to find the rest.\n";
    }

    return 0;
}
```

### Walk-through

* Set up the maze: `maze[5][5]`` is a 2D array. The numbers mark empty spaces, walls, and treasures. The player’s starting position is `row 1, column 1`.

* Set up the treasure array: `treasurePoints` is a regular, one-dimensional array with room for three treasures. Each treasure is worth 10 points. `treasuresFound` keeps track of how many have been collected.

* Start the game loop: The `while` loop continues as long as the player has not found all three treasures and has turns left.

* Print the maze: The nested for loops visit every row and column. They print `P` for the player, `#` for a wall, `T` for a treasure, and `.` for an empty space.

* Check the direction: The `do-while` loop asks for a direction at least once. If the player enters something other than `W`, `A`, `S`, or `D`, it asks again.

* Plan the move: `nextRow` and `nextColumn` start at the player’s current position. The direction changes one of them to show where the player wants to go.

* Move or stay put: If the next space is a wall, the player stays where they are. Otherwise, the player moves there. A treasure is added to treasurePoints, and its spot in the maze becomes empty.

* Finish the game: When the game ends, a for loop adds the collected treasure points. The program then prints the player’s total score and whether they found all the treasures.


If you didn’t solve the project on your own, don’t worry! Projects take practice, and reading through a solution is one way to learn how the pieces fit together. Try changing the maze or the turn limit, then run the program again.

Remember, you just found a way that did not work.

These are all simple things to miss when you’re learning. If your game didn’t work right away, that’s normal—try checking these one at a time:

* Lots of new ideas: This project uses several things you’ve learned. You can build it in small steps instead of doing everything at once. Work with a friend to support each other.

* Rows and columns: It’s easy to mix them up. In `maze[row][column]`, the row comes first and the column comes second.

* Loop limits: Check that your loops visit every row and column. A small change to a loop’s stopping number can leave some out.

* Array indexes: Indexes start at `0`. For example, a three-item array uses indexes 0, 1, and 2.

* The do-while check: It repeats while the answer is invalid. Try testing the condition with one valid letter and one invalid letter.

* Uppercase and lowercase letters: This version accepts uppercase W, A, S, and D. Lowercase letters won’t work unless you change the program.

* Moving into walls: Check whether the next space is a wall before changing the player’s position.

* Counting turns: In this version, trying to move into a wall still uses a turn. That’s a simple rule to overlook.

* Collecting treasures: Remember to add the points, increase the treasure count, and remove the treasure from the maze.

* Printing the maze: Start by printing just the numbers. Then add the symbols for the player, walls, treasures, and empty spaces.

* Tiny typing mistakes: A missing semicolon, brace, or quotation mark can stop the program from compiling. Those are easy mistakes to make, even for experienced programmers.

* If the whole project feels too big, begin with just one goal: make the maze print correctly. Build your code slowly,

Take it one step at a time. Every bug you find is a clue that helps you learn.

You are learning, that is the thing to take away. And if you are trying this project you are **not learning to code**, you **ARE** coding.

---

## I done a stupid

Ask any coder "what is the most stupid thing you have ever done" and the answers will surprise you:

* Number 1 *done a stupid* - the code would not run, the coder changed it, and changed it again ... hours and hours of debugging, and the coder realized they had not saved their code. DOH!

* Number 2 *done a stupid* - this is a common one and every coder has done this (and if they say they have not - then they are lying) and spent hours looking for a major problem only to realize that we had missed a semi-colon. My personal record is six hours.

* Number 3 *done a stupid* - mis-spelled a variable, simple error, but the problems are huge and if you do not check your variables then it is impossible to spot quickly. 
