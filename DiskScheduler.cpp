#include "DiskScheduler.h"
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>

// FCFS - Atiende las solicitudes en orden de llegada
int FCFS::schedule(const std::vector<int>& requests, int initialHead) {
    int total = 0;
    int head = initialHead;
    movements.clear();
    movements.push_back(head);
    
    for (int request : requests) {
        total += abs(request - head);
        head = request;
        movements.push_back(head);
    }
    
    return total;
}

// SCAN - Se mueve hacia arriba y luego hacia abajo
int SCAN::schedule(const std::vector<int>& requests, int initialHead) {
    std::vector<int> left;   // Solicitudes a la izquierda
    std::vector<int> right;  // Solicitudes a la derecha
    movements.clear();
    movements.push_back(initialHead);
    
    // Separar solicitudes
    for (int req : requests) {
        if (req < initialHead)
            left.push_back(req);
        else
            right.push_back(req);
    }
    
    // Ordenar
    std::sort(left.begin(), left.end());
    std::sort(right.begin(), right.end());
    
    int total = 0;
    int head = initialHead;
    
    // Ir hacia la derecha primero
    for (int req : right) {
        total += abs(req - head);
        head = req;
        movements.push_back(head);
    }
    
    // Llegar al final del disco
    if (!right.empty() && head != diskSize - 1) {
        total += abs((diskSize - 1) - head);
        head = diskSize - 1;
        movements.push_back(head);
    }
    
    // Ir hacia la izquierda
    for (int i = left.size() - 1; i >= 0; i--) {
        total += abs(left[i] - head);
        head = left[i];
        movements.push_back(head);
    }
    
    return total;
}

// C-SCAN - Se mueve en una sola dirección de forma circular
int CSCAN::schedule(const std::vector<int>& requests, int initialHead) {
    std::vector<int> left;
    std::vector<int> right;
    movements.clear();
    movements.push_back(initialHead);
    
    // Separar solicitudes
    for (int req : requests) {
        if (req < initialHead)
            left.push_back(req);
        else
            right.push_back(req);
    }
    
    // Ordenar
    std::sort(left.begin(), left.end());
    std::sort(right.begin(), right.end());
    
    int total = 0;
    int head = initialHead;
    
    // Ir hacia la derecha
    for (int req : right) {
        total += abs(req - head);
        head = req;
        movements.push_back(head);
    }
    
    // Llegar al final
    if (!right.empty() && head != diskSize - 1) {
        total += abs((diskSize - 1) - head);
        head = diskSize - 1;
        movements.push_back(head);
    }
    
    // Saltar al inicio (movimiento circular)
    if (head != 0) {
        total += abs(head - 0);
        head = 0;
        movements.push_back(head);
    }
    
    // Atender las solicitudes de la izquierda
    for (int req : left) {
        total += abs(req - head);
        head = req;
        movements.push_back(head);
    }
    
    return total;
}

// Función de exportación para visualización
void exportToCSV(const std::string& algorithm, const std::vector<int>& positions) {
    // Crear carpeta resultados/datos_csv si no existe
#ifdef _WIN32
    system("if not exist resultados\\datos_csv mkdir resultados\\datos_csv");
#else
    system("mkdir -p resultados/datos_csv");
#endif
    
    std::string filename = "resultados/datos_csv/movimientos_" + algorithm + ".csv";
    std::ofstream file(filename);
    
    if (!file) {
        std::cerr << "Error al crear " << filename << "\n";
        return;
    }
    
    file << "paso,desde,hasta,distancia\n";
    for (size_t i = 1; i < positions.size(); i++) {
        int from = positions[i - 1];
        int to = positions[i];
        int distance = abs(to - from);
        file << (i - 1) << "," << from << "," << to << "," << distance << "\n";
    }
    
    file.close();
}
