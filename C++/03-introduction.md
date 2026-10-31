# Introduction to C++ (Part 3) 

## Making Choices with if

A program can make a choice using an if statement. It checks whether something is true, then follows the matching instructions.

```cpp

#include <iostream>

int main() {
    int age;

    std::cout << "How old are you? ";
    std::cin >> age;

    if (age >= 10) {
        std::cout << "You are 10 or older!";
    } else {
        std::cout << "You are younger than 10.";
    }

    return 0;
}
```

The symbol `>=` means “greater than or equal to.” So `age >= 10` checks whether the age is 10 or more.

* If the check is **true**, the program runs the instructions after `if`.
    
* Otherwise, it runs the instructions after else.

> [!NOTE]
>
> Computers often check whether something is true or false. These are called **Boolean** values.
> 
> For example, if age is 12, then `age >= 10` is **true**. If age is 8, then `age >= 10` is **false**.
> 
> C++ has a variable type called bool that stores either true or false:
>
> * `bool isSunny = true;`
> * `bool isRaining = false;`
>
> An `if` statement uses a true-or-false check to decide what to do.

### Task 1

* Try changing 10 to a different number, or change the messages.


## Making Choices with `if` and `else`

An `if` statement checks whether something is **true** or **false**. If it is **true**, the program runs the instructions inside the `if` block. 

Otherwise, an `else` block can run instead:

```cpp

#include <iostream>

int main() {
    int age;

    std::cout << "How old are you? ";
    std::cin >> age;

    if (age >= 10) {
        std::cout << "You are 10 or older!";
    } else {
        std::cout << "You are younger than 10.";
    }

    return 0;
}
```

The condition `age >= 10` means “is age greater than or equal to 10?” It evaluates to **true** or **false**.

* If the condition is **true**, the program prints “You are 10 or older!”
* If the condition is **false**, the program prints “You are younger than 10.”

### Task 2

* Try changing the number 10 or the messages.

## Checking More Than Two Choices

Sometimes a program needs to choose between more than two possibilities. Use else if to check another condition.

```cpp

#include <iostream>

int main() {
    int score;

    std::cout << "What score did you get? ";
    std::cin >> score;

    if (score >= 90) {
        std::cout << "Excellent!";
    } else if (score >= 60) {
        std::cout << "You passed!";
    } else {
        std::cout << "Keep practicing!";
    }

    return 0;
}
```

The program checks the conditions in order:

* If `score >= 90` is **true**, it prints “Excellent!”
* Otherwise, it checks whether `score >= 60` is **true**, it prints "You passed".
* If neither condition is **true**, it runs the else block and prints "Keep practicing!".

Only the first matching block runs. 

### Task 3

* Try entering different scores to see what happens.