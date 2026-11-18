# Introduction to C++ (Part 14)

## Classes and Objects

A class is like a plan for making things in a program. An object is one thing made from that plan. A class can group information together and include functions that work with that information.

Here’s a class for a robot car:

```cpp

#include <iostream>
#include <string>

class RobotCar {
public:
    std::string name;
    int speed;

    void drive() {
        std::cout << name << " is driving at speed "
                  << speed << ".\n";
    }

    void stop() {
        speed = 0;
        std::cout << name << " has stopped.\n";
    }
};

int main() {
    RobotCar car;

    car.name = "Zoomer";
    car.speed = 5;

    car.drive();
    car.stop();

    return 0;
}
```

* `RobotCar` is the `class. `car` is an object made from that class. The variables name and speed store information; `drive` and `stop` are **member functions**, also called **methods**. They belong to the class and can use its information.

### What Does public Mean?

In a class, members are **private** by default, which means code outside the class cannot use them directly. 

The word **public**: makes the members below it available to the rest of the program.

In this example, main can set car.name and call car.drive() because they are under public:.

### Making More Than One Object

You can create several objects from the same class. Each object has its own information.

```cpp

#include <iostream>
#include <string>

class RobotCar {
public:
    std::string name;
    int speed;

    void drive() {
        std::cout << name << " is driving at speed "
                  << speed << ".\n";
    }
};

int main() {
    RobotCar car1;
    car1.name = "Zoomer";
    car1.speed = 5;

    RobotCar car2;
    car2.name = "Dash";
    car2.speed = 3;

    car1.drive();
    car2.drive();

    return 0;
}
```

Changing `car1.speed` would not `change car2.speed`. Each object keeps its own values.

### Task 1

Create a GameCharacter class with a name and a lives value. Make an object and print its information.

#### Solution 1

```cpp

#include <iostream>
#include <string>

class GameCharacter {
public:
    std::string name;
    int lives;
};

int main() {
    GameCharacter hero;

    hero.name = "Comet";
    hero.lives = 3;

    std::cout << hero.name << " has "
              << hero.lives << " lives.\n";

    return 0;
}
```

### Task 2

Add a cheer method to the GameCharacter class. It should print the character’s name followed by is ready!.

#### Solution 2

```cpp

#include <iostream>
#include <string>

class GameCharacter {
public:
    std::string name;
    int lives;

    void cheer() {
        std::cout << name << " is ready!\n";
    }
};

int main() {
    GameCharacter hero;

    hero.name = "Comet";
    hero.lives = 3;

    hero.cheer();

    return 0;
}
```

### Task 3

Create a RobotCar class with a name and a speed. Add a stop method that changes the speed to 0. Print the speed before and after stopping.

#### Solution 3

```cpp

#include <iostream>
#include <string>

class RobotCar {
public:
    std::string name;
    int speed;

    void stop() {
        speed = 0;
    }
};

int main() {
    RobotCar car;

    car.name = "Zoomer";
    car.speed = 5;

    std::cout << "Speed before stopping: " << car.speed << "\n";

    car.stop();

    std::cout << "Speed after stopping: " << car.speed << "\n";

    return 0;
}
```

---

## Bug Detective: Classes and Objects

Detective hats on, team! Find the mistake in each program.

### Mystery 1: Missing public

The program should print the robot’s name, but it cannot access it.

```cpp

#include <iostream>
#include <string>

class Robot {
    std::string name;
};

int main() {
    Robot car;
    car.name = "Zoomer";

    std::cout << car.name << "\n";

    return 0;
}
```

* **Clue:** Class members are private by default. What label makes name available to main?

### Mystery 2: Calling the method incorrectly

The program should make the robot drive.

```cpp

#include <iostream>
#include <string>

class Robot {
public:
    std::string name;

    void drive() {
        std::cout << name << " is driving!\n";
    }
};

int main() {
    Robot car;
    car.name = "Zoomer";

    car.drive;

    return 0;
}
```

* **Clue:** What punctuation shows that a function is being called?

### Mystery 3: The method changes the wrong object

The method should set the car’s speed to 0.

```cpp

#include <iostream>

class RobotCar {
public:
    int speed;

    void stop() {
        speed = 5;
    }
};

int main() {
    RobotCar car;
    car.speed = 8;

    car.stop();

    std::cout << car.speed << "\n";

    return 0;
}
```

* **Clue:** What value should speed have after the car stops?

### Detective answer key

* Add `public:` before `std::string name;`.
* Change `car.drive;` to `car.drive();`.
* Change `speed = 5;` to `speed = 0;`.


---

## A Small Challenge: Robot Remote

Create a RobotCar class with a name and speed. Add methods called drive and stop. Make a car, drive it, stop it, and print its speed after it stops.
