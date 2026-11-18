# Introduction to C++ (Part 10)

## Making Reusable Code with Functions

A **function** is a named set of instructions. You can tell the program to run those instructions whenever you need them. Functions help keep programs organized and avoid repeating the same code.

Here’s a function that prints a greeting:

```cpp

#include <iostream>

void sayHello() {
    std::cout << "Hello!\n";
}

int main() {
    sayHello();
    sayHello();

    return 0;
}
```

* `void` means this function does not send a value back. The function’s name is `sayHello`, and the instructions inside its braces run each time we call it. In main, `sayHello();` is a function call.

### Giving a Function Information

A function can receive information through **parameters**. This function takes a name and uses it in its greeting:

```cpp

#include <iostream>
#include <string>

void greet(std::string name) {
    std::cout << "Hello, " << name << "!\n";
}

int main() {
    greet("Maya");
    greet("Leo");

    return 0;
}
```

* `name` is a parameter: it’s a variable the function can use. The values "Maya" and "Leo" are called **arguments**. Each time greet is called, the argument is passed into the function.
Getting a Value Back

A function can also calculate something and send the result back with return. The type before the function’s name tells us what kind of value it returns. This function returns an int:

```cpp

#include <iostream>

int add(int first, int second) {
    return first + second;
}

int main() {
    int total = add(3, 4);

    std::cout << total << "\n";

    return 0;
}
```

The function receives two integers, adds them, and returns the result. The call add(3, 4) gives back 7, which is stored in total.

### Task 1

Write a function called `showScore` that prints Your score is 10!. Call it from `main`.

#### Solution 1

```cpp

#include <iostream>

void showScore() {
    std::cout << "Your score is 10!\n";
}

int main() {
    showScore();

    return 0;
}
```

### Task 2

Write a function called `doubleNumber` that takes an integer and returns twice its value. Call it with 6 and print the result.

#### Solution 2

```cpp

#include <iostream>

int doubleNumber(int number) {
    return number * 2;
}

int main() {
    int answer = doubleNumber(6);

    std::cout << answer << "\n";

    return 0;
}
```

It prints:

```text

12
```

### Task 3

Write a function called `printRow` that takes a number and prints that many stars. For example, `printRow(4)` should print `****`.

#### Solution 3

```cpp

#include <iostream>

void printRow(int numberOfStars) {
    for (int i = 0; i < numberOfStars; i++) {
        std::cout << "*";
    }

    std::cout << "\n";
}

int main() {
    printRow(4);

    return 0;
}
```

The loop runs four times, printing one star each time.

## Bug Detective: Functions

Detective hats on, team! These functions have a few mistakes. Figure out what each program should do, then fix it.
 
### Mystery 1: The missing call

The program should print Ready!, but it doesn’t.

```cpp

#include <iostream>

void sayReady() {
    std::cout << "Ready!\n";
}

int main() {
    return 0;
}
```

* **Clue:** Defining a function gives it instructions. What do you need to do to run it?

### Mystery 2: The wrong answer

The function should return the sum of its two numbers.

```cpp

int add(int first, int second) {
    return first - second;
}
```
    
* **Clue:** Which math symbol adds two numbers?

### Mystery 3: The result disappears

The program should print 10, but it prints 5.

```cpp

#include <iostream>

int doubleNumber(int number) {
    return number;
}

int main() {
    std::cout << doubleNumber(5) << "\n";

    return 0;
}
```
    
* **Clue:** What calculation would make the number twice as large?

### Detective answer key

* Add `sayReady();` inside `main`.
* Change `first - second` to `first + second`.
* Change `return number;` to `return number * 2;`.


## A Small Challenge: Draw a Box

Use a function to print a row of stars, then call it several times to make a box. For example, a box that is 5 stars wide and 3 rows tall should look like this:
text:

````
*****
*****
*****
```

Try changing the width and height. Functions make it easier to reuse the same instructions for every row!
