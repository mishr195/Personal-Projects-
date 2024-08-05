#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "sudoku.h"

int main(int argc, char **argv) {
    // Check for correct number of command-line arguments
    if (argc != 3) {
        printf("Usage: %s <input_file> <output_file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // Open the input file
    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL) {
        printf("Error: Could not open input file\n");
        return EXIT_FAILURE;
    }

    // Read the Sudoku puzzle from the input file
    Sudoku puzzle;
    if (!readSudoku(input_file, &puzzle)) {
        printf("Error: Invalid input file format\n");
        fclose(input_file);
        return EXIT_FAILURE;
    }

    // Close the input file
    fclose(input_file);

    // Solve the Sudoku puzzle
    if (!solveSudoku(&puzzle)) {
        printf("Error: Failed to solve Sudoku puzzle\n");
        return EXIT_FAILURE;
    }

    printSudoku(&puzzle);

    // Open the output file
    FILE *output_file = fopen(argv[2], "w");
    if (output_file == NULL) {
        printf("Error: Could not open output file\n");
        return EXIT_FAILURE;
    }

    printSudokuToFile(&puzzle, output_file);

    // Close the output file
    fclose(output_file);

    return EXIT_SUCCESS;
}
