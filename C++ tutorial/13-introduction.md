# Introduction to C++ (Part 13)

## Grouping Related Information with Structs

A program might need to store several pieces of information about one thing. For example, a robot car could have a name, a speed, and a battery level. A struct lets you group those values together.

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int speed;
    int batteryLevel;
};

int main() {
    Robot car = {"Zoomer", 5, 80};

    std::cout << car.name << "\n";
    std::cout << car.speed << "\n";
    std::cout << car.batteryLevel << "\n";

    return 0;
}
```

Robot is the name of the new type. Its members are name, speed, and batteryLevel. The variable car is one Robot, and dots let us access its members—for example, car.name.

### Changing a Member

You can update a member just like an ordinary variable:

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int speed;
    int batteryLevel;
};

int main() {
    Robot car = {"Zoomer", 5, 80};

    car.speed = 8;
    car.batteryLevel = 75;

    std::cout << car.name << " is moving at speed "
              << car.speed << ".\n";
    std::cout << "Battery: " << car.batteryLevel << "%\n";

    return 0;
}
```

The program changes the car’s speed and battery level, then prints the updated values.

### Making More Than One Struct

Each variable with type Robot gets its own set of members.

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int speed;
};

int main() {
    Robot car1 = {"Zoomer", 5};
    Robot car2 = {"Dash", 3};

    car1.speed = 7;

    std::cout << car1.name << ": " << car1.speed << "\n";
    std::cout << car2.name << ": " << car2.speed << "\n";

    return 0;
}
```

* Changing `car1.speed` doesn’t change `car2.speed`.

---

## Task 1

Create a Pet struct with a name and an age. Make one pet and print its information.

#### Solution 1

```cpp

#include <iostream>
#include <string>

struct Pet {
    std::string name;
    int age;
};

int main() {
    Pet myPet = {"Noodle", 4};

    std::cout << myPet.name << " is "
              << myPet.age << " years old.\n";

    return 0;
}
```

### Task 2

Create a Robot struct with a name and a battery level. Make a robot, change its battery level, and print the new level.

#### Solution 2

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int batteryLevel;
};

int main() {
    Robot car = {"Zoomer", 80};

    car.batteryLevel = 65;

    std::cout << car.name << " battery: "
              << car.batteryLevel << "%\n";

    return 0;
}
```

### Task 3

Create a GameCharacter struct with a name and a number of lives. Make two characters and print each character’s name and lives.

#### Solution 3

```cpp

#include <iostream>
#include <string>

struct GameCharacter {
    std::string name;
    int lives;
};

int main() {
    GameCharacter hero = {"Comet", 3};
    GameCharacter sidekick = {"Pip", 2};

    std::cout << hero.name << " has "
              << hero.lives << " lives.\n";

    std::cout << sidekick.name << " has "
              << sidekick.lives << " lives.\n";

    return 0;
}
```

---

## Bug Detective: Structs

Detective hats on, team! Find the mistake in each program.

### Mystery 1: The missing member

The program should print the robot’s name, but it won’t compile.

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int speed;
};

int main() {
    Robot car = {"Zoomer", 5};

    std::cout << car.robotName << "\n";

    return 0;
}
```

* **Clue:** Check the member names in the Robot struct. Is there a member called robotName?

### Mystery 2: The wrong value

The program should change the robot’s speed to 8.

```cpp

#include <iostream>
#include <string>

struct Robot {
    std::string name;
    int speed;
};

int main() {
    Robot car = {"Zoomer", 5};

    car.name = 8;

    std::cout << car.speed << "\n";

    return 0;
}
```

* **Clue:** Which member stores the robot’s speed?

### Mystery 3: The missing dot

The program should print the character’s name.

```cpp

#include <iostream>
#include <string>

struct GameCharacter {
    std::string name;
    int lives;
};

int main() {
    GameCharacter hero = {"Comet", 3};

    std::cout << hero name << "\n";

    return 0;
}
```

* **Clue:** What symbol goes between the variable name and the member name?

### Detective answer key

* Change `car.robotName` to `car.name`.
* Change `car.name = 8;` to `car.speed = 8;`.
* Change `hero name` to `hero.name`.

---

## A Small Challenge: Robot Car

Create a RobotCar struct with a name, speed, and battery level. Make a car, update its speed, then print all three details. What other information might be useful to keep about a robot car?
