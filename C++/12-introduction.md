# Introduction to C++ (Part 12)

## Storing Lists with Vectors

An array has a fixed size. A vector is a list that can grow or shrink while your program runs. To use vectors, include the <vector> header.

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores = {8, 10, 7};

    std::cout << scores[0] << "\n";

    return 0;
}
```

This vector stores three integers. Like array indexes, vector indexes start at 0, so scores[0] is the first score.

### Adding Items

Use `.push_back()` to add an item to the end of a vector.

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores = {8, 10};

    scores.push_back(7);

    std::cout << scores[2] << "\n";

    return 0;
}
```

After push_back(7), the vector has three scores, and scores[2] is 7.

### Finding How Many Items There Are

Use `.size()` to find out how many items are in a vector.

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> pets = {"cat", "dog", "rabbit"};

    std::cout << "There are " << pets.size() << " pets.\n";

    return 0;
}
```

This vector stores strings, so the program also needs `#include <string>`:

```cpp

#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> pets = {"cat", "dog", "rabbit"};

    std::cout << "There are " << pets.size() << " pets.\n";

    return 0;
}
```

### Visiting Every Item

A range-based for loop can visit each item in a vector, one at a time:

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores = {8, 10, 7};

    for (int score : scores) {
        std::cout << score << "\n";
    }

    return 0;
}
```

The loop puts each score into the variable score, then prints it. It runs once for every item in the vector.

### Removing the Last Item

Use `.pop_back()` to remove the last item. Only use it when the vector has an item to remove.

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> snacks = {"apple", "crackers", "pear"};

    snacks.pop_back();

    for (std::string snack : snacks) {
        std::cout << snack << "\n";
    }

    return 0;
}
```

This removes "pear", so the program prints the other two snacks.

### Task 1

Make a vector of three favorite animals and print the second animal.

#### Solution 1

```cpp

#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> animals = {"tiger", "panda", "owl"};

    std::cout << animals[1] << "\n";

    return 0;
}

The second animal is at index 1.
Task 2

Make an empty vector of integers. Add three numbers with .push_back(), then print how many numbers it contains.
Solution 2
cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers;

    numbers.push_back(4);
    numbers.push_back(9);
    numbers.push_back(2);

    std::cout << "There are " << numbers.size() << " numbers.\n";

    return 0;
}

Task 3

Make a vector of four scores and use a loop to print every score.
Solution 3
cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> scores = {6, 8, 10, 9};

    for (int score : scores) {
        std::cout << score << "\n";
    }

    return 0;
}
```


## Bug Detective: Vectors

Detective hats on, team! These programs have bugs hiding in their vectors.

### Mystery 1: The missing header

The program should make and print a vector, but it won’t compile.

```cpp

#include <iostream>

int main() {
    std::vector<int> numbers = {3, 6, 9};
    std::cout << numbers[0] << "\n";

    return 0;
}
```

* **Clue:** Which header is needed to use std::vector?

### Mystery 2: The wrong index

The program should print the first color, "red".

```cpp

#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> colors = {"red", "blue", "green"};

    std::cout << colors[1] << "\n";

    return 0;
}
```

* **Clue:** What index does the first item use?

### Mystery 3: The item wasn’t added

The program should add 5 to the vector and print it.

```cpp

#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers = {2, 4};

    numbers.push_back;

    std::cout << numbers[2] << "\n";

    return 0;
}
```

* **Clue:** What goes in the parentheses after push_back?

### Detective answer key

* Add `#include <vector>`.
* Change `colors[1]` to `colors[0]`.
* Change `numbers.push_back;` to `numbers.push_back(5);`.


## A Small Challenge: Score Keeper

Start with an empty vector of scores. Ask the user to enter three scores, add each one to the vector, then print all the scores and how many there are.

Here’s a hint for reading and adding each score:

```cpp

int score;
std::cin >> score;
scores.push_back(score);
```
