#include "DiskScheduler.h"
#include <iostream>
#include <vector>
#include <random>
#include <ctime>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    // Validar argumentos
    if (argc < 2) {
        cout << "Uso: " << argv[0] << " <posicion_inicial>\n";
        return 1;
    }
    
    int initialHead = atoi(argv[1]);
    const int DISK_SIZE = 5000;
    const int NUM_REQUESTS = 1000;
    
    if (initialHead < 0 || initialHead >= DISK_SIZE) {
        cout << "Error: posicion inicial debe estar entre 0 y 4999\n";
        return 1;
    }
    
    // Generar solicitudes aleatorias
    srand(time(0));
    vector<int> requests(NUM_REQUESTS);
    for (int i = 0; i < NUM_REQUESTS; i++) {
        requests[i] = rand() % DISK_SIZE;
    }
    
    // Mostrar información
    cout << "\n====================================\n";
    cout << "  SIMULADOR DE DISCO\n";
    cout << "====================================\n";
    cout << "Cilindros: 0 - " << DISK_SIZE - 1 << "\n";
    cout << "Posicion inicial: " << initialHead << "\n";
    cout << "Solicitudes: " << NUM_REQUESTS << "\n\n";
    
    // Crear algoritmos
    FCFS fcfs;
    SCAN scan(DISK_SIZE);
    CSCAN cscan(DISK_SIZE);
    
    // Ejecutar algoritmos
    int fcfsMovement = fcfs.schedule(requests, initialHead);
    int scanMovement = scan.schedule(requests, initialHead);
    int cscanMovement = cscan.schedule(requests, initialHead);
    
    // Mostrar resultados
    cout << "RESULTADOS:\n";
    cout << "------------------------------------\n";
    cout << "FCFS   : " << fcfsMovement << " cilindros\n";
    cout << "SCAN   : " << scanMovement << " cilindros\n";
    cout << "C-SCAN : " << cscanMovement << " cilindros\n";
    cout << "====================================\n\n";
    
    // Crear carpeta resultados/datos_csv si no existe
#ifdef _WIN32
    system("if not exist resultados\\datos_csv mkdir resultados\\datos_csv");
#else
    system("mkdir -p resultados/datos_csv");
#endif
    
    // Exportar datos para visualización
    exportToCSV("FCFS", fcfs.movements);
    exportToCSV("SCAN", scan.movements);
    exportToCSV("C-SCAN", cscan.movements);
    
    // Crear archivo resumen.csv
    ofstream summary("resultados/datos_csv/resumen.csv");
    if (summary) {
        summary << "algoritmo,movimiento_total\n";
        summary << "FCFS," << fcfsMovement << "\n";
        summary << "SCAN," << scanMovement << "\n";
        summary << "C-SCAN," << cscanMovement << "\n";
        summary.close();

        cout << "Ejecuta 'python visualizar.py' para ver graficas.\n\n";
    }
    
    return 0;
}
