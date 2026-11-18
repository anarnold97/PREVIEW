# Introduction to C++ (Part 4) 

## Repeating Instructions with a for Loop

Now that the program can make choices, it can also repeat instructions. A loop repeats a piece of code.

```cpp

#include <iostream>

int main() {
    for (int count = 1; count <= 5; count++) {
        std::cout << "Hello!\n";
    }

    return 0;
}
```

This prints Hello! five times. The \n moves the next message to a new line.

The `for` loop has three parts:

* `int count = 1` creates a counter that starts at 1.
* `count <= 5` means “keep repeating while count is 5 or less.”
* `count++` adds 1 to the counter after each repeat.

When count becomes 6, the check is false, so the loop stops.

### Task 1

* Try changing 5 to another number. How many times will the program print Hello!?

## Nested for Loops

A **nested loop** is a loop inside another loop. The inner loop completes all its repeats each time the outer loop repeats once.

```cpp

#include <iostream>

int main() {
    for (int row = 1; row <= 3; row++) {
        for (int star = 1; star <= 4; star++) {
            std::cout << "* ";
        }

        std::cout << "\n";
    }

    return 0;
}
```

This prints four stars on each of three lines:

```text

* * * *
* * * *
* * * *
```

The outer loop counts the rows. For each row, the inner loop prints four stars. After the inner loop finishes, `std::cout << "\n";`` starts a new line.

### Task 2

* Try changing the loop limits. For example, what happens if the outer loop counts to 5 and the inner loop counts to 2?

## Arithmetic Operators

Arithmetic operators let a program do math. Here are some common ones:

| Operator | Meaning | Example |
| -------- | ------- | ------- |
| `+` |	Add	| 4 + 3  gives 7 |
| `-` |	Subtract |	4 - 3 gives 1 |
| `*`	| Multiply	| 4 * 3 gives 12 |
| `/` |	Divide |	12 / 3 gives 4 |
| `%` |	Find the remainder| 7 % 3 gives 1 |

You can use them with variables:

```cpp

#include <iostream>

int main() {
    int apples = 5;
    int moreApples = 3;
    int total = apples + moreApples;

    std::cout << "Total apples: " << total;
    return 0;
}
```

This displays **Total apples: 8**.


> [!WARNING]
>
> With `int` numbers, division keeps only the whole-number part: 7 / 2 gives 3. 
>
> To get a decimal answer, use double, such as 7.0 / 2.0, which gives 3.5.
> 

---

## Interesting fact

Margaret Hamilton worked at MIT, where her team built the software that guided Apollo’s command and lunar modules. In those days, software engineering was so new that there were no classes to teach it. The team had to figure out how to design and organize a system that people would trust to carry astronauts to the Moon—and bring them home.

Hamilton led the teams writing that software. She believed it should do more than follow instructions: it should notice when something went wrong, tell the astronauts, and recover when it could. During Apollo 11’s landing, the computer was overloaded with tasks. The software recognized the problem, set priorities, and kept the mission-critical work going. 

Hamilton called this work “software engineering” because she believed software deserved the same care and respect as other kinds of engineering. She helped make it a discipline—not just a pile of code, but a system thoughtfully designed to handle trouble. 

When you organize your code into clear pieces, give each part a job, and plan for things to go wrong, you’re following the kind of discipline Margaret Hamilton helped build. Good software isn’t only about making things work. It’s about making them work when it matters.

So: give your ideas tidy little jobs, test your work, and make a backup plan. Because even computers sometimes need to hear, “Not everything at once, please!”
