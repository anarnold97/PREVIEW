# Python 2 - HelloWorld

## Your First Python Program

### Panel 1 — Meet Python

Picture: Andy stands beside a computer showing a game, an app, and a robot.

* Andy: “Python is a programming language—a way to give instructions to a computer. People use it to make games, apps, and many other things.”

### Panel 2 — Say hello

Picture: Andy types while Mary looks over his shoulder.

* Andy: “A program is a set of instructions a computer follows. Here’s a tiny Python program.”

```python

print("Hello, world!")
```

### Panel 3 — The result

Picture: The computer displays the words.

Screen:
```text

Hello, world!
```

* Andy: “When we run the program, it displays Hello, world!”

* Mary: “Good example. print() tells Python to show something on the screen.”

### Panel 4 — Try your own message

Picture: Andy changes the message on screen.

* Andy: “Change the words inside the quotation marks to your name or a fun message, then run it again.”

* Mary: “Keep the quotation marks — they show Python that the message is text.”

## Task 1

* Change "Hello, world!" to your name or a fun message. Run the program. What does it display?

## Part Two: Storing Information in Variables


### Panel 5 — A labeled box

Picture: Mary points to a box labeled age with 10 inside.

* Andy: “Programs can remember information using variables. A variable is like a labeled box that holds a value.”

* Mary: “In Python, we create a variable by giving it a name and a value.”

### Panel 6 — Make an age variable

Picture: The code appears on a screen.

```python

age = 10
print(age)
```

* Andy: “Here, age is the variable’s name, and 10 is the value stored in it.”

Screen:

```text

10
```

* Mary: “Python figures out that 10 is a whole number, so we don’t need to write a separate number type here.”

### Panel 7 — Put a variable in a message

Picture: Andy’s program builds a sentence from separate pieces.

```python

age = 10
print("I am", age, "years old.")
```

* Andy: “We can use a variable as part of a message, too.”

Screen:
```text

I am 10 years old.
```

* Mary: “Notice the commas inside print(). They let Python display the text and the value together, with spaces between them.”

## Task 2

Change 10 to another number and run the program. What does it display?


## Interesting Fact: Grace Hopper

### Panel 8 — Making computers easier to program

Picture: Grace Hopper stands beside an early computer while long strings of 1s and 0s fill the background.

* Andy: “Early computers worked with instructions written very close to machine code. Grace Hopper believed programming could be made easier for people to read and write.”

* Mary: “She helped develop early compilers—tools that translate programming instructions into forms a computer can use.” Smithsonian Institution

### Panel 9 — The famous moth

Picture: Engineers inspect a computer relay. Someone spots a moth and carefully records it in a logbook.

* Andy: “In 1947, the Mark II computer team found a moth stuck in a relay and taped it into a logbook.”

* Mary: “The logbook called it the ‘first actual case of bug being found.’ The word bug was already used for technical problems, but this story helped make the phrase famous.” 

* Andy: “We’ll learn more about Grace Hopper in a later interesting fact. COS WE LOVE GRACE!”

* Mary: "Yeah we really do."

## Bugs

### Panel 10 — What’s a bug?

Picture: Andy and Mary examine a program with a magnifying glass. A cartoon bug hides beside the code.

* Andy: “A bug is a mistake in a program that can make it behave unexpectedly or stop working.”

* Mary: “Finding and fixing bugs is called debugging. Every coder finds them—then tests, learns, and improves their code.”

## Bug Detective Challenge

### Panel 11 — The mystery begins

Picture: Andy puts on a detective hat; Mary holds a clue card.

* Andy: “Detective hats on! Each program below has one sneaky mistake. Run them one at a time and solve the case.”

* Mary: “One program has a mistake in its punctuation, one has a misspelled command, and one runs but prints the wrong message.”

### Mystery 1: Python is grumbling

```python

print("Hello, world!"
```

* Clue from Mary: “Check that every opening parenthesis has a closing one.”

### Mystery 2: “What is prnt?”

```python

prnt("Hello, world!")
```

* Clue from Mary: “Check the spelling of the command that displays text.”

### Mystery 3: It said hello… sort of

```python

print("Hello world!")
```

* Clue from Mary: “Compare the message carefully with Hello, world!.”

## Panel 12 — Detective answer key

Picture: Andy and Mary reveal the fixes on a board.

* Andy: “Mystery 1: Add the missing ).”

* Mary: “Mystery 2: Change prnt to print. 

* Andy: "Mystery 3: Add the missing comma inside the message.”

* Mary: “Great detective work! Every bug you find is a chance to learn.”
