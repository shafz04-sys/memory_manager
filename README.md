# OS Memory Management Simulator

An interactive simulation of Operating System memory management techniques, implemented in Python using CustomTkinter. The project visualizes **Contiguous Memory Allocation** (Variable Partitioning) and also **Non-Contiguous Paging**, showing concepts like fragmentation, swapping, and page tables.

## Table of Contents
- [OS Memory Management Simulator](#os-memory-management-simulator)
  - [Features & Algorithms](#features--algorithms)
    - [Contiguous Memory Allocation](#contiguous-memory-allocation)
    - [Paging (Non-Contiguous Allocation)](#paging-non-contiguous-allocation)
    - [First Fit](#first-fit)
    - [Best Fit](#best-fit)
    - [Worst Fit](#worst-fit)
    - [Memory Compaction](#memory-compaction)
    - [Swapping Mechanism](#swapping-mechanism)
  - [Installation](#installation)
  - [Usage Guide](#usage-guide)
  - [Contributors](#contributors)

## Features & Algorithms

### Contiguous Memory Allocation
- **Variable Partitioning:** The simulator manages memory as a continuous block. Processes are allocated specific contiguous chunks of RAM.
- **Visual Representation:** The gui displays a linear memory bar where users can see exactly where a process resides and where holes are located.
- **External Fragmentation:** Visually demonstrates how loading and unloading processes of different sizes creates unusable gaps between allocated blocks.

### Paging (Non-Contiguous Allocation)
- **Grid-Based Visualization:** Unlike contiguous allocation, paging helps us visualize memory as a grid of fixed-size frames.
- **Scattered Allocation:** Demonstrates how a single process can be broken into pages and scattered across various physical frames, this solves external fragmentation.
- **Page Table Inspector:** This feature allows us to select a Process ID and view the exact Page-to-Frame mapping table, bridging link between logical and physical addresses.
- **Internal Fragmentation:** Visually highlights wasted space within the last frame of a process when the process size is not a perfect multiple of the frame size.

### First Fit
- **First Fit** is an allocation strategy that searches the list of free memory blocks from the beginning and allocates the *first* block that is large enough to hold the process.
- It is usually faster because it minimizes the search time, but it tends to concentrate allocation at the start of memory, leaving small, unusable holes at the beginning.

### Best Fit
- **Best Fit** searches the entire list of free memory blocks and allocates the *smallest* hole that is big enough to hold the process.
- This strategy attempts to minimize wasted space by leaving the smallest possible leftover hole but it often results in creating tiny, useless fragments that are too small to be used by any future process.

### Worst Fit
- **Worst Fit** searches the entire list and allocates the *largest* available hole.
- The philosophy behind this is that the remaining leftover hole will be large enough to be useful for another process thus preventing the creation of tiny, unusable fragments but consumes the largest contiguous blocks quickly.

### Memory Compaction
- **Defragmentation:** The simulator includes a compact feature for the Contiguous Memory mode.
- When triggered, it shifts all active processes to the top of the memory addresses (0x00) and merges all scattered free holes into one large, usable block at the bottom. This effectively solves the issue of external fragmentation, earlier OS used to implement such compaction systems in order to reduce/eliminate fragmentation

### Swapping Mechanism
- **Virtual Memory Simulation:** My project implements a working swapping system. When Main Memory (RAM) is full, the system automatically identifies a "victim" process.
- **Backing Store:** The victim process is moved to a secondary "Disk" visualization. When space becomes available (or the user requests it), the process can be swapped back into RAM. This simulates and shows the lifecycle of a process moving between Ready and Suspended states.

## Installation
1- Clone the repository

2- Install (CustomTkinter)
```bash
pip install customtkinter
```

3- Run the application
```bash
python gui.py
```

## Usage Guide
The application is split into two main tabs:

**Tab 1: Older OS (Contiguous)**
- **Input:** Enter a Process ID (e.g., "P1") and Size (KB).
- **Select Algorithm:** Choose First Fit, Best Fit, or Worst Fit from the dropdown.
- **Allocate:** Click to place the process in RAM.
- **Compact:** If fragmentation prevents allocation, click "Run Compaction" to merge free space.

**Tab 2: Modern OS (Paging)**
- **Input:** Enter Process ID and Size.
- **Allocate:** The system automatically divides the process into pages and assigns them to random free frames.
- **Inspector:** Use the "Inspector" dropdown to select a process and view its Page Table (Logical Page # -> Physical Frame #).

## Contributors

- [Shafwath Tamjid](https://github.com/shafz04-sys)
