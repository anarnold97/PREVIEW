# Tutorial 10 — Indexes: Reaching Inside a List

## Part One: Indexes

### Panel 1 — The index tags

Visual: The row of boxes from Tutorial 9 appears again. The boxes hold 8, 10, 7, and 9; below them, position tags read 0, 1, 2, and 3.

* Caption: In Tutorial 9, we looped over a whole list. Now we'll learn to reach in and grab any single item—and how lists can grow.

```
scores = [8, 10, 7, 9]

print(scores[0])
```

* Mary: Indexes start at 0. A four-item list has indexes 0 through 3, so scores[0] is 8.

### Panel 2 — Reading and changing items

Visual: Mary swaps the 8 in the first box for a 10. Then she points to the last box.

* Andy: An index lets you change an item, too.

```
scores[0] = 10
print(scores[0])
```

* Mary: That replaces the first score. Notice the list still has four items—changing an item doesn't change its length. Adding an item is different, as we'll see in a moment.

* Mary: And here's a handy Python shortcut: scores[-1] means "the last item."

```
print(scores[-1])  # 9
```

### Task 1 — Try an index

Change one score by its index, then print a different score. Next, try:

```
print(scores[4])
```

* Mary: What happens? A list with four items has indexes 0 to 3. There's no item at index 4, so Python raises an IndexError.

## Part Two: Growing lists and choosing the right loop

### Panel 3 — Add to the list

Visual: Andy adds another box to the row. Mary updates the list's length counter, which changes by itself.

* Andy: In C++, a basic array has a fixed size. Python lists can grow: .append() adds an item to the end.

```
scores = [8, 10, 7, 9]
scores.append(6)

print(scores)
print(len(scores))
```

* Mary: Now scores has five items, and len(scores) automatically reports 5. We don't need to update a size number ourselves. Are you chattering about how good C++ is again. (rolls eyes and giggles)

* Andy: "Fixed-size arrays build character."

* Mary: "So does remembering to call `.append()`!"

### Panel 4 — Loop with an index or directly?

Visual: Two paths run alongside the list. One is marked "index," the other "visit each value."

* Andy: If you need each item's position, loop over indexes:

```
for i in range(len(scores)):
    print(i, scores[i])
```

* Mary: `i` is the index, and `scores[i]` is the value at that position.

* Andy: If you don't need the position, loop directly over the values:

```
for score in scores:
    print(score)
```

* Mary: Use indexes when you need the position. Otherwise, the direct loop is simpler.

## Task 2 — Add two more scores

Append two more scores to the list, then run both loops. The index loop will adjust automatically because it uses len(scores).

## Bug Detective: Indexes

Visual: Andy pins three code samples to the detective board. Mary looks for where each bug hides.

### Mystery 1 — One too far

```
scores = [8, 10, 7, 9]

for i in range(len(scores) + 1):
    print(scores[i])
```

* Mary: Why does this crash?

* **Clue:** `len(scores) + 1` makes the loop try index 4. The valid indexes are 0 through 3.

* **Fix:**

```
for i in range(len(scores)):
    print(scores[i])
```

### Mystery 2 — Printing the index instead of the value

```
scores = [8, 10, 7, 9]

for i in range(len(scores)):
    print(i)
```

* Andy: This prints 0, 1, 2, 3. How can we print the scores?

* **Clue:** i is the position. To get the value at that position, use scores[i].

* **Fix:**

```
for i in range(len(scores)):
    print(scores[i])
```

### Mystery 3 — The append that escaped

```
animals = []

for i in range(3):
    animal = input("Enter an animal: ")

animals.append(animal)
```

* Andy: The user typed three animals, but the list only has one — and it's the last one! Why?

* **Clue:** Look at the indentation. The `.append()` line is outside the loop, so it only runs once, after the loop has finished. By then, animal holds just the last name typed.

* **Fix:** Indent the append so it runs inside the loop, once per animal:

```
animals = []

for i in range(3):
    animal = input("Enter an animal: ")
    animals.append(animal)
```

* Mary: Indentation decides whether a line runs every time the loop repeats—or only once, after it ends.

### Detective-board answer key:

Check where the index starts, where it stops, and whether you're printing the position or the value. And check indentation: code inside a loop runs each time the loop repeats; code outside it runs only once.

## Interesting Fact: Frances Allen

Visual: Frances Allen examines a program's loops while a compiler diagram shows code being translated into instructions.

* Andy: Frances Allen was a computer scientist known for her work on optimizing compilers—programs that translate code and help it run more efficiently.

* Mary: Her compiler research included techniques for analyzing and improving loops, connecting neatly to the loops we use in Python.

Visual: A Turing Award appears beside the year 2006.

* Andy: In 2006, she became the first woman to receive the Turing Award, computing's highest honor. Her work helped advance compiler design and program optimization. Computer History Museum

## Final Challenge — Numbered roll call

* Mary: Let's use indexes to number each animal in the list.

Write a program that asks the user for three animals, stores them in a list using `.append()`, and prints a numbered roll call like this:

```
1. cat is a great animal!
2. dog is a great animal!
3. fox is a great animal!
You entered 3 animals.
```

* **Hint:** Use `range(len(animals))` to get each index. Remember, indexes start at 0, so add 1 to i when printing the number.

**Hint:** Numbers are tricky to print neatly — print(i + 1, ".") adds unwanted spaces. An f-string puts the number and the dot together exactly as you want: f"{i + 1}. {animal} is a great animal!" We met f-strings in Tutorial 7.

* Finish by using `len(animals)` to show how many animals were entered.
