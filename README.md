# CPP_REPL: Experimental
The C++ REPL sits on LLVM's Clang frontend libraries and is driven from an interactive Python shell.

This interactive shell allows developers to run and test any C++ code on the fly.



This project is based on the concept of building the binary bridge between the C++ and Python runtimes.



## Preview (Demo)

Here is a showcase of what interacting with CPP_REPL feels like.

![Alt Text](https://raw.githubusercontent.com/BeAllAround/CPP_REPL/refs/heads/main/Demo/Demo01Gif.gif)





## Inspiration and Dependencies

This project is inspired by the [LLVM Compiler Infrastructure Project](https://github.com/llvm/llvm-project).

It integrates directly with LLVM’s [clang-repl](https://github.com/llvm/llvm-project/tree/main/clang/tools/clang-repl) (the official Clang JIT / REPL).  
The C++ REPL itself is _**NOT**_ built or implemented from scratch ***in any shape or form***; this project embeds and drives the existing clang-repl infrastructure.
