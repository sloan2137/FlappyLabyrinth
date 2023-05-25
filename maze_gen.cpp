#include <bits/stdc++.h>

struct Cell {
    int x, y;
    Cell(int x, int y) {
        this->x = x;
        this->y = y;
    }

    void add_neighbours(std::vector<Cell> &neighbours, int n) {
        if (x > 0) {
            neighbours.push_back(Cell(x - 1, y));
        }
        if (x < n - 1) {
            neighbours.push_back(Cell(x + 1, y));
        }
        if (y > 0) {
            neighbours.push_back(Cell(x, y - 1));
        }
        if (y < n - 1) {
            neighbours.push_back(Cell(x, y + 1));
        }
    }
};

typedef std::vector<std::vector<bool>> Grid;

void backtrack(Cell cell, std::ofstream &stream, Grid &visited, int n) {
    visited[cell.x][cell.y] = true;
    std::vector<Cell> neighbours;
    cell.add_neighbours(neighbours, n);
    std::random_shuffle(neighbours.begin(), neighbours.end());
    for (Cell neighbour : neighbours) {
        if (!visited[neighbour.x][neighbour.y]) {
            stream << cell.x << "," << cell.y << " " << neighbour.x << ","
                   << neighbour.y << std::endl;
            backtrack(neighbour, stream, visited, n);
        }
    }
}

int main(int argc, char *argv[]) {
    std::string difficulty = argv[1];
    int n = std::stoi(difficulty);

    std::ofstream file;
    file.open("maze.maze");

    std::srand(std::time(nullptr));
    Cell start(0, 0);
    Cell end(n - 1, n - 1);
    if (rand() & 1) {
        start.x = rand() % n;
        end.y = rand() % n;
    } else {
        start.y = rand() % n;
        end.x = rand() % n;
    }

    file << n << std::endl;
    file << start.x << "," << start.y << std::endl;
    file << end.x << "," << end.y << std::endl;

    std::vector<std::vector<bool>> visited(n, std::vector<bool>(n, false));

    backtrack(start, file, visited, n);
}
