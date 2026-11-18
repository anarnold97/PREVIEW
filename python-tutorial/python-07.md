# Python 7 — Our First Project: Print the Times Tables

## Panel 1 — The project

Picture: Mary stands beside a screen showing multiplication equations from the 1 times table to the 12 times table.

* Mary: “Let’s write a program that prints the times tables from 1 to 12. We’ll use two loops: one to choose the times table, and another to print its equations.”

## Panel 2 — One loop inside another

Picture: Mary draws a large loop around the times tables and a smaller loop inside it around the equations.

* Mary: “The outer loop chooses the table: 1, then 2, then 3, and so on.”

* Mary: “For each table, the inner loop multiplies that number by 1 through 12.”

## Panel 3 — Set up the outer loop

Picture: The screen shows the outer loop counting from 1 to 12.

* Mary: “In Python, `range(1, 13)` gives us the numbers from 1 through 12. It stops before 13.”

Code card:
```python

for table in range(1, 13):
    # Print this table's equations here
```

## Panel 4 — Add the inner loop

Picture: Mary points to a second loop, indented inside the first. A multiplication sign appears between the two loop counters.

* Mary: “The inner loop gives us each multiplier. We multiply table by number to get the answer.”

Code card:
```python

for table in range(1, 13):
    for number in range(1, 13):
        answer = table * number
```

## Panel 5 — Print the equations on one line

Picture: The screen displays one table as a row of equations. Mary points to `end=" "`.

* Mary: “Normally, `print()` moves to a new line afterward. The end argument lets us put spaces at the end instead, so the equations stay on the same line.”

Code card:
```python

for table in range(1, 13):
    for number in range(1, 13):
        answer = table * number
        print(f"{table} x {number} = {answer}", end="   ")
    print()
```

## Panel 6 — Run the program

Picture: Mary runs the program. The first two lines appear on screen.

Screen:
```text

1 x 1 = 1   1 x 2 = 2   1 x 3 = 3   ...   1 x 12 = 12
2 x 1 = 2   2 x 2 = 4   2 x 3 = 6   ...   2 x 12 = 24
```

* Mary: “The `final print()` is outside the inner loop, so it moves to a new line after each times table.”

## Your project

Write and run the complete program:

```python

for table in range(1, 13):
    for number in range(1, 13):
        answer = table * number
        print(f"{table} x {number} = {answer}", end="   ")
    print()
```

## Challenge

Add a blank line between each times table by adding another print() after the existing print().

## Interesting Fact: Hedy Lamarr

### Panel 7 — More than a movie star

Picture: Hedy Lamarr looks at a diagram of a radio signal while composer George Antheil studies a piano roll.

* Mary: “Hedy Lamarr was a movie star and an inventor. During World War II, she and composer George Antheil developed a frequency-hopping idea for radio-controlled torpedoes—a signal that changed frequencies to make it harder to jam.” 


### Panel 8 — An idea that came later

Picture: A timeline shows the invention during the war, then a later military communication system.

* Mary: “Their invention wasn’t used during the war. A version of the idea was later used in military communications, and their work became part of the history of spread-spectrum technology.” 
