# Introduction to C++ (Part 1)

## Part One

C++ is a programming language—a way to give instructions to a computer. People use C++ to make games, apps, and many other things.

A program is a list of instructions that a computer follows. Here is a tiny C++ program:

```cpp

#include <iostream>

int main() {
    std::cout << "Hello, world!";
    return 0;
}
```

When you run this program, it displays:

```text

Hello, world!
```

Here’s what the parts do:

* `#include <iostream>` gives the program tools for showing text.
* `int main()` shows where the program begins.
* `{` and `}` show where the instructions start and end.
* `std::cout` displays something on the screen.
* `"Hello, world!"` is the message to display.
* `return 0;` tells the computer that the program has finished.

C++ instructions often end with a semicolon (`;`). If you forget one, the computer will not understand your program.

### Task 1

You can change the message inside the quotation marks. Try replacing `"Hello, world!"` with your name or a fun message, then run the program again.

## Part Two

### Storing Information in Variables

Programs can remember information using variables. A variable is like a labeled box that holds a value.

```cpp

#include <iostream>

int main() {
    int age = 10;
    std::cout << age;
    return 0;
}
```

This program displays:

```text

10
```

Here, `int` means the variable stores a whole number. The name age is the label, and `10` is the value inside it.

You can also use a variable in a message:

```cpp

#include <iostream>

int main() {
    int age = 10;
    std::cout << "I am ";
    std::cout << age;
    std::cout << " years old.";
    return 0;
}
```

It displays:

```text

I am 10 years old.
```

### Task 2

* Try changing 10 to another number. What does the program display?

---

## Bugs

Bugs in programming are mistakes or errors in the code that can cause a program to not work correctly. A bug can make a computer program behave unexpectedly or even crash.

Grace Hopper is our hero for many reasons. She also found the first **bug**.

In 1947, Grace and her team were working on the Harvard Mark II computer when they discovered a moth that had caused a problem by entering the circuits of one of the early computers.

They documented this incident in their logbook, labeling it as the "first actual case of bug being found."

---

## Bug Detective Challenge

Detective hats on, team! Let’s investigate the bugs hiding in our “Hello, world!” program. Each version has one sneaky mistake. Run the programs, follow the clues, and see if you can solve the case!

Each program below has one bug. Copy and run them one at a time. Some bugs stop the program from compiling; one lets it run but makes it say the wrong thing.

### Mystery 1: The compiler is grumbling

```cpp

#include <iostream>

int main() {
    std::cout << "Hello, world!\n"
    return 0;
}
```

* **Clue:** C++ expects a punctuation mark at the end of most instructions.

### Mystery 2: “I don’t know what cout is!”

```cpp

int main() {
    std::cout << "Hello, world!\n";
    return 0;
}
```

* **Clue:** The program needs to bring in the tool that lets it print words.

### Mystery 3: It said hello… sort of

```cpp

#include <iostream>

int main() {
    std::cout << "Hello world!\n";
    return 0;
}
```

* **Clue:** Compare its message carefully with the one the program is supposed to print. Even punctuation matters!

### Detective answer key

* Add a semicolon after the std::cout instruction.
* Add `#include <iostream>` at the top.
* Add the missing comma after Hello.




