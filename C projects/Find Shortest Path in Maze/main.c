#include <stdio.h>
#include "maze.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    Maze maze = readMazeFromFile(argv[1]);
    findShortestPaths(&maze);
    printDistances(&maze);

    return 0;
}
