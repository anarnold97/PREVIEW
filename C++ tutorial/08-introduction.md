# Introduction to C++ (Part 8)

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

This 2D array has 2 rows and 3 columns. Like a regular array, its indexes start at 0. So grid[0][1] means “the value in row 0, column 1, which is **2**.

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
1 3 5
7 8 9
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

---

## Arrays with Three or More Dimensions

A 2D array is like a table: it has rows and columns. Adding another dimension is like stacking several tables on top of each other. A 3D array uses three indexes to find a value: one for the stack, one for the row, and one for the column.

Arrays with four or more dimensions work the same way: each extra dimension adds another index. These are called multidimensional arrays. You might hear “3D array,” “4D array,” or “N-dimensional array,” where N means any number of dimensions.
Example: A Stack of Grids

This 3D array stores two grids, each with two rows and three columns:

```cpp

#include <iostream>

int main() {
    int cubes[2][2][3] = {
        {
            {1, 2, 3},
            {4, 5, 6}
        },
        {
            {7, 8, 9},
            {10, 11, 12}
        }
    };

    for (int layer = 0; layer < 2; layer++) {
        std::cout << "Layer " << layer << ":\n";

        for (int row = 0; row < 2; row++) {
            for (int column = 0; column < 3; column++) {
                std::cout << cubes[layer][row][column] << " ";
            }

            std::cout << "\n";
        }
    }

    return 0;
}
```

The first index chooses the layer, the second chooses the row, and the third chooses the column. For example, cubes[1][0][2] is 9.

A 4D array adds one more index. For example, a game might use four indexes for day, level, row, and column:

```cpp

int gameMaps[7][3][4][5];

Here, gameMaps[2][1][3][4] refers to a value on day 2, in level 1, row 3, column 4. Arrays with many dimensions can be harder to understand, so programmers usually choose a structure that matches the problem they’re solving.

```

---

## Bug Detective: Multi-Dimensional Arrays

Detective hats on, team! These programs use grids and stacks of grids, but sneaky bugs are hiding in their indexes and loops. Run each program separately and see what happens.

### Mystery 1: Find the right square

The program should print the value in row 1, column 2: 6.

```cpp

#include <iostream>

int main() {
    int grid[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    std::cout << grid[1][1];

    return 0;
}
```

* **Clue:** The first index is the row; the second is the column. Which column holds 6?

### Mystery 2: Where did the last column go?

The program should print all three values in each row.

```cpp

#include <iostream>

int main() {
    int grid[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    for (int row = 0; row < 2; row++) {
        for (int column = 0; column < 2; column++) {
            std::cout << grid[row][column] << " ";
        }

        std::cout << "\n";
    }

    return 0;
}
```
* **Clue:** The grid has 3 columns. How many column indexes should the inner loop visit?

### Mystery 3: Which layer?

The program should print 9, which is in layer 1, row 0, column 2.

```cpp

#include <iostream>

int main() {
    int cubes[2][2][3] = {
        {
            {1, 2, 3},
            {4, 5, 6}
        },
        {
            {7, 8, 9},
            {10, 11, 12}
        }
    };

    std::cout << cubes[0][1][2];

    return 0;
}
```

* **Clue:** The indexes go in this order: layer, row, column.


### Detective answer key

* Change `grid[1][1]` to `grid[1][2]`.
* Change column `< 2` to column `< 3`.
* Change `cubes[0][1][2]` to `cubes[1][0][2]`.
