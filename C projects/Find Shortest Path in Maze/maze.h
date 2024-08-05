#ifndef MAZE_H
#define MAZE_H

#define MAX_ROWS 100
#define MAX_COLS 100
#define INF (MAX_ROWS * MAX_COLS + 1)

typedef struct {
    int row;
    int col;
} Point;

typedef struct {
    int rows;
    int cols;
    char cells[MAX_ROWS][MAX_COLS];
    int distances[MAX_ROWS][MAX_COLS];
} Maze;

// Function prototypes
Maze readMazeFromFile(const char *filename);
void findShortestPaths(Maze *maze);
void printDistances(const Maze *maze);

#endif /* MAZE_H */
