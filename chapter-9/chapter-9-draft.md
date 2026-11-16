# Tutorial 9 — For Loops: Looping the Smart Way

## (Version 2 — incorporating review)*

---

## Panel 1 — We've met for before

**Visual:** Andy points to a FizzBuzz poster and a times-table chart. Mary holds a magnifying glass over a line of code.

**Caption:** We've been using `for` loops all along. Remember FizzBuzz and the times tables? Now let's really understand how they work — and how to use them with more than just numbers. By the end, you'll be able to loop through a collection of items, build a total as you go, and choose between `for` and `while`.

* **Andy:** In FizzBuzz, `for` visited numbers. In the times-table project, it visited rows and columns.
* **Mary:** So a `for` loop repeats its instructions for each value it gets.

---

## Panel 2 — One-argument range()

**Visual:** Five numbered stepping stones: 0, 1, 2, 3, 4. A sign says "Stop before 5!"

* **Andy:** With one argument, `range(5)` starts at zero and stops before five.
* **Mary:** That gives us five numbers: 0, 1, 2, 3, 4.

```
for number in range(5):
    print(number)
```

* **Mary:** Remember Bug Detective from Tutorial 6? We investigated `range(1, 30)`. It starts at 1 and stops before 30 — so 30 isn't included. Same rule here: `range(5)` stops before 5.
* **Andy:** That "stops before" rule trips everyone up sooner or later. Now you know it before it trips you.

