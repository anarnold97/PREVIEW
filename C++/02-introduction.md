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

Computers are like Sam, they follow instructions logically.