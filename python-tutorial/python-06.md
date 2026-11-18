# Python 6 — Project: FizzBuzz

## Andy’s First Counting Game

### Panel 1 — A classic beginner project

Picture: Andy stands beside a screen showing numbers turning into “Fizz,” “Buzz,” and “FizzBuzz.”

* Andy: “FizzBuzz is one of the first programs I write when I’m learning a new language.”

* Andy: “It’s a small game, but it lets us practice a lot at once: loops, conditionals, comparisons, remainder, and printing.”

### Panel 2 — The rules

Picture: Andy points to a list of numbers from 1 to 30.

Andy: “We’ll count from 1 to 30. For each number:

    * If it divides evenly by both 3 and 5, print FizzBuzz.
    * Otherwise, if it divides evenly by 3, print Fizz.
    * Otherwise, if it divides evenly by 5, print Buzz.
    * If none of those rules apply, print the number.”

### Panel 3 — Find the remainder

Picture: Andy uses a calculator. `10 % 5` shows `0`; `11 % 5` shows `1`.

* Andy: “In Python, `%` gives us the remainder. If the remainder is zero, the number divides evenly.”

Code card:
```python

10 % 5 == 0  # True
11 % 5 == 0  # False
```

### Panel 4 — Compare and combine checks

Picture: Andy points to == and and on a whiteboard.

* Andy: “`==` asks whether two values are equal. One equals sign, =, assigns a value; two, ==, compare values.”

* Andy: “And and means both checks must be true.”

### Panel 5 — Count from 1 to 30

Picture: Andy types a loop, and a counter moves from 1 toward 30.

* Andy: “A `for` loop with range(1, 31) visits the numbers from 1 through 30. Python stops before the second number in `range()`.”

Code card:
```python

for number in range(1, 31):
    print(number)
```

### Panel 6 — Add the FizzBuzz rules

Picture: Andy’s screen shows 15 turning into “FizzBuzz.” A thought bubble shows that 15 divides evenly by both 3 and 5.

* Andy: “Check for numbers divisible by both 3 and 5 first. Otherwise, 15 would match the rule for 3 first, and the program would print only Fizz.”

Code card:
```python

for number in range(1, 31):
    if number % 3 == 0 and number % 5 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)
```

### Panel 7 — Run the game

Picture: Andy runs the program. The screen fills with numbers and words.

* Andy: “That’s the whole game! The if, elif, and else statements choose what to print for each number.”

Sample results:
```text

3  → Fizz
5  → Buzz
15 → FizzBuzz
16 → 16
```

* Mary: “Nice example, Andy! FizzBuzz is a great way to practice loops and conditionals.”

### Task 1

Run the program. Check what it prints for 3, 5, 15, and 16.

##Extra challenge

Change the game so it counts to 50, or invent your own words and numbers.

## Bug Detective Challenge

### Panel 8 — Mystery 1: Where did FizzBuzz go?

Picture: Andy tests the number 15. The program prints Fizz, and “FizzBuzz” is still waiting in line.

* Andy: “Fifteen matches the rule for 3, so the program stops checking before it reaches the FizzBuzz rule.”

Code card:
```python

number = 15

if number % 3 == 0:
    print("Fizz")
elif number % 5 == 0:
    print("Buzz")
elif number % 3 == 0 and number % 5 == 0:
    print("FizzBuzz")
else:
    print(number)
```

* Clue from Andy: “The program takes the first matching branch. Which check should come first?”

### Panel 9 — Mystery 2: The missing number

Picture: Andy’s program counts up to 29, but 30 never appears.

* Andy: “It should count through 30. Look carefully at the end of the `range()`.”

Code card:
```python

for number in range(1, 30):
    print(number)
```

* Clue from Andy: “`range()` stops before its ending value. What ending value includes 30?”

### Panel 10 — Mystery 3: The wrong kind of math

Picture: The program checks whether 3 divides by 3, but Andy’s code checks the answer of the division instead of its remainder.

* Andy: “This should print Fizz for 3. Which operator checks what’s left over?”

Code card:
```python

number = 3

if number / 3 == 0:
    print("Fizz")
else:
    print(number)
```

* Clue from Andy: “/ divides. Use the operator that finds the remainder.”

### Panel 11 — Detective answer key

Picture: Andy writes the fixes on a board.

* Andy: “Mystery 1: Put the check for both 3 and 5 before the individual checks.”

* Andy: “Mystery 2: Change `range(1, 30)` to `range(1, 31)`.”

* Andy: “Mystery 3: Change `/` to `%`.”

* Andy: “If your output is wrong, test one number at a time. That’s how I learn a new language—and how I find the bug.”
