# Introduction to C++ (Part 4 - while loops and do while loops)

## Repeating Instructions with a while Loop

A while loop repeats instructions while a condition is true. It checks the condition before each repeat.

```cpp

#include <iostream>

int main() {
    int count = 1;

    while (count <= 5) {
        std::cout << count << "\n";
        count++;
    }

    return 0;
}
```

This prints the numbers 1 through 5.

* `int count = 1` creates a counter that starts at 1.
* `count <= 5` means “keep going while count is 5 or less.”
* `count++` adds 1 each time the loop repeats.

When count becomes 6, the condition is false, so the loop stops. The computer is done counting and can finally have a snack... in other words - a byte to eat!

### Task 1

* Change the loop so it counts from 1 to 10.
* What do you think would happen if you removed `count++`? Predict first—don’t run it! Without changing the counter, the condition would stay **true**, and the loop could repeat forever - an **infinite** loop.

## Repeating Instructions with a do while Loop

A **do while** loop is similar, but it checks the condition after running the instructions. That means its instructions always run at least once.

```cpp

#include <iostream>

int main() {
    int number = 0;

    do {
        std::cout << "Enter 10 or more: ";
        std::cin >> number;
    } while (number < 10);

    std::cout << "Great—you entered 10 or more!\n";

    return 0;
}
```

If you enter 4, the program asks again. If you enter 12, it stops and says “Great!” If you enter 12 the first time, it still asks you once—because do while always does its instructions before checking.

Do not forget to notice the semicolon after the condition:

```cpp

} while (number < 10);
```

That semicolon is part of the do while loop. It’s a tiny punctuation mark with a very important job.

####Task 2

* Try entering a number below 10, then a number that is 10 or more.
* Change the program so it keeps asking until the number is at least 20.

## Which loop

Which loop should you use?

* Use a for loop when you know how many times you want to repeat something, like counting to 5.
* Use a while loop when you want to keep repeating as long as a condition is true.
* Use a do while loop when the instructions should happen at least once before checking the condition.

With any loop, make sure something can eventually make its condition false—or your program might keep looping forever.

Your computer will not stop looping until it runs out of memory!

---

## Bug Detective: while and do while

Detective hats on, team! These loops are supposed to repeat until it’s time to stop—but a few sneaky bugs are confusing them. Copy and run each program separately, then use the clue to investigate.

### Mystery 1: The missing 5

This program should print the numbers 1 through 5. Does it?

```cpp

#include <iostream>

int main() {
    int count = 1;

    while (count < 5) {
        std::cout << count << "\n";
        count++;
    }

    return 0;
}
```

* **Clue:** When count becomes 5, is count < 5 still true?

### Mystery 2: It never asks!

This program should keep asking until you enter 10 or more. Instead, it skips the question.

```cpp

#include <iostream>

int main() {
    int number = 0;

    while (number >= 10) {
        std::cout << "Enter 10 or more: ";
        std::cin >> number;
    }

    std::cout << "Great—you entered 10 or more!\n";
    return 0;
}
```

* **Clue:** What is number at the very first condition check?

### Mystery 3: It asks again when you got it right

This program should stop when you enter 10 or more. Try entering 12.

```cpp

#include <iostream>

int main() {
    int number = 0;

    do {
        std::cout << "Enter 10 or more: ";
        std::cin >> number;
    } while (number >= 10);

    std::cout << "Great—you entered 10 or more!\n";
    return 0;
}
```

* **Clue:** The do while repeats when its condition is true. Should it repeat when the number is 12?

### Mystery 4: A punctuation puzzle

This program should print 1, 2, and 3, but the compiler complains.

```cpp

#include <iostream>

int main() {
    int count = 1;

    do {
        std::cout << count << "\n";
        count++;
    } while (count <= 3)

    return 0;
}
```

* **Clue:** The do while loop needs a punctuation mark after its condition.

### Detective answer key

* Change count `< 5` to count `<= 5`.
* Change number `>= 10` to number `< 10`.
* Change number `>= 10` to number `< 10`.
* Add a semicolon after while (`count <= 3`).


