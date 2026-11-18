# Python 3 — Variables and Input

## Teaching Python to Remember and Ask

### Panel 1 — The computer remembers

Picture: Andy points to three labeled boxes on a screen: name, age, and favorite_number.

* Andy: “Last time, we gave Python information to display. Now let’s give our program some information to remember.”

* Mary: “Variables are like labeled boxes. Each one has a name and stores a value.”

### Panel 2 — Different kinds of values

Picture: The boxes fill with "Mia", 10, and 7.5.

* Andy: “Text is stored as a string, whole numbers as integers, and numbers with decimals as floats.”

* Mary: “Python figures out the kind of value from what we assign. We don’t have to declare the type first.”

Code card:

```python

name = "Mia"
age = 10
favorite_number = 7.5

print(name, "is", age, "years old.")
```

### Panel 3 — Show what’s in the boxes

Picture: The computer displays: Mia is 10 years old.

* Andy: “We can use variables inside print() to display their values.”

* Mary: “The commas separate the pieces, and print() puts spaces between them.”

### Panel 4 — Ask a question

Picture: The computer displays: What is your name? Mia types her answer.

* Andy: “Programs can get information from the person using them, too.”

* Mary: “Use input() to ask a question and save the answer in a variable.”

Code card:
```python

name = input("What is your name? ")
print("Hello,", name + "!")
```

### Panel 5 — A greeting appears

Picture: Mia presses Enter. The screen displays: Hello, Mia!

* Andy: “The answer Mia typed was stored in the name variable.”

* Mary: “For now, try entering a name without spaces. We’ll learn other ways to read text later.”

## Task 1

Change the program so it asks for the user’s favorite animal. Then print a friendly message using their answer.

## The Programmer and the Shopping List

### Panel 6 — Sam gets an instruction

Picture: Sam’s husband hands Sam a shopping list.

* Husband: “Please pick up a loaf of bread. If the shop has eggs, get a dozen.”

### Panel 7 — A very literal interpretation

Picture: Sam sees eggs at the shop and arrives home carrying twelve loaves of bread.

* Husband: “Twelve loaves?”

* Sam: “The shop had eggs, so I got a dozen!”

### Panel 8 — Clarify the instructions

Picture: They laugh together. Sam writes a clearer list: 1 loaf of bread; 12 eggs.

* Husband: “I meant a dozen eggs!”

* Sam: “Next time, I’ll ask if I’m not sure what you mean.”

* Mary: “Instructions can sometimes mean more than one thing. Computers follow instructions literally, so we need to be clear.”

## Bug Detective: Variables

### Panel 9 — Mystery 1: The name that isn’t there

Picture: Detective Andy examines a program with a magnifying glass. Mary points to name on one line and nme on another.

* Andy: “The program saved the name here…”

* Mary: “…but this line asks for a variable called nme. That name doesn’t exist!”

Code card:
```python

name = "Mia"

print(nme, "says hello!")
```

* Clue from Mary: “Check whether the variable’s name matches everywhere.”

### Panel 10 — Mystery 2: Where did the decimal go?

Picture: Andy finds 7.5 being squeezed into a whole-number box labeled int(). The decimal point falls out.

* Andy: “The program runs, but it displays 7 instead of 7.5.”

* Mary: “int() converts a number to a whole number. Use float() to keep the decimal.”

Code card:
```python

favorite_number = int(7.5)

print("My favorite number is", favorite_number)
```

* Clue from Mary: “Which conversion keeps a decimal part?”

### Panel 11 — Mystery 3: The wrong box is on display

Picture: Mia types her name. The computer replies, Hello, 10! Andy looks surprised.

* Andy: “The program saved the answer in name…”

* Mary: “…but it displays age. That’s the wrong variable!”

Code card:
```python

name = input("What is your name? ")
age = 10

print("Hello,", age, "!")
```

* Clue from Mary: “Which variable holds the answer the user typed?”

### Panel 12 — Detective answer key

Picture: Andy and Mary reveal the fixes on a detective’s board.

* Andy: “Mystery 1: Change nme to name.”

* Mary: “Mystery 2: Change int(7.5) to float(7.5), or just write favorite_number = 7.5.”

* Andy: “Mystery 3: Display name instead of age.”

* Mary: “Great detective work! Check what your program saves—and what it displays.”

## Interesting Fact: The ENIAC Six

### Panel 13 — Programming a giant machine

Picture: Andy and Mary stand beside a room-sized ENIAC computer. The six programmers study diagrams and cables.

* Andy: “ENIAC was an early electronic computer. Programming it meant setting switches and connecting cables—not typing code.”

* Mary: “Six women programmed ENIAC: Jean Jennings Bartik, Kathleen McNulty, Marlyn Meltzer, Betty Snyder Holberton, Frances Bilas Spence, and Ruth Lichterman Teitelbaum.” 

### Panel 14 — Pioneers at work

Picture: The six women work together as ENIAC’s lights glow behind them.

* Andy: “They figured out how to program the machine, helping it calculate artillery trajectories.”

* Mary: “Their work wasn’t widely recognized for many years. Today, they’re celebrated as pioneers in computing.” 

### Panel 15 — First try, next try

Picture: Andy’s program displays an error. He studies it, fixes a variable name, and runs it again.

* Andy: “My program made a mistake.”

* Mary: “Then you’ve got a chance to investigate, fix it, and learn. Debugging is part of programming!”

## End-of-chapter task: Make a program that asks for the user’s name and favorite animal, then prints a sentence using both answers.