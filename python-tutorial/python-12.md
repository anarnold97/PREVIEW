# Tutorial 12 — Project Solution: The Little Treasure Maze

## Panel 1 — Andy and Mary return to the maze

Visual: Andy and Mary stand beside the maze. The explorer waits at the entrance while three treasures sparkle inside.

* Andy: Let’s put the pieces together: a maze made from a list of lists, a treasure-points list, loops, and direction input.

* Mary: We’ll count a move into a wall as a turn, just like the puzzle rules say.

## Panel 2 — Set up the game

Visual: Mary labels the maze rows and columns. Andy places three empty score tokens beside it.

* Mary: The maze is a 2D list. The treasure-points list has room for three treasures, each worth 10 points.

Code card — setup:
```python

maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1],
    [1, 0, 1, 2, 1],
    [1, 2, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

treasure_points = [0, 0, 0]
treasures_found = 0
turns = 0

player_row = 1
player_column = 1
```

* Andy: The explorer starts at row 1, column 1. In `maze[row][column]`, the `row` comes first.

## Panel 3 — Start the game loop

Visual: A large loop surrounds the maze. One sign says “Treasures found: 3”; another says “Turns used: 15.”

* Andy: Keep playing while there are treasures left and turns available.

Code card — loop condition:
```python

while treasures_found < 3 and turns < 15:
```

## Panel 4 — Print the maze

Visual: Andy and Mary scan each row, then each space in the row. The explorer appears as `P`, walls as `#`, treasures as `T`, and empty spaces as `.`.

* Mary: The nested loops visit every row and column. We check the player’s position first so the explorer is drawn over the maze space.

Code card — display the maze:
```python

    for row in range(5):
        for column in range(5):
            if row == player_row and column == player_column:
                print("P", end=" ")
            elif maze[row][column] == 1:
                print("#", end=" ")
            elif maze[row][column] == 2:
                print("T", end=" ")
            else:
                print(".", end=" ")
        print()
```

## Panel 5 — Ask for a valid direction

Visual: Four arrows show W, A, S, and D. Mary holds up a sign: “Try again if the direction isn’t valid!”

* Andy: Python doesn’t have a built-in do-while loop. We can use `while True` and `break` to ask at least once and keep asking until the input is valid.

Code card — validate input:
```python

    print(f"Treasures found: {treasures_found} of 3")
    print(f"Turns remaining: {15 - turns}")

    while True:
        direction = input(
            "Move with W (up), A (left), S (down), or D (right): "
        ).strip().upper()

        if direction in ["W", "A", "S", "D"]:
            break

        print("Please enter W, A, S, or D.")
```

* Mary: .upper() lets lowercase input work too. The loop accepts only W, A, S, or D.

## Panel 6 — Plan the move

Visual: The explorer considers one step in each direction. A tiny map shows rows changing for up and down, and columns changing for left and right.

* Andy: Start by treating the next position as the current position. Then adjust the row or column based on the direction.

Code card — calculate the next position:
```python

    next_row = player_row
    next_column = player_column

    if direction == "W":
        next_row -= 1
    elif direction == "A":
        next_column -= 1
    elif direction == "S":
        next_row += 1
    elif direction == "D":
        next_column += 1

    turns += 1
```

* Mary: We add a turn after every valid move choice—even if a wall blocks the explorer.

## Panel 7 — Move or stay put

Visual: The explorer walks toward a wall, stops, then steps onto a treasure. Mary replaces the collected treasure with an empty-space marker.

* Andy: Check for a wall before changing the player’s position. If the explorer reaches a treasure, record the points and clear it from the maze.

Code card — handle the move:
```python

    if maze[next_row][next_column] == 1:
        print("There's a wall there! You stay where you are.")
    else:
        player_row = next_row
        player_column = next_column

        if maze[player_row][player_column] == 2:
            treasure_points[treasures_found] = 10
            treasures_found += 1
            maze[player_row][player_column] = 0

            print("You found a treasure worth 10 points!")

    print()
```

* Mary: Setting the treasure’s maze space to 0 means it can’t be collected a second time.

## Panel 8 — Show the final maze and score

Visual: The game ends. Andy adds the treasure tokens while Mary prints the final maze and score.

* Andy: When the game loop ends, print the final maze and add up the points with a for loop.

Complete solution — code card:
```python

maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1],
    [1, 0, 1, 2, 1],
    [1, 2, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

treasure_points = [0, 0, 0]
treasures_found = 0
turns = 0

player_row = 1
player_column = 1

while treasures_found < 3 and turns < 15:
    # Print the maze.
    for row in range(5):
        for column in range(5):
            if row == player_row and column == player_column:
                print("P", end=" ")
            elif maze[row][column] == 1:
                print("#", end=" ")
            elif maze[row][column] == 2:
                print("T", end=" ")
            else:
                print(".", end=" ")
        print()

    print(f"Treasures found: {treasures_found} of 3")
    print(f"Turns remaining: {15 - turns}")

    # Ask until the player enters a valid direction.
    while True:
        direction = input(
            "Move with W (up), A (left), S (down), or D (right): "
        ).strip().upper()

        if direction in ["W", "A", "S", "D"]:
            break

        print("Please enter W, A, S, or D.")

    # Work out where the player would move.
    next_row = player_row
    next_column = player_column

    if direction == "W":
        next_row -= 1
    elif direction == "A":
        next_column -= 1
    elif direction == "S":
        next_row += 1
    elif direction == "D":
        next_column += 1

    turns += 1

    # Move only if the next space is not a wall.
    if maze[next_row][next_column] == 1:
        print("There's a wall there! You stay where you are.")
    else:
        player_row = next_row
        player_column = next_column

        # Collect a treasure if the player landed on one.
        if maze[player_row][player_column] == 2:
            treasure_points[treasures_found] = 10
            treasures_found += 1
            maze[player_row][player_column] = 0

            print("You found a treasure worth 10 points!")

    print()

# Print the final maze.
print("Final maze:")
for row in range(5):
    for column in range(5):
        if row == player_row and column == player_column:
            print("P", end=" ")
        elif maze[row][column] == 1:
            print("#", end=" ")
        elif maze[row][column] == 2:
            print("T", end=" ")
        else:
            print(".", end=" ")
    print()

# Add up the points for collected treasures.
total_points = 0
for i in range(treasures_found):
    total_points += treasure_points[i]

print(f"You found {treasures_found} treasure(s).")
print(f"Your total score is {total_points} points.")

if treasures_found == 3:
    print("You found every treasure. Great exploring!")
else:
    print("Time's up! Try the maze again to find the rest.")
```

## Panel 9 — Detective notes

Visual: Mary pins bug clues to a board. Andy circles the row and column labels.*

* Mary: If your game doesn’t work right away, that’s normal. Try checking one clue at a time:

    * Rows and columns: In `maze[row][column]`, the row comes first.
    * Indexes: Python indexes start at 0.
    * Loop limits: The maze has five rows and columns, with indexes 0 through 4.
    * Direction input: `.upper()` makes lowercase directions work.
    * Walls: Check the destination space before moving the player.
    * Turns: Trying to move into a wall still uses a turn.
    * Treasure collection: Add points, increase the treasure count, and clear the treasure from the maze.
    * Indentation: Code inside a loop runs each time the loop repeats.

* Andy: If the whole project feels big, build it in small steps. Start by printing the maze, then add movement, walls, treasures, and scoring.

* Mary: Every bug you find is a clue. You’re not just learning to code — you’re coding.
