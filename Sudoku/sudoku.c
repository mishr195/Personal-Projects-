#include "sudoku.h"
#include <string.h> 

// Function to read Sudoku puzzle from file
bool readSudoku(FILE *input_file, Sudoku *puzzle) {
    char buffer[MAX_SIZE];
    int row = 0;

    while (fgets(buffer, MAX_SIZE, input_file) != NULL) {
        if (strlen(buffer) < SIZE) {
            return false;
        }
        for (int col = 0; col < SIZE; col++) {
            if (buffer[col] == '-') {
                puzzle->grid[row][col] = EMPTY;
            } else if (buffer[col] >= '1' && buffer[col] <= '9') {
                puzzle->grid[row][col] = buffer[col] - '0';
            } else {
                return false;
            }
        }
        row++;
    }

    return true;
}

// Function to print Sudoku puzzle
void printSudoku(const Sudoku *puzzle) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d", puzzle->grid[i][j]);
        }
        printf("\n");
    }
}

// Function to check if a number can be placed in a particular cell
bool isValid(const Sudoku *puzzle, int row, int col, int num) {
    // Check row and column
    for (int i = 0; i < SIZE; i++) {
        if (puzzle->grid[row][i] == num || puzzle->grid[i][col] == num) {
            return false;
        }
    }

    // Check 3x3 subgrid
    int startRow = row - row % 3;
    int startCol = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (puzzle->grid[i + startRow][j + startCol] == num) {
                return false;
            }
        }
    }

    return true;
}

// Function to solve Sudoku puzzle using backtracking
bool solveSudoku(Sudoku *puzzle) {
    int row, col;

    // Find an empty cell
    if (!findEmptyCell(puzzle, &row, &col)) {
        return true; // Puzzle is solved
    }

    // Try placing numbers from 1 to 9
    for (int num = 1; num <= SIZE; num++) {
        if (isValid(puzzle, row, col, num)) {
            puzzle->grid[row][col] = num; // Place the number
            if (solveSudoku(puzzle)) {
                return true; // Puzzle solved recursively
            }
            puzzle->grid[row][col] = EMPTY; // Backtrack
        }
    }

    return false; // No solution found
}

// Function to find an empty cell
bool findEmptyCell(const Sudoku *puzzle, int *row, int *col) {
    for (*row = 0; *row < SIZE; (*row)++) {
        for (*col = 0; *col < SIZE; (*col)++) {
            if (puzzle->grid[*row][*col] == EMPTY) {
                return true; // Empty cell found
            }
        }
    }
    return false; // No empty cell found
}

void printSudokuToFile(const Sudoku *puzzle, FILE *output_file) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            fprintf(output_file, "%d", puzzle->grid[i][j]);
        }
        fprintf(output_file, "\n");
    }
}
