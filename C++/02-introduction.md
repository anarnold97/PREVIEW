# Introduction to C++ (Part 2)

## Variables

Variables can store different kinds of information. Here are three common types:

* `int` stores whole numbers, like 7 or 42.
* `double` stores numbers with decimal points, like 3.5.
* `std::string` stores words or sentences, like "Hello!".

To use `std::string`, include the `<string>`` library:

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name = "Mia";
    int age = 10;
    double favoriteNumber = 7.5;

    std::cout << name << " is " << age << " years old.";
    return 0;
}
```

The program displays:

```text

Mia is 10 years old.
```

The `<<` operator sends pieces of information to `std::cout`, which displays them on the screen.

### Task 1

* Try changing the name and age. Then add another std::string variable to store your favorite animal.

## Getting Input from the User

So far, the program has displayed information. It can also ask the user to type something. Use std::cin to read what they type.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name;

    std::cout << "What is your name? ";
    std::cin >>
```

If the user types Mia, the program displays:

```text

What is your name? Mia
Hello, Mia!
```

`std::cin >> name`; reads one word from the user and stores it in the name variable. For now, enter a name without spaces.

### Task 2

* Change the question, or make a program that asks for the user's favorite animal.

---

## The Programmer and the Shopping List

Sam was a programmer who liked instructions to be very exact.

One day, Sam’s husband said, “Please pick up a loaf of bread. If the shop has eggs, get a dozen.”

Sam went to the shop. They had eggs, so Sam followed the words very carefully and bought twelve loaves of bread!

When Sam got home, their husband laughed. “I meant a loaf of bread and a dozen eggs!”

Sam smiled. “Next time, I’ll ask if I’m not sure what you mean.”

The lesson: Instructions can sometimes mean more than one thing.

Computers are like Sam, they follow instructions very logically. What you tell it to do in a program, might not be how the computer interprets your instructions. 

---

## Bug Detective: Variables

Detective hats on, team! Variables are like labeled boxes where a program keeps information. Let’s investigate what happens when a label is misspelled, the wrong kind of box is used, or we show the wrong box!

Each program has one bug. Copy and run them one at a time.

### Mystery 1: The name that isn’t there

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name = "Mia";

    std::cout << nme << " says hello!\n";
    return 0;
}
```

* **Clue:** Check whether the variable’s name in the std::cout line matches its label above.

### Mystery 2: Where did the decimal go?

```cpp

#include <iostream>

int main() {
    int favoriteNumber = 7.5;

    std::cout << "My favorite number is " << favoriteNumber << "\n";
    return 0;
}
```

This program runs, but it won’t show 7.5.

* **Clue:** `int` is for whole numbers. Which type can store numbers with a decimal part?

### Mystery 3: The wrong box is on display

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name;
    int age = 10;

    std::cout << "What is your name? ";
    std::cin >> name;

    std::cout << "Hello, " << age << "!\n";
    return 0;
}
```

Try entering Mia. Does the program greet Mia?

* **Clue:** The program saved the answer in one variable. Which variable does it show afterward?

### Detective answer key

* Change `nme` to `name`.
* Change `int favoriteNumber` to `double favoriteNumber`.
* Change `age` to `name` in the final `std::cout` line.

---

## Interesting fact

ENIAC, finished in 1945, was one of the first electronic computers ever built. It was enormous — about the size of a large classroom — with around 18,000 vacuum tubes that glowed, overheated, and burned out constantly. Some tubes failed every single day.

Programming ENIAC didn't mean typing code. It meant physically moving cables and switches for days until the machine did what you wanted. There was no manual. Nobody had ever done this before.

The team who figured out how to program it were six women: Kathleen McNulty, Jean Jennings Bartik, Frances Spence, Ruth Lichterman, Elizabeth Snyder, and Marlyn Wescoff. They studied the machine's blueprints and worked out, entirely from scratch, how to make it calculate.

In 1946, ENIAC was shown off to the press and Army officials. It was called a miracle of modern science. The six women who made it work? They were not mentioned. They weren't even in the photograph.

Was ENIAC a success? Not really! It barely worked, it was retired after a few years, and better machines quickly replaced it. But every computer that came after — including the one you're reading this on — works because six women first wrestled the impossible machine into cooperating. 

So when your program crashes on the first try, you are in excellent historical company. First versions are supposed to be disasters. That's what first versions are for.

We salute the ENIAC Six, who by definition, are the world's first professional developers!