# Introduction to C++ (Part 2) 

## Variables

Variables can store different kinds of information. Here are three common types:

* `int` stores whole numbers, like **7** or **42**.
* `double` stores numbers with decimal points, like **3.5**.
* `std::string` stores words or sentences, like **"Hello!"**.

To use std::string, include the <string> tool:

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

The ``<<`` symbols let you join several pieces of information when displaying them.

### Task 1

* Try changing the name and age. Then add another std::string variable to store your favorite animal.


## Getting Input from the User

So far, the program has displayed information. It can also ask the user to type something. Use `std::cin` to read what they type.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name;

    std::cout << "What is your name? ";
    std::cin >> name;

    std::cout << "Hello, " << name << "!";
    return 0;
}
```

If the user types Mia, the program displays:

```text

What is your name? Mia
Hello, Mia!
```

* `std::cin >> name`; takes the typed word and stores it in the **name** variable.

### Task 2

* Try changing the question, or make a program that asks for the user's favorite animal.