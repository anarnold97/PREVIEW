# Introduction to C++ (Part 6) 

## How did you do?

* If you managed - WELL DONE

* If you could not manage - DO NOT WORRY - you are learning. This is actually pretty high level logic! Grad students get this wrong.

### The Solution

```cpp

#include <iostream>

int main() {
    for (int table = 1; table <= 12; table++) {
        for (int multiplier = 1; multiplier <= 12; multiplier++) {
            int answer = table * multiplier;

            std::cout << table << " x " << multiplier
                      << " = " << answer << "   ";
        }

        std::cout << "\n";
    }

    return 0;
}
```

#### How It Works

The program uses two `for` loops, one inside the other. This is called a `nested loop`.

The outer loop chooses which times table to print:


```cpp

for (int table = 1; table <= 12; table++)
```

It starts with table set to 1. After each time table is printed, `table++` increases it by one. The loop stops after table reaches 12.

The inner loop prints the equations for the current table:

```cpp

for (int multiplier = 1; multiplier <= 12; multiplier++)
```

For each value of table, multiplier counts from 1 to 12.

This line calculates the answer:

```cpp

int answer = table * multiplier;
```

For example, when table is 3 and multiplier is 4, the answer is 12.

These lines print the equation:

```cpp

std::cout << table << " x " << multiplier
          << " = " << answer << "   ";
```

The `<<`` symbols send each piece of the equation to the screen. The spaces at the end help separate the sums.

Finally, this line starts a new line:

```cpp

std::cout << "\n";
```

It comes after the inner loop, so the program prints all 12 equations before moving to the next line. Once the inner loop finishes, the outer loop moves on to the next times table.

> [!NOTE]
>
> If you didn’t get it yet, that’s okay. Nested loops can take a little time to understand, and getting stuck is part of learning to program. 
>
> Try tracing the loops one step at a time (and this is a great skill to learn). We call it **debugging**.
>
> Or ask a friend or teacher to work through one line with you.
>
> A quote often attributed to Thomas Edison says:
>
> “I have not failed. I’ve just found 10,000 ways that won’t work.”
>
> Keep experimenting and you **WILL** get there!
> 

---

## Interesting fact

Sophie Wilson helped design the ARM processor with her colleague Steve Furber. A processor is the tiny chip that carries out a computer’s instructions. ARM designs are now used in billions of devices, including smartphones. So the phone in your pocket has a little piece of Sophie’s work inside it. 

Sophie and her team also built a working prototype of the BBC Micro in less than a week. That’s a reminder that small teams can build big things when everyone brings their skills—and remembers to sleep eventually. 

So remember that hardware and code work together, and you don’t have to build something huge to make a huge difference. A tiny chip can help power a whole lot of cat videos.
