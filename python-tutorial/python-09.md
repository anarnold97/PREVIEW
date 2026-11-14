# Tutorial 9 — For Loops: Looping the Smart Way

## Panel 1 — We've met for before

Visual: Andy points to a FizzBuzz poster and a times-table chart. Mary holds a magnifying glass over a line of code.

Caption: We've been using for loops all along. Remember FizzBuzz and the times tables? Now let's really understand how they work—and how to use them with more than just numbers. By the end, you'll be able to loop through a collection of items, build a total as you go, and choose between for and while.

* Andy: In FizzBuzz, for visited numbers. In the times-table project, it visited rows and columns.

* Mary: So a for loop repeats its instructions for each value it gets.

## Panel 2 — One-argument range()

Visual: Five numbered stepping stones: 0, 1, 2, 3, 4. A sign says "Stop before 5!"

* Andy: With one argument, range(5) starts at zero and stops before five.

* Mary: That gives us five numbers: 0, 1, 2, 3, 4.

```
for number in range(5):
    print(number)
```

> [!NOTE]
>
> Bug Detective callback:
> 
> In Tutorial 6, we investigated range(1, 30). It starts at 1 and stops before 30—so 30 isn't included.

## Panel 3 — Stepping through

Visual: Andy hops along a number line in jumps of three. Mary points to an arrow running backward.

* Andy: `range()` can take three arguments: a *start*, a *stop*, and a *step*.

```
for number in range(1, 13, 3):
    print(number)
```

* Mary: That prints 1, 4, 7, 10. Each step adds 3, and the loop stops before 13.

* Andy: A negative step counts backward:

```
for number in range(5, 0, -1):
    print(number)
```

* Mary: That prints 5, 4, 3, 2, 1. The stop value is still excluded.

### Task 1 — Even numbers

Use one call to `range()` to print the even numbers from 2 through 20.

* **Hint:** Think about the start, the stop, and how far to step each time.

## Part Two: Looping over a list

### Panel 4 — A row of labeled boxes

Visual: Three boxes in a row, labeled animals. Inside them are "cat," "dog," and "fox."

* Mary: In Tutorial 3, we described a variable as a labeled box. A list is like a labeled row of boxes: it can hold several items in order.

```
animals = ["cat", "dog", "fox"]
```

* Andy: The variable animals refers to the whole list. The list contains three strings.

### Panel 5 — How long is a list?

Visual: Mary counts the boxes on her fingers and holds up a card that says 3.

* Mary: Python has a built-in function that tells you how many items are in a list: len().

```
animals = ["cat", "dog", "fox"]
print(len(animals))
```

* Andy: That prints 3. We'll use `len()` soon — both for checking answers and in a Bug Detective mystery.

### Panel 6 — The loop variable gets each item

Visual: A spotlight moves from the "cat" box to "dog," then "fox." Andy holds a card labeled animal.

* Andy: Here's the heart of looping over a list:

```
for animal in animals:
    print(animal)
```

* Mary: Python takes each item from animals, one at a time, and puts it in animal. First "cat", then "dog", then "fox".

* Andy: No counter needed. The loop hands you each element in turn.

### Panel 7 — Give your loop variable a useful name

Visual: Mary compares two labels: a tiny "x" tag and a clear "animal" tag.

* Mary: This works, but it's not very descriptive:

```
for x in animals:
    print(x)
```

* Andy: This is easier to read:

```
for animal in animals:
    print(animal)
```

* Mary: A good name tells readers what the loop variable represents.

## Task 2 — Greet your friends

Make a list of friends' names, then use a for loop to print a greeting for each one.

Example output:

```
Hello, Sam!
Hello, Priya!
Hello, Jordan!
```

## Part Three: Building results as you go

### Panel 8 — The accumulator

Visual: Mary drops numbers into a jar marked total. Andy points to the indentation inside the loop and then to a print statement below it.

* Andy: A loop can build a result as it goes. A variable that keeps a running result is called an accumulator.

```
numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number

print(total)
```

* Mary: The loop adds each number to total. After the loop finishes, total is 13.

