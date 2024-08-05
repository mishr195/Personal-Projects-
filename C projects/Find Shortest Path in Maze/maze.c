#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "maze.h"

// Function to read the maze from file and initialize the distances array
Maze readMazeFromFile(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening file: %s\n", filename);
        exit(1);
    }

    Maze maze;
    int row = 0;
    while (fgets(maze.cells[row], MAX_COLS + 2, file) != NULL) {
        // Remove newline character if present
        int len = strlen(maze.cells[row]);
        if (len > 0 && maze.cells[row][len - 1] == '\n') {
            maze.cells[row][len - 1] = '\0'; // Remove newline
            len--; // Adjust column count
        }

        // Initialize distances for each cell
        for (int col = 0; col < len; col++) {
            if (maze.cells[row][col] == 'b') {
                maze.distances[row][col] = -1; // Wall
            } else if (maze.cells[row][col] == 's') {
                maze.distances[row][col] = 0; // Starting point
            } else {
                maze.distances[row][col] = INF; // Unvisited cell
            }
        }

        row++;
    }
    maze.rows = row;
    maze.cols = strlen(maze.cells[0]); // Assuming all rows have the same length

    fclose(file);
    return maze;
}

// Function to find shortest paths from the starting point using BFS
void findShortestPaths(Maze *maze) {
    Point queue[MAX_ROWS * MAX_COLS];
    int front = 0, rear = 0;

    // Add starting point to the queue
    for (int i = 0; i < maze->rows; i++) {
        for (int j = 0; j < maze->cols; j++) {
            if (maze->cells[i][j] == 's') {
                queue[rear++] = (Point){i, j};
            }
        }
    }

    // Perform BFS traversal
    while (front < rear) {
        Point current = queue[front++];
        int row = current.row;
        int col = current.col;
        int distance = maze->distances[row][col] + 1;

        // Explore neighboring cells
        if (row > 0 && maze->cells[row - 1][col] != 'b' && distance < maze->distances[row - 1][col]) {
            maze->distances[row - 1][col] = distance;
            queue[rear++] = (Point){row - 1, col};
        }
        if (row < maze->rows - 1 && maze->cells[row + 1][col] != 'b' && distance < maze->distances[row + 1][col]) {
            maze->distances[row + 1][col] = distance;
            queue[rear++] = (Point){row + 1, col};
        }
        if (col > 0 && maze->cells[row][col - 1] != 'b' && distance < maze->distances[row][col - 1]) {
            maze->distances[row][col - 1] = distance;
            queue[rear++] = (Point){row, col - 1};
        }
        if (col < maze->cols - 1 && maze->cells[row][col + 1] != 'b' && distance < maze->distances[row][col + 1]) {
            maze->distances[row][col + 1] = distance;
            queue[rear++] = (Point){row, col + 1};
        }
    }
    // Mark unreachable cells
    for (int i = 0; i < maze->rows; i++) {
        for (int j = 0; j < maze->cols; j++) {
            if (maze->distances[i][j] == INF) {
                maze->distances[i][j] = maze->rows * maze->cols + 1;
        }
    }
}
    
}



// Function to print distances of each cell from the starting point
void printDistances(const Maze *maze) {
    for (int i = 0; i < maze->rows; i++) {
        for (int j = 0; j < maze->cols; j++) {
            printf("%4d ", maze->distances[i][j]);
        }
        printf("\n");
    }
}
