# Introduction to C++ (Part 11)

## Working with Text

Let us get stringy like string cheese!

A `std::string` stores text, such as a name, a word, or a whole sentence. To use strings, include the `<string>` header.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name = "Maya";

    std::cout << name << "\n";

    return 0;
}
```

The variable name stores the text "Maya". Put text values inside double quotation marks.

### Joining Strings

You can join strings using `+`. This is called **concatenation**.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string firstName = "Maya";
    std::string greeting = "Hello, " + firstName + "!";

    std::cout << greeting << "\n";

    return 0;
}
```

It prints:

```text

Hello, Maya!
```

You can also add a space between two words:

```cpp

std::string fullName = firstName + " " + "Chen";
```

### Reading a Word

`std::cin` can read a word from the keyboard. It stops reading when it reaches a space.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string favoriteColor;

    std::cout << "What is your favorite color? ";
    std::cin >> favoriteColor;

    std::cout << "You chose " << favoriteColor << "!\n";

    return 0;
}
```

If you type `bright blue`, this program reads only `bright`.

### Reading a Whole Line

To read a sentence, use std::getline. It keeps reading until you press Enter.
cpp

#include <iostream>
#include <string>

int main() {
    std::string favoriteGame;

    std::cout << "What game do you like? ";
    std::getline(std::cin, favoriteGame);

    std::cout << "You like " << favoriteGame << "!\n";

    return 0;
}

Now you can type a response with spaces, such as hide and seek.

### Finding a String’s Length

The `.length()` function tells you how many characters are in a string. Spaces and punctuation count too.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string word = "robot";

    std::cout << word.length() << "\n";

    return 0;
}
```

It prints 5, because "robot" has five characters.

### Getting One Character

You can use an index to get one character from a string. Just like array indexes, string indexes start at 0.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string word = "robot";

    std::cout << word[0] << "\n";
    std::cout << word[3] << "\n";

    return 0;
}
```

It prints:

```text

r
o
```

The character at index 0 is r; the character at index 3 is o. Make sure an index is less than the string’s length—otherwise, it can refer to a position outside the string.

### Task 1

Create a string called `petName` and print a sentence that includes it, such as `My pet is Noodle!`.

#### Solution 1

```cpp

#include <iostream>
#include <string>

int main() {
    std::string petName = "Noodle";

    std::cout << "My pet is " << petName << "!\n";

    return 0;
}
```

### Task 2

Ask the user for their first name and favorite animal. Print a sentence using both answers. For this task, each answer can be a single word.

#### Solution 2

```cpp

#include <iostream>
#include <string>

int main() {
    std::string name;
    std::string animal;

    std::cout << "What is your first name? ";
    std::cin >> name;

    std::cout << "What is your favorite animal? ";
    std::cin >> animal;

    std::cout << name << " likes " << animal << "!\n";

    return 0;
}
```

### Task 3

Create a string called secretWord. Print its length and its first character.

#### Solution 3

```cpp

#include <iostream>
#include <string>

int main() {
    std::string secretWord = "dragon";

    std::cout << "The word has " << secretWord.length()
              << " characters.\n";
    std::cout << "Its first character is " << secretWord[0] << ".\n";

    return 0;
}
```

## Bug Detective: Strings

Detective hats on, team! Each program has a bug. Find and fix it.

### Mystery 1: The missing header

The program should create and print a string, but it is missing something it needs.

```cpp

#include <iostream>

int main() {
    std::string message = "Hello!";
    std::cout << message << "\n";

    return 0;
}
```

* **Clue:** Which header lets a program use `std::string`?

### Mystery 2: The wrong character

The program should print the first character of cat, which is c.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string animal = "cat";

    std::cout << animal[1] << "\n";

    return 0;
}
```

* **Clue:** What index do strings start at?

### Mystery 3: The sentence gets cut short

The program should let the user type a whole sentence, including spaces.

```cpp

#include <iostream>
#include <string>

int main() {
    std::string sentence;

    std::cout << "Type a sentence: ";
    std::cin >> sentence;

    std::cout << sentence << "\n";

    return 0;
}
```

* **Clue:** Which input command reads a whole line?

### Detective answer key

* Add `#include <string>`.
* Change `animal[1]` to `animal[0]`.
* Replace `std::cin >> sentence;` with `std::getline(std::cin, sentence);`.


### A Small Challenge: Word Detective

Ask the user to type a word. Print how many characters it has and show its first character. Then, try changing the program to ask for a whole sentence instead.
