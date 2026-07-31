"""
Pipeline Flow & Pressure Simulator (CLI Edition)
==================================================
A Python pipeline analysis tool that calculates 14 fluid-flow properties
(pressure loss, Reynolds number, pump power requirements, and more) for a
single pipe design, and lets you stack up multiple pipeline design
scenarios side-by-side with automated Matplotlib comparison graphs.

No GUI toolkit required -- runs entirely in the terminal. Graphs are
generated with Matplotlib, saved to PNG files, and popped up on screen
(if a display is available).

Run with:  python pipeline_simulator.py

Requires: numpy, matplotlib
"""

import sys

from analysis import run_single_analysis
from comparison import run_comparison


BANNER = r"""
============================================================
   PIPELINE FLOW & PRESSURE SIMULATOR
   14 fluid-flow properties + automated Matplotlib graphs
============================================================
"""


def main():
    print(BANNER)
    while True:
        print("\n=== MAIN MENU ===")
        print("1) Single Pipe Analysis")
        print("2) Scenario Comparison")
        print("3) Exit")
        choice = input("Select an option [1-3]: ").strip()

        if choice == "1":
            run_single_analysis()
        elif choice == "2":
            run_comparison()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        sys.exit(0)
9
