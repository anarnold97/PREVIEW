# Introduction to C++ (Part 5)

## Storing Values in Rows and Columns

A regular array stores values in a single row. A 2D array stores values in rows and columns, like a grid or a table.

```
cpp


#include <iostream>

int main() {
    int grid[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    std::cout << grid[0][1];

    return 0;
}
```

This 2D array has 2 rows and 3 columns. Like a regular array, its indexes start at 0. So grid[0][1] means “the value in row 0, column 1,” which is 2.

### Using Nested Loops with a 2D Array

A nested loop can visit every value in the grid. The outer loop goes through the rows, and the inner loop goes through the columns.

```cpp


#include <iostream>

int main() {
    int grid[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    for (int row = 0; row < 2; row++) {
        for (int column = 0; column < 3; column++) {
            std::cout << grid[row][column] << " ";
        }

        std::cout << "\n";
    }

    return 0;
}
```

* The inner loop prints each value in one row. Then std::cout << "\n"; moves to a new line before the outer loop continues to the next row.

* The program prints:

    ``` text

    1 2 3
    4 5 6
    ```

### Task 1

* Change some of the numbers in the grid.

* Change the grid to have 3 rows and 3 columns. Update the array and the loops to match.

#### Solution 1

The loops use row `< 3` and column `< 3` so they visit every value.

```cpp

#include <iostream>

int main() {
    int grid[3][3] = {
        {2, 4, 6},
        {1, 3, 5},
        {7, 8, 9}
    };

    for (int row = 0; row < 3; row++) {
        for (int column = 0; column < 3; column++) {
            std::cout << grid[row][column] << " ";
        }

        std::cout << "\n";
    }

    return 0;
}
```

It prints:

```text

2 4 6
```


### Task 2

Make a small game map using numbers. For example, use 0 for an empty space and 1 for a wall. Print the map using nested loops.

> [!NOTE]
>
> A row-and-column grid is one way computers can represent a game map or a picture made of pixels. Each position in the grid stores information about that spot.

#### Solution 2: A Small Game Map

Here, `0` means an empty space and `1` means a wall. The nested loops print the map row by row.

```cpp

#include <iostream>

int main() {
    int map[4][5] = {
        {1, 1, 1, 1, 1},
        {1, 0, 0, 0, 1},
        {1, 0, 1, 0, 1},
        {1, 1, 1, 1, 1}
    };

    for (int row = 0; row < 4; row++) {
        for (int column = 0; column < 5; column++) {
            std::cout << map[row][column] << " ";
        }

        std::cout << "\n";
    }

    return 0;
}
```

It prints:

```text

1 1 1 1 1
1 0 0 0 1
1 0 1 0 1
1 1 1 1 1
```

---

## Interesting fact

Katherine Johnson was a mathematician whose calculations helped NASA plan spacecraft journeys, including the Apollo missions to the Moon. 
NASA

Her calculations of orbital mechanics as a NASA employee were critical to the success of the first and subsequent U.S. crewed spaceflights. 

Yet she said of herself " I am just a girl who loved to count."