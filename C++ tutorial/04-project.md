# Introduction to C++ (Part 4 project)

## Project: FizzBuzz

Let’s teach the computer a counting game! It will count from 1 to 30, but sometimes it will say a silly word instead of a number.

### The rules

For each number:

* If it divides evenly by 3 and 5, print **FizzBuzz**.
* Otherwise, if it divides evenly by 3, print **Fizz**.
* Otherwise, if it divides evenly by 5, print **Buzz**.
* If none of those are true, print the number.

“Divides evenly” means there’s nothing left over. For example, 10 divides evenly by 5, but 11 doesn’t.

#### New tools for the game

* `%` finds the remainder. So `10 % 5` is `0`, but `11 % 5` is `1`.
* `==`` asks “are these values equal?” For example, `10 % 5 == 0` asks, “Is the remainder zero?”
* `&&` means **AND**. Both checks must be **true**.


> [!WARNING]
>
> Watch out: `=`` stores a value, while `==`` compares two values. One equals sign gives something a name tag; two ask if the name tags match!
>

### Step-by-step walkthrough

* Start a counting loop. We want the computer to count from 1 through 30:

	```cpp
		for (int number = 1; number <= 30; number++) {
	    // We will decide what to print here.
	  }
	```  

* Check for numbers divisible by both 3 and 5. We check this first because 15 divides evenly by both. If we checked for 3 first, the computer would print Fizz and never get to FizzBuzz.

	```cpp

		if (number % 3 == 0 && number % 5 == 0) {
		std::cout << "FizzBuzz\n";
		}
	```	

* Check for numbers divisible by 3:

	```cpp
	    else if (number % 3 == 0) {
	        std::cout << "Fizz\n";
	    }
	```

* Check for numbers divisible by 5:

	```cpp
	    else if (number % 5 == 0) {
	        std::cout << "Buzz\n";
	    }
	```

* Print the number if none of the checks matched:

	```cpp
	    else {
	        std::cout << number << "\n";
	    }
	```

* Put it all together and run your program:

	```cpp

	    #include <iostream>

	    int main() {
	        for (int number = 1; number <= 30; number++) {
	            if (number % 3 == 0 && number % 5 == 0) {
	                std::cout << "FizzBuzz\n";
	            } else if (number % 3 == 0) {
	                std::cout << "Fizz\n";
	            } else if (number % 5 == 0) {
	                std::cout << "Buzz\n";
	            } else {
	                std::cout << number << "\n";
	            }
	        }

	        return 0;
	    }
	```

* Test your program

Check that a few numbers produce the right result:

* 3 prints `Fizz
* 5 prints `Buzz
* 15 prints FizzBuzz
* 16 prints 16

If one of them is wrong, don’t panic! You’ve discovered a bug—and now you get to be the detective.

---

## Extra challenge: 

Change the game so it counts to 50, or invent your own words and numbers.

---

## Bug Detective Challenge

Each program below has a bug. Copy and run one at a time, then use the clue to investigate. 

Detective hats optional; magnifying glasses mostly make the keyboard harder to use.

### Mystery 1: Where did FizzBuzz go?

This program tests the number 15. What does it print?

```cpp

#include <iostream>

int main() {
    int number = 15;

    if (number % 3 == 0) {
        std::cout << "Fizz\n";
    } else if (number % 5 == 0) {
        std::cout << "Buzz\n";
    } else if (number % 3 == 0 && number % 5 == 0) {
        std::cout << "FizzBuzz\n";
    } else {
        std::cout << number << "\n";
    }

    return 0;
}
```

* **Clue:** The computer stops at the first rule that matches.

### Mystery 2: The missing number

This program should count from 1 through 30. Does it?

```cpp

#include <iostream>

int main() {
    for (int number = 1; number < 30; number++) {
        if (number % 3 == 0 && number % 5 == 0) {
            std::cout << "FizzBuzz\n";
        } else if (number % 3 == 0) {
            std::cout << "Fizz\n";
        } else if (number % 5 == 0) {
            std::cout << "Buzz\n";
        } else {
            std::cout << number << "\n";
        }
    }

    return 0;
}
```

* **Clue:** Look closely at the loop’s stopping check. Does it include 30?


### Mystery 3: The wrong kind of math

This program checks the number 3. It should print Fizz. What does it print instead?

```cpp

#include <iostream>

int main() {
    int number = 3;

    if (number / 3 == 0) {
        std::cout << "Fizz\n";
    } else {
        std::cout << number << "\n";
    }

    return 0;
}
```

* **Clue:** / divides. Which operator finds the remainder?

### Detective answer key

* Check “divisible by both 3 and 5” first, before checking 3 or 5 separately.
* Change number `< 30` to number `<= 30` so the loop includes 30.
* Use `%` instead of `/` to check the remainder.

