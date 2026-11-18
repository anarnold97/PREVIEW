# Introduction to C++ (Part 0)

## How Computers Follow Our Instructions

Imagine a computer is a very fast robot. It can do amazing things—but it’s also very literal. If you tell it, “Make me a sandwich,” it might stare at the bread forever unless you explain every step.

That’s where programming comes in!

## What’s a programming language?

A programming language is a way for people to write instructions that a computer can use.

For example, in C++ you can write:

```cpp

std::cout << "Hello!";
```

That means: you are telling the computer "show the words Hello! on the screen.”

Programming languages have rules—just like spelling and grammar. Computers are picky readers. A missing symbol can make them say, “I have no idea what you mean!” (Computers are not famous for guessing.)

## How does a program work?

* A person writes code—instructions in a programming language.
* The computer translates or reads the code so it can work with it.
* The computer follows the instructions, very quickly.
* Something happens: words appear, a game character jumps, or a robot starts dancing.

The things that happen are called the program’s output. Hopefully the robot dances. If it starts mailing cheese to your teacher, check the code.

## What’s a compiler?

A compiler is a translator that converts a whole program into instructions the computer can run.

Think of writing a whole recipe in English, then having a translator turn the entire recipe into Robot Language before the robot starts cooking.

A compiler can also point out some mistakes before the program runs—like a missing bracket or a word the language doesn’t recognize. It won’t always catch every problem, though. It might translate your instructions perfectly even if they tell the robot to put ice cream in a sock.

C++ programs are usually compiled before they run.

## What’s an interpreter?

An interpreter reads a program and carries out its instructions as it goes—more like a translator who reads one line of a recipe aloud, then waits while the robot does that step.

If something is wrong, the interpreter may stop when it reaches the confusing instruction.

Many programming languages are commonly run with an interpreter, though real languages and tools can work in more complicated ways.

## Compiler vs. interpreter

* Compiler: translates the program first, then the computer runs it.
* Interpreter: reads and carries out the program as it goes.

Both help the computer understand what the programmer wants. They’re like two different ways to explain a recipe to a robot chef.

You’ll meet some strange-sounding words as we go. You don’t have to memorize them as we’ll explain them when they show up. So here is a tiny glossary

* Code: Instructions written for a computer.
* Program: A set of instructions that does a job.
* Programming language: A language used to write code, such as C++.
* Compiler: A tool that translates a whole program before it runs.
* Interpreter: A tool that reads and carries out instructions as it goes.
* Computer: The machine that follows instructions—sometimes too literally.
* Processor (CPU): The part of the computer that carries out instructions. Think of it as the very busy worker in the computer.
* Input: Information given to a program, such as a button press or a number.
* Output: What a program produces, such as a message, picture, or sound.
* Bug: A mistake in a program. Not a real bug—please don’t look under the keyboard.
* Debugging: Finding and fixing bugs. It’s detective work, but the clues are usually missing commas.
* Run: To start a program and let the computer follow its instructions.

**Oh it all sounds so complicated!!!**

Yes, it is. But it will help your code if you know what is happening when you run a program.  

## Mistakes

Don’t worry if your code has mistakes—even the world’s best programmers make them! Sometimes a tiny, sneaky mistake can be hard to spot, like finding one missing sprinkle on a giant cupcake. The important thing isn’t to get everything perfect the first time: it’s to test your code, learn what went wrong, and try again. Every bug you fix makes you a better programmer!

Here’s a real-life example. In 1996, the first Ariane 5 rocket launched carrying science satellites. About 37 seconds after liftoff, a problem in its guidance software meant it lost reliable information about how it was moving. The rocket veered off course and was automatically destroyed for safety. Some software had been reused from an older rocket, but its assumptions hadn’t been tested well enough for the new rocket. It wasn’t just one person’s mistake—it was a chain of problems that better testing could have caught. The lesson? Reusing code can be helpful, but you still have to check that it works in its new home. 

We all make mistakes, so successful coding is a team effort. You might be good at writing code, or you might be good at finding bugs. 

---

## Interesting fact

Ada Lovelace was born in England in 1815. Her father was Lord Byron, one of the most famous poets in the world — but her mother decided poetry was too wild, and raised Ada on mathematics instead.

When Ada was a teenager, she met Charles Babbage, an inventor who had drawn plans for a giant mechanical computer called the Analytical Engine. It was full of gears and punch cards — but he never finished building it. The machine existed only on paper.

Most people looked at the drawings and saw a very fancy calculator. Ada Lovelace saw something bigger. She realized that if a machine could follow instructions about numbers, it could follow instructions about anything — even music.

In 1843, Ada wrote out detailed instructions for the machine — the first published computer algorithm. She wrote the world's first program for a computer made entirely of imagination.

More than a hundred years later, real computers were built — and they worked exactly the way Ada had seen they could. Which is why she is remembered as the first computer programmer.

Every program you write starts the same way hers did: with an idea, and the instructions to make it real.