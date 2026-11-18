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


### Task 2

* Try changing the number 10 or the messages.

---

## Infinite Loop

An infinite loop is a set of instructions in a computer program that keeps repeating forever because it never reaches a stopping point. 

It's like a game that keeps going without ever ending unless someone turns it off.

---

## Bug Detective: Making Choices

Detective hats on, team! The program is deciding whether someone is 10 or older—but some sneaky bugs are messing with its choices. Run each program separately and test the age shown in its clue.

### Mystery 1: What about exactly 10?

```cpp

#include <iostream>

int main() {
    int age;

    std::cout << "How old are you? ";
    std::cin >> age;

    if (age > 10) {
        std::cout << "You are 10 or older!";
    } else {
        std::cout << "You are younger than 10.";
    }

    return 0;
}
```

Try entering 10.

* **Clue:** Does > include 10, or only numbers bigger than 10?

### Mystery 2: Backwards answers

```cpp

#include <iostream>

int main() {
    int age;

    std::cout << "How old are you? ";
    std::cin >> age;

    if (age >= 10) {
        std::cout << "You are younger than 10.";
    } else {
        std::cout << "You are 10 or older!";
    }

    return 0;
}
```

Try entering 8.

* **Clue:** The condition checks correctly. Do the messages match the branches?

### Mystery 3: Exactly 10—or 10 and older?

```cpp

#include <iostream>

int main() {
    int age;

    std::cout << "How old are you? ";
    std::cin >> age;

    if (age == 10) {
        std::cout << "You are 10 or older!";
    } else {
        std::cout << "You are younger than 10.";
    }

    return 0;
}
```

Try entering 12.

* **Clue:** `==`` checks whether the age is exactly 10. Which condition also includes ages above 10?

### Detective answer key

* Change `age > 10` to `age >= 10`.
* Swap the two messages so each matches its branch.
* Change `age == 10` to age `>= 10`.

---

## Interesting fact

Katherine Johnson worked at NASA, where they were figuring out how to send humans safely into space. Trajectories — the paths spacecraft take — depend on thousands of mathematical calculations, and in the early days, people had to do many of them by hand.

Katherine was so brilliant at this that the astronauts asked for her personally. Before John Glenn's orbital flight in 1962, the new electronic computers produced the numbers — but Glenn didn't fully trust the unfamiliar machine. He said: "get the girl to check the numbers. If she says they're good, then I'm ready to go".

The woman checked the computer. And the computer's math was good, because Katherine had checked it.

She described herself simply: "I'm just a girl who likes to count." She counted her way to the Moon and back, at a time when many people made things difficult for women — and for Black women especially — in science. The mathematics never minded. It worked for anyone who loved it.

So when you check your code before running it — look at every line, test every path — you're doing exactly what the astronauts trusted Katherine Johnson to do. Always check like Katherine, because one day, people could depend on your code too.