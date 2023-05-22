#include <bits/stdc++.h>

int main(int argc, char *argv[]) {
    std::string difficulty = argv[1];
    int n = std::stoi(difficulty);

    std::ofstream fout("maze.maze");

    fout << n << " " << n << "\n";
    
    std::srand(std::time(nullptr));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            fout << std::rand() % 2;
        }
        fout << "\n";
    }

    return 0;
}
