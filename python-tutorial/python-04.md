# Python 4 — Making Choices with if

## Teaching a Program to Decide

### Panel 1 — A program asks a question

Picture: Andy and Mary look at a computer screen asking, How old are you?

* Andy: “Programs can make choices by checking whether something is true.”

* Mary: “In Python, an if statement tells the program what to do when a check is true.”

### Panel 2 — Get the age

Picture: Andy types an age. Mary points to int() in the code.

* Andy: “input() gives us text. Since we want to compare an age as a number, we convert the answer with int().”

Code card:
```python

age = int(input("How old are you? "))
```

### Panel 3 — Make a choice

Picture: The screen shows a fork in a path: one sign says 10 or older, the other younger than 10.

* Andy: “The symbol `>=` means ‘greater than or equal to.’”

* Mary: “So age `>= 10` is true when the age is 10 or more.”

Code card:
```python

if age >= 10:
    print("You are 10 or older!")
else:
    print("You are younger than 10.")
```

### Panel 4 — Follow the matching path

Picture: One path lights up when the age is 12; the other lights up when the age is 8.

* Andy: “If the condition is true, Python runs the indented lines under if.”

* Mary: “Otherwise, it runs the lines under else. In Python, indentation shows which instructions belong together.”

### Panel 5 — True or false?

Picture: Mary holds up two cards: True and False.

* Mary: “A check like age `>= 10` has a Boolean result: it’s either `True` or `False`.”

* Andy: “Python’s Boolean values are spelled with capital letters: `True` and `False`.”

Code card:
```python

is_sunny = True
is_raining = False
```

### Task 1

Change 10 to another number, or change the messages. Try ages on both sides of the number you chose.

### Task 2

Change the program so it checks whether a number is at least 18. Test a number below 18 and one that is 18 or above.

## Infinite Loops

### Panel 6 — The loop that won’t stop

Picture: Andy and Mary watch a cartoon game character run around the same track again and again.

* Andy: “A loop repeats instructions. An infinite loop keeps repeating because it never reaches a stopping point.”

* Mary: “It’s like a game that keeps going until someone stops it.”

Code card:
```python

while True:
    print("Still going!")
```

* Mary: “This example really does keep printing. If you run it, stop it with your editor’s stop button or Ctrl+C.”

## Bug Detective: Making Choices

### Panel 7 — The mystery begins

Picture: Andy puts on a detective hat. Mary holds up three clue cards.

* Andy: “Detective hats on! Each program is deciding whether someone is 10 or older—but one sneaky bug is causing trouble.”

* Mary: “Run each program separately. For each mystery, try the age shown in the clue.”

### Panel 8 — Mystery 1: What about exactly 10?

Picture: The program checks an age of 10, but sends it down the younger path.

* Andy: “The message says ‘10 or older,’ but the program didn’t choose it!”

* Mary: “`>` means greater than. Does that include exactly 10?”

Code card:
```python

age = 10

if age > 10:
    print("You are 10 or older!")
else:
    print("You are younger than 10.")
```

* Clue from Mary: “Which comparison includes numbers equal to 10?”

### Panel 9 — Mystery 2: Backwards answers

Picture: The program checks the age 8, then displays You are 10 or older! Andy looks puzzled.

* Andy: “The check looks right for age 8…”

* Mary: “…but the messages in the two branches are the wrong way around.”

Code card:
```python

age = 8

if age >= 10:
    print("You are younger than 10.")
else:
    print("You are 10 or older!")
```

* Clue from Mary: “The condition is fine. Do the messages match the if and else branches?”

### Panel 10 — Mystery 3: Exactly 10—or 10 and older?

Picture: Someone enters 12, but the program says they are younger than 10.

* Andy: “Twelve is older than ten. Why did the program choose else?”

* Mary: “Because `==` checks whether the age is exactly 10—not whether it is 10 or more.”

Code card:
```python

age = 12

if age == 10:
    print("You are 10 or older!")
else:
    print("You are younger than 10.")
```

* Clue from Mary: “Which comparison also includes ages above 10?”

### Panel 11 — Detective answer key

Picture: Andy and Mary reveal the fixes on a board.

* Andy: “Mystery 1: Change age > 10 to age >= 10.”

* Mary: “Mystery 2: Swap the two messages so each matches its branch.”

* Andy: “Mystery 3: Change age == 10 to age >= 10.”

* Mary: “Great detective work! Test different values to check both paths.”

## Interesting Fact: Katherine Johnson

### Panel 12 — Checking a spacecraft’s path

Picture: Katherine Johnson works with calculations while a spacecraft travels along a curved path around Earth.

* Andy: “Katherine Johnson was a mathematician whose calculations helped make early spaceflight possible.”

* Mary: “After electronic computers were introduced, astronaut John Glenn asked for Katherine to check the computer’s calculations before his 1962 orbital flight.” 
Space

### Panel 13 — Check the numbers

Picture: Katherine checks a stack of calculations. In the background, Glenn prepares for the flight.

* Andy: “Glenn reportedly said, ‘Get the girl to check the numbers. If she says the numbers are good, I am ready to go.’”

* Mary: “Katherine’s calculations also contributed to later space missions, including the Apollo program.” Space

### Panel 14 — Test both paths

Picture: Andy tests his if program with two ages. Mary checks the results beside him.

* Andy: “I tested an age below 10 and one above it.”

* Mary: “And don’t forget exactly 10! Testing the boundary helps catch mistakes.”

* Caption: “Check your conditions, test each path, and make sure the messages match.”