*(QA fix: the Tutorial 6 callback was previously a NOTE block interrupting the flow — folded into Mary's dialogue and given a reason to exist: naming the trip-hazard.)*

---

## Panel 3 — Stepping through

**Visual:** Andy hops along a number line in jumps of three. Mary points to an arrow running backward.

* **Andy:** `range()` can take three arguments: a *start*, a *stop*, and a *step*.

```
for number in range(1, 13, 3):
    print(number)
```

* **Mary:** That prints 1, 4, 7, 10. Each step adds 3, and the loop stops before 13.
* **Andy:** A negative step counts backward:

```
for number in range(5, 0, -1):
    print(number)
```

* **Mary:** That prints 5, 4, 3, 2, 1. The stop value is still excluded.

### Task 1 — Even numbers

Use one call to `range()` to print the even numbers from 2 through 20.

* **Hint:** Think about the start, the stop, and how far to step each time.

Expected output:

```
2
4
6
8
10
12
14
16
18
20
```

*(QA fix: expected output added so learners can self-check, consistent with Task 2.)*

---

## Part Two: Looping over a list

### Panel 4 — A row of labeled boxes

**Visual:** Three boxes in a row, labeled `animals`. Inside them are "cat," "dog," and "fox."

* **Mary:** In Tutorial 3, we described a variable as a labeled box. A list is like a labeled row of boxes: it can hold several items in order.

```
animals = ["cat", "dog", "fox"]
```

* **Andy:** The variable `animals` refers to the whole list. The list contains three strings.
* **Mary:** And lists can be *changed* — you can add, remove, or replace items later. We'll learn how in Tutorial 12. For now, we'll build lists and read them.
* **Andy:** Yes — and if you were wondering whether you can reach in and change one box directly, hold that thought. It's coming.

*(QA fix: mutation question a curious learner will immediately ask — now acknowledged and explicitly deferred to Tutorial 12, so nobody wanders off to try `animals[0] = "owl"` unguided. Adjust the tutorial number to match your syllabus.)*

---

### Panel 5 — How long is a list?

**Visual:** Mary counts the boxes on her fingers and holds up a card that says 3.

* **Mary:** Python has a built-in function that tells you how many items are in a list: `len()`.

```
animals = ["cat", "dog", "fox"]
print(len(animals))
```

* **Andy:** That prints 3. We'll use `len()` soon — both for checking answers and in a Bug Detective mystery.

---

### Panel 6 — The loop variable gets each item

**Visual:** A spotlight moves from the "cat" box to "dog," then "fox." Andy holds a card labeled `animal`.

* **Andy:** Here's the heart of looping over a list:

```
for animal in animals:
    print(animal)
```

* **Mary:** Python takes each item from `animals`, one at a time, and puts it in `animal`. First "cat", then "dog", then "fox".
* **Andy:** No counter needed. The loop hands you each element in turn.

---

### Panel 7 — Give your loop variable a useful name

**Visual:** Mary compares two labels: a tiny "x" tag and a clear "animal" tag.

* **Mary:** This works, but it's not very descriptive:

```
for x in animals:
    print(x)
```

* **Andy:** This is easier to read:

```
for animal in animals:
    print(animal)
```

* **Mary:** A good name tells readers what the loop variable represents. Remember Jean Sammet later in this chapter — readable code helps people communicate.

*(QA fix: forward-link to the Sammet sidebar added so the naming/readability theme is planted before the payoff.)*

---

## Task 2 — Greet your friends

Make a list of friends' names, then use a `for` loop to print a greeting for each one.

Example output:

```
Hello, Sam!
Hello, Priya!
Hello, Jordan!
```

---

## Part Three: Building results as you go

### Panel 8 — The accumulator

**Visual:** Mary drops numbers into a jar marked `total`. Andy points to the indentation inside the loop and then to a print statement below it.

* **Andy:** A loop can build a result as it goes. A variable that keeps a running result is called an *accumulator*.

```
numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number

print(total)
```

* **Mary:** The loop adds each number to `total`. After the loop finishes, `total` is 13.
* **Andy:** Notice the indentation: the addition is *inside* the loop, but `print(total)` is *outside*. It runs once, after all the numbers have been added.
* **Mary:** Now — a prediction before you turn the page. What would happen if that `print(total)` were *inside* the loop instead? How many lines would print, and what would they say?
* **Andy:** Hold your answer. We'll test it in the Bug Detective.

*(QA fix: Panel 8 now foreshadows Mystery 2 with a prediction prompt, turning the mystery into a payoff rather than a repeat.)*

---

### Panel 9 — Which loop should you choose?

**Visual:** Three doors: one marked "For: visit each item," one marked "While: keep checking," and one marked "Run once, then decide."

* **Mary:** Let's revisit the loop-choice doors from Tutorial 5.
    * Use a `for` loop when you're going through a collection or a known sequence of values.
    * Use a `while` loop when repeating depends on a condition.
    * Use `while True` with `break` when the loop should run at least once before deciding whether to stop.
* **Andy:** Pick the loop that matches the job.

---

### Panel 10 — When you need the item *and* its position *(new)*

**Visual:** Mary holds a delivery list with a checkbox beside each name. Andy points to a clipboard numbered 0, 1, 2.

* **Andy:** Our Bug Detective is about to show why looping with indexes can go wrong. But sometimes you genuinely *need* the position — say you want to number the friends in a list: "1. Sam, 2. Priya…"
* **Mary:** For those cases, Python has a tool called `enumerate()`. It hands you each item *and* its position together:

```
for position, name in enumerate(names, start=1):
    print(position, name)
```

* **Andy:** `enumerate()` counts the positions for you — no `len()`, no off-by-one traps.
* **Mary:** Rule of thumb: loop directly over the list when you need the items. Reach for indexes or `enumerate()` only when you need to know *where* you are.

*(QA fix: new panel. The original draft taught index-looping only via a bug, risking the conclusion that indexes are bad. This panel teaches the legitimate use and the safe tool.)*

---

## Bug Detective: For Loops

**Visual:** Andy pins three code samples to a detective board. Mary studies them through a magnifying glass.

### Mystery 1 — The missing last friend

```
names = ["Sam", "Priya", "Jordan"]

for index in range(0, len(names) - 1):
    print(names[index])
```

* **Andy:** The program should greet everyone — but Jordan never gets a turn. Why?
* **Mary:** `len(names)` is 3, so `range(0, 2)` gives us 0 and 1. And remember: `range()` stops before its stop value.
* **Clue:** The indexes of this list are 0, 1, and 2. The loop never reaches index 2.
* **Fix:** If you want every name, loop over the list directly — no indexes, no off-by-one worries:

```
for name in names:
    print(name)
```

* **Andy:** And if you truly needed the position — say, to number the greetings — that's what `enumerate()` in Panel 10 is for. Did your prediction from Panel 8 about Mystery 2 hold?

### Mystery 2 — The total that won't stop printing

```
numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number
    print(total)
```

* **Andy:** The addition is fine. Why does the program print several totals instead of just one? *(Mary asked you to predict this back in Panel 8 — how close were you?)*
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

* **Mary:** We wanted to print every animal in the list. What does this program actually print?
* **Andy:** "owl" — three times! The assignment replaces the loop variable's value before we print it.
* **Clue:** Assigning to `animal` overwrites the value the loop just handed us. The list itself is untouched — the next iteration still receives the next real item.
* **Fix:** Keep the loop variable for the loop's value, and use a different name if you need a separate value:

```
for animal in animals:
    print(animal)
```

* **Mary:** A related prediction puzzle: what if the assignment came *after* the print? The output would look correct — this time. Overwriting a loop variable is a trap waiting for the next change to the code, so it's a habit worth avoiding even when it doesn't cause a visible bug.

### Detective-board answer key:

Check where the loop starts and where `range()` stops; inspect indentation; don't overwrite a loop variable while you're using it. When possible, loop directly over a list's items — and when you need positions, let `enumerate()` do the counting.

---

## Interesting Fact: Jean Sammet

**Visual:** Jean Sammet works at an early computer, with handwritten notes and punch cards nearby.

* **Andy:** Jean Sammet was a mathematician who became a programmer and worked in computing during the 1950s — one of the few women in the field at the time.
* **Mary:** At IBM, she led the team that created FORMAC, a language for symbolic mathematics, and supervised the development of COBOL, a programming language designed to be *readable* — even by people who weren't programmers.
* **Andy:** That connects to one of our big ideas: clear, readable code helps people understand what a program is doing. COBOL wanted non-programmers to read code; Python carries the same flag today.
* **Mary:** Yes Andy… make your code readable! *(rolls eyes and giggles)*

**Visual:** A conference badge reading "History of Programming Languages" hangs beside a portrait of Jean.

* **Mary:** She also organized the first conference on the history of programming languages — HOPL — helping preserve the stories of how our languages came to be.

*(QA fix: "supervised the development of COBOL" tightened to "led the team that created FORMAC… supervised COBOL"; "languages like ours" replaced with an explicit Python-readability lineage; HOPL named.)*

---

## Final Challenge — Animal roll call

* **Mary:** Time to combine lists, loops, `input()`, and counting.

Write a program that:

* Asks the user to type the names of three animals.
* Stores those names in a list.
* Uses a `for` loop to print each animal followed by "is a great animal!".
* Finishes by printing how many animals were entered — can you do it with `len()` *and* with `enumerate()`?

* **Hint:** Start with an empty list, use `input()` three times to collect the names, and use `len()` — which we met in Panel 5 — to count the items.

Example output might look like this:

```
cat is a great animal!
dog is a great animal!
fox is a great animal!
You entered 3 animals.
```

---

## Changelog for this revision

1. Tutorial 6 callback folded into Panel 2 dialogue (was a disruptive NOTE block).
2. Task 1: expected output added for self-checking.
3. Panel 4: list mutability acknowledged and deferred to Tutorial 12.
4. Panel 7: readability theme forward-linked to the Sammet sidebar.
5. Panel 8: prediction prompt added to set up Mystery 2.
6. **New Panel 10:** `enumerate()` — legitimate index use, offsetting the "indexes are bugs" implication of Mystery 1.
7. Bug Detective: cross-references added (Panel 8 ↔ Mystery 1 ↔ Mystery 2).
8. Sammet sidebar: fact-checked phrasing; HOPL named; Python lineage made explicit.
9. Code formatting normalised: fenced blocks for multi-line, inline backticks for tokens.
