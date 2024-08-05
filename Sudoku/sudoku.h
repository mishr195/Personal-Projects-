#ifndef SUDOKU_H
#define SUDOKU_H

#include <stdio.h>
#include <stdbool.h>

#define SIZE 9
#define MAX_SIZE 20
#define EMPTY 0

typedef struct {
    int grid[SIZE][SIZE];
} Sudoku;

bool readSudoku(FILE *input_file, Sudoku *puzzle);
void printSudoku(const Sudoku *puzzle);
bool isValid(const Sudoku *puzzle, int row, int col, int num);
bool solveSudoku(Sudoku *puzzle);
bool findEmptyCell(const Sudoku *puzzle, int *row, int *col);
void printSudokuToFile(const Sudoku *puzzle, FILE *output_file);

#endif /* SUDOKU_H */
