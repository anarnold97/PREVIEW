# Tutorial 9 — For Loops: Looping the Smart Way
(Version 3 — restructured revision)

Changes from v2 (full changelog at the bottom):

    Added a running mini-project ("Robot Recital") that threads through the chapter, giving panels a narrative spine instead of isolated snippets.
    Task ladder now ramps from recall → modify → predict → create.
    New "Prediction Pause" ritual formalised: learners commit to a guess before seeing output. Used twice (Panels 8 and 11) so the habit becomes routine, not a one-off gimmick.
    Vocabulary box moved to the end of Part One, once the reader has seen all three ideas in action.
    Bug Detective re-titled mysteries as cases with a stated Method panel — mirroring real debugging practice.
    Sammet sidebar shortened and made punchier; long history beats cut.

## Panel 1 — We've met for before

Visual: Andy points to a faded "FizzBuzz" poster and a times-table chart pinned to a corkboard. Mary taps a loop diagram on it.

Caption: We've been using for loops all along — in FizzBuzz and the times tables. Now we'll make them ours: you'll loop over anything, not just numbers.

    Andy: In FizzBuzz, for visited numbers. In the times-table project, it visited rows and columns.
    Mary: So a for loop repeats its instructions for each value it gets — whatever those values are.
    Andy: "Whatever those values are" is today's headline. Numbers are just one kind of thing a loop can visit.

## Panel 2 — One-argument range()

Visual: Five numbered stepping stones: 0, 1, 2, 3, 4. A signpost says "Stop before 5!" Andy stands on stone 4.

    Andy: With one argument, range(5) starts at zero and stops before five.
    Mary: Five stones — 0, 1, 2, 3, 4 — but the stone labelled 5 is never built.
```python
for number in range(5):
    print(number)
```
    Mary: Remember Bug Detective from Tutorial 6? We investigated range(1, 30) — it starts at 1 and stops before 30. Same rule here: the stop value is excluded.
    Andy: That "stops before" rule trips everyone eventually. Today you learn it before it trips you.

Panel 3 — Stepping through

Visual: Andy hops along a number line in jumps of three. Mary points to a second arrow running backward.

    Andy: range() can take three arguments: a start, a stop, and a step.
```python
for number in range(1, 13, 3):
    print(number)
```
    Mary: That prints 1, 4, 7, 10. Each step adds 3, and the loop stops before 13.
    Andy: A negative step counts backward:
```
for number in range(5, 0, -1):
    print(number)
```
    Mary: 5, 4, 3, 2, 1 — liftoff! The stop value is still excluded.

Panel 4 - Prediction Pause #1

Visual: Mary holds a card over the next code block. A thought bubble above Andy shows a big "?".

    Mary: Before Andy reveals it — what will this print?
```
for number in range(3, 21, 4):
    print(number)
```
    Andy: Write your guess down, then check it. Getting surprised is how you learn what range actually does.

Task 1 — Even numbers

Print the even numbers from 2 through 20 using a single call to range(). (One line of range code, one line of print.)

    Hint: Start at 2, stop beyond 20, step by… you tell me.

Expected output:

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

Part Two: Looping over a list
Panel 5 — A row of labeled boxes

Visual: A crate labelled animals holds three smaller boxes in a row: "cat," "dog," "fox." Order tags 0, 1, 2 are clipped to the shelf beneath — small, unfussed-over.

    Mary: In Tutorial 3, a variable was a labeled box. A list is one labeled container holding several smaller boxes, in order.
    Andy: The order is the list's superpower — "cat" is in position, "dog" is next, "fox" is last. Hold onto that.

animals = ["cat", "dog", "fox"]

    Mary: Lists can also change — you can add, remove, or replace items later. We'll learn how in Tutorial 12. Today we build lists and read them.
    Andy: If you're itching to ask "can I change one box directly?" — good instinct. Park it until Tutorial 12 and it'll feel easy.

