# Python 8 — Times Tables: The Solution

## How did you do?

Picture: Mary gives the reader a cheerful thumbs-up beside a screen showing rows of times tables.

* Mary: “If you managed it—well done! If you didn’t, don’t worry. Nested loops take practice. You’re learning some pretty advanced logic, and even experienced programmers sometimes need to trace a program step by step.”

### The solution

Code card:
```python

for table in range(1, 13):
    for multiplier in range(1, 13):
        answer = table * multiplier

        print(f"{table} x {multiplier} = {answer}", end="   ")

    print()
```

#### How it works

Panel 1 — The outer loop chooses a table

Picture: Mary points to a counter moving from 1 to 12.

* Mary: “The outer loop chooses which times table to print.”

Code card:
```python

for table in range(1, 13):
```

* Mary: “range(1, 13) gives us the numbers 1 through 12. Python stops before 13.”

##### Panel 2 — The inner loop prints its equations

Picture: For the 3 times table, the inner counter moves through 1, 2, 3, and onward to 12.

* Mary: “For each value of table, the inner loop makes multiplier count from 1 to 12.”

Code card:
```python

for multiplier in range(1, 13):
```

##### Panel 3 — Calculate the answer

Picture: Mary shows 3 × 4 becoming 12.

* Mary: “This line multiplies the table number by the multiplier. For example, when table is 3 and multiplier is 4, the answer is 12.”

Code card:
```python

answer = table * multiplier
```

##### Panel 4 — Print one equation at a time

Picture: The screen displays 3 x 4 = 12, followed by a few spaces.

* Mary: “An `f-string` lets us put variable values directly into a message. The end argument adds spaces after each equation instead of moving to a new line.”

Code card:
```python

print(f"{table} x {multiplier} = {answer}", end="   ")
```

##### Panel 5 — Start a new line

Picture: Mary points to the end of the row, where the next times table begins.

* Mary: “This `print()` is outside the inner loop, so it runs after all 12 equations have been printed. It moves us to a new line before the next times table begins.”

Code card:
```python

    print()
```

### Panel 6 - Challenge solution — Add a blank line

Picture: A blank line appears between each times table.

* Mary: “To add a blank line after each table, add one more print() after the existing one.”

```python

for table in range(1, 13):
    for multiplier in range(1, 13):
        answer = table * multiplier
        print(f"{table} x {multiplier} = {answer}", end="   ")

    print()
    print()
```

* Mary’s note: “If it didn’t click right away, that’s okay. Try tracing the loops one step at a time: hold table at 1 while multiplier counts from 1 to 12, then move table to 2 and repeat. Tracing a program is a useful debugging skill.”

## Interesting fact: Sophie Wilson

### Panel 6 — Building a computer in a week

Picture: Sophie Wilson and Steve Furber work on a computer prototype, with a calendar showing the week passing.

* Mary: “Sophie Wilson and her colleague Steve Furber helped design and build the prototype that became the BBC Micro in less than a week. Sophie also designed its operating system and wrote its BASIC interpreter.” 

### Panel 7 — Designing ARM

Picture: Mary holds up a tiny processor chip beside pictures of a phone, a tablet, and other devices.

* Mary: “Sophie Wilson and Steve Furber also co-designed the ARM processor. ARM processor designs are used in many kinds of devices, including phones and tablets.” 

* Mary: “It’s a reminder that hardware and code work together—and you don’t have to build something huge to make a big difference. A tiny chip can help power a whole lot of cat videos!”