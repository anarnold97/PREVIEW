# Introduction to C++ (Part 7)

## Arrays and Storing Several Values

An array stores several values of the same type under one name. It’s like a row of boxes, with one value in each box.

```cpp


#include <iostream>

int main() {
    int scores[4] = {8, 10, 7, 9};

    std::cout << scores[0];

    return 0;
}
```

This array is called **scores**. 

It holds four numbers. 

To get one value, use its **index** —the number that tells C++ which box to look in.

Array indexes start at 0, so:

* scores[0] is 8
* scores[1] is 10
* scores[2] is 7
* scores[3] is 9


### Task 1

* Change the numbers in the array.

* Try printing a different value by changing the index.

## Using a Loop with an Array

* A for loop can visit each value in an array. This is especially useful when an array has lots of values.

```cpp


#include <iostream>

int main() {
    int scores[4] = {8, 10, 7, 9};

    for (int i = 0; i < 4; i++) {
        std::cout << scores[i] << "\n";
    }

    return 0;
}
```

The variable i is the index. It starts at 0 and increases each time the loop repeats. The loop stops when i is no longer less than 4.

Each time around, scores[i] means “the value in the box with index i.”

### Task 2

Change the scores and run the program again.

Add another score to the array. Remember to update the array’s size and the loop’s stopping number too.

> [!NOTE]
>
> An array with 4 values has indexes from 0 to 3—not 1 to 4. 
>
> Trying to use an index that is outside the array’s range can cause problems.
>

--- 

## Interesting fact

Frances Allen was a computer scientist whose work helped improve compilers—the programs that translate code so computers can run it. She was the first woman to receive the Turing Award, a major award in computing. 

Her work laid the foundation for advancements in compiler design and machine architecture, which impact modern computing technologies.