Panel 6 — How long is a list?

Visual: Mary counts boxes on her fingers and holds up a card that says 3. Andy checks a tape measure labelled len().

    Mary: Python's built-in len() tells you how many items are in a list.

animals = ["cat", "dog", "fox"]
print(len(animals))

    Andy: That prints 3. len() measures items, not positions — a fact our Bug Detective will exploit shortly.

Panel 7 — The loop variable gets each item

Visual: A spotlight sweeps from the "cat" box to "dog," then "fox." Andy hands each item to a courier holding a parcel tagged animal.

    Andy: Here's the heart of looping over a list:

for animal in animals:
    print(animal)

    Mary: Python takes each item, one at a time, and puts it in animal. First "cat," then "dog," then "fox."
    Andy: No counters, no indexes. The loop hands you each element in turn — like a conveyor belt.

Panel 8 — Name your loop variable like you mean it

Visual: Mary compares two parcels: one tagged with a scribbled "x," one tagged "animal."

    Mary: This works, but tells the reader nothing:

for x in animals:
    print(x)

    Andy: This one explains itself:

for animal in animals:
    print(animal)

    Mary: A good loop-variable name tells readers what's inside the box at each moment. We'll meet someone who fought for exactly this idea later — keep that thought.

Part Three: Building results as you go
Panel 9 — The accumulator

Visual: Mary drops coins into a jar marked total. Andy draws a bracket around the indented lines, then circles the print below.

    Andy: A loop can build a result as it runs. A variable holding a running result is an accumulator.

numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number

print(total)

    Mary: After the loop, total holds 13.
    Andy: The indentation is the whole trick: the addition lives inside the loop; print(total) sits outside — it runs once, after all the adding is done.
    Mary: Prediction Pause #2: if print(total) moved inside the loop — how many lines would print, and what would they say? Commit to a guess. We'll settle this in the Bug Detective.

Panel 10 — Choosing your loop

Visual: Three doors: "For: visit each item," "While: keep checking," "Run once, then decide."

    Mary: The loop-choice doors from Tutorial 5, rehung:
        for — going through a collection or known sequence of values.
        while — repeating as long as a condition holds.
        while True with break — run at least once, then decide.
    Andy: Match the loop to the job and the job gets easier.

Panel 10 — When you need the item and its position

Visual: Mary holds a delivery checklist with a number beside each name. Andy points to a clipboard stamped enumerate().

    Andy: Sometimes you genuinely need the position — numbering guests, say: "1. Sam, 2. Priya…"
    Mary: enumerate() hands you each item and its position together:

for position, name in enumerate(names, start=1):
    print(position, name)

    Andy: enumerate() does the counting — no len(), no off-by-one traps.
    Mary: Rule of thumb: loop directly over the list when you need the items. Reach for positions only when you need to know where you are — and let enumerate() count for you.

Panel 11 — The Robot Recital (mini-project begins)

Visual: A small robot on stage facing three mic stands. Mary holds a clipboard titled "Recital Program."

    Mary: Everything you've learned this chapter, in one tiny project. First, the set list:

acts = ["juggle", "spin", "bow"]
for act in acts:
    print("The robot will now:", act)

    Andy: A list, a loop, a readable loop variable — the crowd loves a well-named program.
    Mary: Task: extend the recital so it counts the acts and announces the total at the end. You have every tool for that already.

(Task 3 below gives the full spec; Task 4 stretches it.)
Bug Detective: For Loops

Visual: Andy pins three code samples to a detective board under CASE 1/2/3 headings. Mary polishes her magnifying glass.
Method (posted above the board)

Visual: A three-step checklist card.

    Read the code aloud and predict the output before running it.
    Trace each iteration — what does the loop variable hold right now?
    Check indentation: what runs every time vs. once at the end?

CASE 1 — The missing last friend

names = ["Sam", "Priya", "Jordan"]

