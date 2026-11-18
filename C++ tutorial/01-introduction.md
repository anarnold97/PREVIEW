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

## Interesting fact

After Ada Lovelace imagined programs, people had to write them — but early computers only understood raw numbers. Programming meant writing long streams of 1s and 0s. Grace Hopper, a US Navy rear admiral and mathematician, thought that was absurd. Why couldn't humans program in words?

Everyone told her machines could never translate human words into computer language. She built the first compiler anyway — a program that translates human-readable code into machine code. Every modern programming language, including the one in these tutorials, exists because Grace Hopper insisted computers should speak our language too.

Oh — and her team also found the first literal computer bug: an actual moth, squashed in a relay, taped into the logbook with the caption "first actual case of bug being found." When your program misbehaves, you're carrying on a tradition that's older than you think.

WE LOVE GRACE HOPPER! We will tell you more about her in a later interesting fact!

---


## Bugs

Now we can talk about bugs. Bugs in programming are mistakes or errors in the code that can cause a program to not work correctly. A bug can make a computer program behave unexpectedly or even crash.

Every coder will find bugs in their code. Bugs let us improve.

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




