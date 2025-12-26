# OS Memory Management Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/Interface-CustomTkinter-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

A powerful, interactive Operating System simulator that visualizes **Contiguous Memory Allocation** (Variable Partitioning) and **Non-Contiguous Paging** techniques. Designed to demonstrate complex OS concepts like fragmentation, swapping, and address translation in real-time.

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Algorithms Implemented](#algorithms-implemented)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)

## 📖 About the Project

This application simulates how an Operating System manages Random Access Memory (RAM). It bridges the gap between theoretical concepts and practical implementation by providing a visual interface for allocating, deallocating, and swapping processes.

Users can experiment with different allocation strategies, trigger memory compaction to solve fragmentation, and inspect page tables to understand how logical addresses map to physical frames.

## ✨ Key Features

### 🧠 1. Contiguous Memory Manager (Variable Partitioning)
* **Dynamic Allocation:** visually allocates memory blocks of varying sizes.
* **Swapping Mechanism:** Automatically identifies "victim" processes and swaps them to a secondary **Disk (Virtual Memory)** when RAM is full, restoring them later when space becomes available.
* **Memory Compaction:** Includes a "Defragmentation" tool that coalesces scattered free holes into a single usable block, solving external fragmentation.
* **Real-time Visualization:** Dual-canvas display showing the state of Main Memory vs. Backing Store (Disk).

### 📄 2. Paging Memory Manager (Non-Contiguous)
* **Scattered Frame Visualization:** Uses a grid-based system to demonstrate how a single process is broken into pages and scattered across non-adjacent physical frames.
* **Page Table Inspector:** A built-in inspection tool that allows users to select any active Process ID and view its exact Page-to-Frame mapping.
* **Internal Fragmentation:** Visually represents wasted space within the last frame of a process.
* **Randomized Allocation:** Simulates realistic physical frame selection using randomized logic to prove non-contiguous capability.

## 🚀 Algorithms Implemented

The simulator allows users to switch between standard allocation strategies on the fly:

1.  **First Fit:** Allocates the first hole that is big enough. Fastest but causes fragmentation.
2.  **Best Fit:** Allocates the smallest hole that is big enough. Minimizes immediate waste but creates tiny, unusable holes.
3.  **Worst Fit:** Allocates the largest available hole. Prevents tiny holes but consumes large contiguous blocks quickly.

## 📸 Screenshots

### Contiguous Allocation & Swapping
*Visualizes variable partitioning, showing processes in RAM (Green) and Swapped to Disk (Blue).*
![Contiguous Memory Demo](https://via.placeholder.com/800x400?text=Insert+Screenshot+of+Tab+1+Here)

### Paging & Page Table Inspector
*Visualizes scattered frames and the inspector tool showing logical-to-physical mapping.*
![Paging Demo](https://via.placeholder.com/800x400?text=Insert+Screenshot+of+Tab+2+Here)

## 🛠 Getting Started

### Prerequisites
* Python 3.x
* CustomTkinter (`pip install customtkinter`)

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/os-memory-simulator.git](https://github.com/yourusername/os-memory-simulator.git)
    ```
2.  Navigate to the directory:
    ```bash
    cd os-memory-simulator
    ```
3.  Run the application:
    ```bash
    python gui.py
    ```

## 📂 Project Structure

```text
├── gui.py                # Main Entry Point. Handles UI layout, user inputs, and drawing logic.
├── memory_managers.py    # Backend Logic. Contains the classes for ContiguousManager and PagingManager.
└── README.md             # Documentation.
