import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def find_empty(self):
        """Find an empty cell in the Sudoku grid. Returns a tuple (row, col) or None."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos):
        """Check if a number can be placed at the given position."""
        # Check row
        for i in range(9):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(9):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        """Solve the Sudoku puzzle using backtracking. Returns True if solved, False otherwise."""
        find = self.find_empty()
        if not find:
            return True
        row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.grid[row][col] = i

                if self.solve():
                    return True

                self.grid[row][col] = 0

        return False

class SudokuGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Sudoku Solver")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j] = tk.Entry(self.window, width=2, font=('Arial', 18), justify='center', borderwidth=2)
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)

        solve_button = tk.Button(self.window, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=9, column=0, columnspan=4, pady=10)

        clear_button = tk.Button(self.window, text="Clear", command=self.clear_puzzle)
        clear_button.grid(row=9, column=5, columnspan=4, pady=10)

    def read_grid(self):
        """Reads the grid values from the GUI."""
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                self.grid[i][j] = int(value) if value.isdigit() else 0

    def update_grid(self):
        """Updates the GUI with solved grid values."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.grid[i][j]))

    def solve_puzzle(self):
        self.read_grid()
        solver = SudokuSolver(self.grid)
        if solver.solve():
            self.update_grid()
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists for this puzzle.")

    def clear_puzzle(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.grid[i][j] = 0

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

# Run the Sudoku solver GUI application
main()