* Andy: Notice the indentation: the addition is inside the loop, but print(total) is outside. It runs once, after all the numbers have been added.

### Panel 9 — Which loop should you choose?

Visual: Three doors: one marked "For: visit each item," one marked "While: keep checking," and one marked "Run once, then decide."

* Mary: Let's revisit the loop-choice doors from Tutorial 5.
    
    * Use a `for` loop when you're going through a collection or a known sequence of values.
    * Use a `while` loop when repeating depends on a condition.
    * Use `while True` with `break` when the loop should run at least once before deciding whether to stop.

* Andy: Pick the loop that matches the job.

## Bug Detective: For Loops

Visual: Andy pins three code samples to a detective board. Mary studies them through a magnifying glass.

### Mystery 1 — The missing last friend

```
names = ["Sam", "Priya", "Jordan"]

for index in range(0, len(names) - 1):
    print(names[index])
```

* Andy: The program should greet everyone—but Jordan never gets a turn. Why?

* Mary: `len(names)` is 3, so `range(0, 2)` gives us 0 and 1. And remember: `range()` stops before its stop value.

* **Clue:** The indexes of this list are 0, 1, and 2. The loop never reaches index 2.

* **Fix:** If you want every name, loop over the list directly—no indexes, no off-by-one worries:

```
for name in names:
    print(name)
```

### Mystery 2 — The total that won't stop printing

```
numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number
    print(total)
```

* Andy: The addition is fine. Why does the program print several totals instead of just one?

* **Clue:** `print(total)` is indented inside the loop, so it runs once per number.

* **Fix:** Move the print statement outside the loop:

```
for number in numbers:
    total = total + number

print(total)
```

### Mystery 3 — The overwritten loop variable

```
animals = ["cat", "dog", "fox"]

for animal in animals:
    animal = "owl"
    print(animal)
```

* Mary: We wanted to print every animal in the list. What does this program actually print?

* Andy: "owl" — three times! The assignment replaces the loop variable's value before we print it.

* **Clue:** Assigning to animal overwrites the value the loop just handed us. The list itself is untouched—the next iteration still receives the next real item.

* **Fix:** Keep the loop variable for the loop's value, and use a different name if you need a separate value:

```
for animal in animals:
    print(animal)
```

* Mary: A related prediction puzzle: what if the assignment came after the print? The output would look correct—this time. Overwriting a loop variable is a trap waiting for the next change to the code, so it's a habit worth avoiding even when it doesn't cause a visible bug.

### Detective-board answer key:

* Check where the loop starts and where range() stops, inspect indentation, and don't overwrite a loop variable while you're using it. When possible, looping directly over a list's items keeps the code clear.

## Interesting Fact: Jean Sammet

Visual: Jean Sammet works at an early computer, with handwritten notes and punch cards nearby.

* Andy: Jean Sammet was a mathematician who became a programmer and worked in computing during the 1950s—one of the few women in the field at the time.

Visual: Two language name cards, FORMAC and COBOL, appear beside a sign that reads "Readable code helps people communicate."

* Mary: At IBM, she helped create FORMAC, a language for symbolic mathematics, and supervised the development of COBOL, a programming language designed to be readable—even by people who weren't programmers.

* Andy: That connects to one of our big ideas: clear, readable code helps people understand what a program is doing.

* Mary: Yes Andy... make your code readable! (rolls eyes and giggles)

Visual: A conference badge reading "History of Programming Languages" hangs beside a portrait of Jean.

* Mary: She also organized the first conference on the history of programming languages, helping preserve the stories of how languages like ours came to be.

## Final Challenge — Animal roll call

* Mary: Time to combine lists, loops, input(), and counting.

Write a program that:

* Asks the user to type the names of three animals.
* Stores those names in a list.
* Uses a for loop to print each animal followed by "is a great animal!".
* Finishes by printing how many animals were entered.

* **Hint:** Start with an empty list, use `input()` three times to collect the names, and use `len()` —which we met in Panel 5 — to count the items.

Example output might look like this:

```
cat is a great animal!
dog is a great animal!
fox is a great animal!
You entered 3 animals.
```
