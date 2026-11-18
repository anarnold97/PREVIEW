# 5 — Repeating Instructions with Loops

## Counting, Asking Again, and Knowing When to Stop

### Panel 1 — Count with a while loop

Picture: Andy watches a counter tick from 1 upward on a computer screen.

* Andy: “A while loop repeats instructions as long as a condition is true.”

* Mary: “It checks the condition before each repeat. Let’s count to five.”

Code card:
```python

count = 1

while count <= 5:
    print(count)
    count += 1
```

### Panel 2 — How the counter works

Picture: Mary points to the code as the numbers 1, 2, 3, 4, and 5 appear.

* Andy: “count = 1 starts the counter at 1.”

* Mary: “count <= 5 means ‘keep going while count is 5 or less.’ And count += 1 adds 1 each time.”

* Andy: “When count becomes 6, the condition is false, so the loop stops.”

* Mary: “Then the computer can have a snack—a byte to eat!”

### Task 1 - 

Change the loop so it counts from 1 to 10.

Picture: Andy reaches toward the keyboard, but Mary pauses him.

* Mary: “Before you change anything else, predict what would happen if we removed count += 1.”

* Andy: “The counter would stay at 1, so count <= 5 would always be true.”

* Mary: “Right. The loop could run forever. Let’s not run that version!”

## Keep Asking Until the Answer Is Big Enough

### Panel 3 — Ask for a number

Picture: The computer asks, Enter 10 or more: Andy types 4.

* Andy: “A while loop can keep asking until the user enters a number that meets a condition.”

* Mary: “We ask once before the loop, then repeat while the number is less than 10.”

Code card:
```python

number = int(input("Enter 10 or more: "))

while number < 10:
    number = int(input("Try again—enter 10 or more: "))

print("Great—you entered 10 or more!")
```

### Panel 4 — The loop stops

Picture: Andy enters 4 again, then enters 12. The computer displays: Great—you entered 10 or more!

* Andy: “Since 4 is less than 10, the question repeats.”

* Mary: “When you enter 12, number < 10 is false, so the loop ends.”

## Panel 5 — What about a do while loop?

Picture: Mary draws a loop on the board. It goes through the instructions first, then checks whether to repeat.

* Andy: “C++ has a do while loop that always runs its instructions once before checking the condition.”

* Mary: “Python doesn’t have a built-in do while loop. But we can get the same behavior with while True and break.”

Code card:
```python

while True:
    number = int(input("Enter 10 or more: "))

    if number >= 10:
        break

print("Great—you entered 10 or more!")
```

### Panel 6 — How break works

Picture: Andy enters 4; the question appears again. He enters 12; a stop sign appears beside the loop.

* Andy: “The loop body runs first, so it asks at least once.”

* Mary: “When the number is 10 or more, break stops the loop.”

### Task 2

Run the program and try a number below 10, followed by a number that is 10 or more. Then change it so the program keeps asking until the number is at least 20.

Which Loop Should You Use?

### Panel 7 — Pick the right loop

Picture: Andy and Mary stand beside three doors: for, while, and while True.

* Andy: “Use a for loop when you know how many times you want to repeat something.”

* Mary: “Use a while loop when you want to repeat while a condition is true.”

* Andy: “And use while True with break when you need the loop to run at least once before deciding whether to stop.”

* Mary: “With any loop, make sure there’s a way for it to stop. Otherwise, it may keep running until you stop the program.”

## Bug Detective: Loops

### Panel 8 — Mystery 1: The missing 5

Picture: The screen prints 1, 2, 3, 4, then stops. Andy looks at the empty spot where 5 should be.

* Andy: “This program should print 1 through 5. Why did it stop early?”

* Mary: “Check the condition when count becomes 5.”

Code card:
```python

count = 1

while count < 5:
    print(count)
    count += 1
```

* Clue from Mary: “When count is 5, is count < 5 still true?”

### Panel 9 — Mystery 2: It never asks!

Picture: The program prints Great—you entered 10 or more! before Andy can type anything.

* Andy: “It skipped the question!”

* Mary: “The starting value is 0. Check whether number >= 10 is true at the start.”

Code card:
```python

number = 0

while number >= 10:
    number = int(input("Enter 10 or more: "))

print("Great—you entered 10 or more!")
```

* Clue from Mary: “What is number during the first condition check?”
 
### Panel 10 — Mystery 3: It asks again when you got it right

Picture: Andy enters 12, but the computer immediately asks again.

* Andy: “Twelve is enough. Why is it repeating?”

* Mary: “The loop repeats when its condition is true. Should it repeat when the number is 12?”

Code card:
```python

while True:
    number = int(input("Enter 10 or more: "))

    if number >= 10:
```       

* Clue from Mary: “What condition should make the loop stop?”

### Panel 11 — Mystery 4: The counter is stuck

Picture: The screen displays 1 again and again. Andy notices the counter never changes.

* Andy: “It keeps printing 1!”

* Mary: “The loop needs to update the counter each time.”

Code card:
```python

count = 1

while count <= 3:
    print(count)
```

* Clue from Mary: “What line should you add so count eventually becomes greater than 3?”

### Panel 12 — Detective answer key

Picture: Andy and Mary reveal the fixes on a board.

* Andy: “Mystery 1: Change count `< 5` to count `<= 5`.”

* Mary: “Mystery 2: Use while number < 10, and ask for a number before the loop.”

* Andy: “Mystery 3: Stop when the number is at least 10—for example, with if number >= 10: break.”

* Mary: “Mystery 4: Add count += 1 inside the loop.”

* Andy: “Great detective work!”

## Final challenge

Write a program that asks the user to guess a secret number. Keep asking while the guess is wrong, then print a congratulatory message when they get it right.