for index in range(0, len(names) - 1):
    print(names[index])

    Andy: The program should greet everyone — but Jordan never gets a turn. Why?
    Mary: len(names) is 3, so range(0, 2) yields 0 and 1. The loop stops one short — the classic off-by-one.
    Clue: The list's indexes are 0, 1, and 2. The loop never reaches 2.
    Fix: If you want every name, skip the indexes entirely:

for name in names:
    print(name)

    Andy: Need the position anyway? That's enumerate() — Panel 10.

CASE 2 — The total that won't stop printing

numbers = [4, 7, 2]
total = 0

for number in numbers:
    total = total + number
    print(total)

    Andy: How close was your Prediction Pause #2?
    Clue: print(total) is indented inside the loop, so it runs once per number: 4, then 11, then 13.
    Fix: Dedent the print so it runs once, after the loop.

CASE 3 — The overwritten loop variable

animals = ["cat", "dog", "fox"]

for animal in animals:
    animal = "owl"
    print(animal)

    Mary: We wanted every animal. What actually prints?

    Andy: "owl" — three times. The assignment clobbers the value the loop just handed us.

    Clue: The list itself is untouched; each iteration still delivers the next real item. But overwriting the loop variable is a landmine for future edits.

    Fix: Don't assign to the loop variable. If you need a separate value, give it its own name.

    Mary: Bonus trace, no code needed: if the animal = "owl" line came after the print, the output would look right — this time. Bugs that hide are worse than bugs that shout.

Detective-board answer key

Check where range() starts and stops; inspect indentation; never overwrite a loop variable mid-loop. Loop directly over items by default — delegate counting to enumerate().
Interesting Fact: Jean Sammet

Visual: Jean Sammet at an early computer, punch cards nearby; inset portrait with a "HOPL-1" conference badge.

    Andy: Jean Sammet — mathematician turned programmer, working in computing in the 1950s, one of few women in the field.
    Mary: At IBM she led the FORMAC project, a language for symbolic math, and supervised early COBOL — a language designed so non-programmers could read it.
    Andy: That's our thread: readable code is communication. COBOL carried that flag in 1959; Python carries it today.
    Mary: So name your loop variables properly, Andy. (giggles) And she organised the first History of Programming Languages conference — HOPL — preserving how our languages came to be. Readable code and readable history.

Final Challenge — Animal roll call

    Mary: Combine lists, loops, input(), and counting.

Write a program that:

    Asks the user to type three animal names.

    Stores them in a list.

    Prints each animal followed by "is a great animal!"

    Ends with how many animals were entered — once with len(), once with enumerate().

    Hint: Start with an empty list; use input() three times; len() came from Panel 5.

Example output:

cat is a great animal!
dog is a great animal!
fox is a great animal!
You entered 3 animals.

Stretch goals (optional)

    Print a numbered roll call using enumerate(names, start=1).
    Print the animals in reverse using a negative-step range over positions — then compare how it feels against looping over the list directly, and ask yourself which you'd rather read.

Changelog for v3

    Task ladder rebuilt: recall (Task 1) → modify/create (Tasks 2–3, Robot Recital) → stretch goals.
    Prediction Pause ritual formalised: Panel 3 (#1) and Panel 8 (#2), paying off in Bug Detective Cases 1–2.
    Panel 4: index tags shown quietly (0, 1, 2) on the visual so off-by-one in Case 1 has a referent, without front-loading index syntax.
    Bug Detective gains an explicit three-step Method panel — teaching debugging process, not just spotting three bugs.
    Robot Recital mini-project added (Panel 11 + Tasks 3–4) as a narrative spine pulling lists, loops, accumulator, and enumerate() together.
    len() in Panel 5 now foreshadows its Bug Detective role ("measures items, not positions").
    Sammet sidebar condensed; HOPL retained; readability-through-history framing kept.
    Language tightened throughout; QA-fix margin notes removed (they're meta-commentary, not learner content) — this document is the record of them.
