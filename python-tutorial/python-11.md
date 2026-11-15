# Tutorial 11 — Project: The Little Treasure Maze

## Panel 1 — A tiny explorer needs help

Visual: Andy and Mary look down at a small maze. A tiny explorer stands near the entrance, with treasures glinting farther inside.

* Andy: A tiny explorer is searching this maze for three treasures!

* Mary: Help them move around, avoid walls, and keep track of the treasures they find.

## Panel 2 — Build the maze

Visual: The maze appears as five rows of boxes. Mary labels empty spaces, walls, and treasures.

* Mary: In Python, we can represent a maze as a list of lists. Each inner list is one row.

Code card:
```python

maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1],
    [1, 0, 1, 2, 1],
    [1, 2, 0, 0, 1],
    [1, 1, 1, 1, 1]
]
```

* Andy: Each number has a meaning: 0 is an empty space, 1 is a wall, and 2 is a treasure.

## Panel 3 — Find the starting position

Visual: The explorer stands in the second row, second column. A coordinate marker reads row 1, column 1.

* Mary: The explorer starts at row 1, column 1. Remember, Python indexes start at 0, so the top-left corner is row 0, column 0.

* Andy: The outside edge is made of walls, so the explorer can’t leave the maze.

## Panel 4 — Draw what the explorer sees

Visual: Andy holds up a display showing symbols for the maze. Mary points to a nested loop.

* Andy: The player should see the maze after every turn. Use P for the explorer, . for an empty space, # for a wall, and T for a treasure.

* Mary: Use nested for loops to visit each row and each space in that row.

Code card — display plan:
```python

for row in maze:
    for space in row:
        # Choose and print the right symbol
        pass
    print()
```

* Andy: The `print()` after the inner loop starts a new line for each row. You’ll also need to check whether each space contains the explorer before printing the maze symbol.

## Panel 5 — Choose a direction

Visual: Four arrows surround the explorer: up, left, down, and right.

* Mary: The player chooses a direction by typing:

    * W to move up
    * A to move left
    * S to move down
    * D to move right

* Andy: Ask again if they enter something else. Python doesn’t have a built-in do-while loop, but while True and break can do the job.

Code card — direction check:
```python

while True:
    direction = input("Choose W, A, S, or D: ").strip().upper()

    if direction in ["W", "A", "S", "D"]:
        break

    print("Please enter W, A, S, or D.")
```

## Panel 6 — Move carefully

Visual: The explorer tries to move right. One square is empty; another is blocked by a wall.

* Andy: Convert the chosen direction into a new row and column. Before moving, check what’s in the destination space.

* Mary: If it’s a wall, keep the explorer where they are. If it’s a treasure, collect it and clear that space in the maze.

Code card — movement hints:
```text
    * Up changes the row by -1.
    * Down changes the row by +1.
    * Left changes the column by -1.
    * Right changes the column by +1.
    * If the destination contains 1, don’t move.
    * If the destination contains 2, add 10 to the treasure-points list, then set that maze space to 0.
```

## Panel 7 — Keep track of the game

Visual: Mary puts three empty treasure slots on a scoreboard. Andy points to a turn counter.

* Mary: Use a 1D list to record points for treasures collected. Start with an empty list:

```python

treasure_points = []
```

* Andy: Each time the explorer finds a treasure, add 10 to the list. The game should keep going until all three treasures are found or the player has used 15 turns.

Code card — game-loop idea:
```python

while len(treasure_points) < 3 and turns < 15:
    # Show the maze
    # Get a valid direction
    # Try to move
    # Collect a treasure, if there is one
    # Count the turn
    pass
```

## Panel 8 — Add up the points

Visual: Andy counts the collected treasure tokens. Mary writes the total on the scoreboard.

* Andy: After the game, use a for loop to add the points together.

Code card — scoring:
```python

total = 0

for points in treasure_points:
    total = total + points

print("Total points:", total)
```

* Mary: Then tell the player whether they found all three treasures or ran out of turns.

## Your mission

Build the game using:

    * A 2D list for the maze.
    * A 1D list for the treasure points.
    * Nested for loops to display the maze row by row.
    * A while loop to play until all three treasures are found or 15 turns are used.
    * A while True loop with break to keep asking until the player enters a valid direction.

When the explorer moves into a wall, leave them in place. When they find a treasure, add its points to the list and remove it from the maze so it can’t be collected twice.

## Bug Detective — Test your maze

Visual: Andy draws a detective board with five checks. Mary inspects the code.*

* Mary: Let’s test one thing at a time:

    * Does the maze print in five rows and five columns?
    * Can the explorer collect a treasure?
    * Does a wall stop the explorer?
    * Does the program reject an invalid direction?
    * Does the game stop after all three treasures are found or after 15 turns?
    * Can a treasure be collected only once?

## Bonus challenge — Play again*

Visual: The explorer emerges from the maze. Andy holds up a sign: “Play again? Y/N”

* Andy: Ask whether the player wants another round. Use while True with break so the program keeps asking until they enter `Y` or `N`.

Mary: If they choose `Y`, start a fresh game with a fresh maze and empty treasure list.
