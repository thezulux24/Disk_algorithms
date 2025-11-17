#ifndef DISK_SCHEDULER_H
#define DISK_SCHEDULER_H

#include <vector>
#include <string>

// Clase base para algoritmos de planificación
class DiskScheduler {
public:
    virtual ~DiskScheduler() {}
    
    // Calcula el movimiento total de la cabeza
    virtual int schedule(const std::vector<int>& requests, int initialHead) = 0;
    
    virtual const char* getName() = 0;
    
    // Para exportar datos de visualización
    std::vector<int> movements;  // Guarda cada posición visitada
};

// FCFS - First Come First Served
class FCFS : public DiskScheduler {
public:
    int schedule(const std::vector<int>& requests, int initialHead);
    const char* getName() { return "FCFS"; }
};

// SCAN - Algoritmo del ascensor
class SCAN : public DiskScheduler {
private:
    int diskSize;
public:
    SCAN(int size) : diskSize(size) {}
    int schedule(const std::vector<int>& requests, int initialHead);
    const char* getName() { return "SCAN"; }
};

// C-SCAN - Circular SCAN
class CSCAN : public DiskScheduler {
private:
    int diskSize;
public:
    CSCAN(int size) : diskSize(size) {}
    int schedule(const std::vector<int>& requests, int initialHead);
    const char* getName() { return "C-SCAN"; }
};

// Funciones de exportación para visualización
void exportToCSV(const std::string& algorithm, const std::vector<int>& positions);

#endif
