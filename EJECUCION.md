# Ejecución del Simulador de Planificación de Disco

## Compilación

```powershell
# Compilar archivos objeto
g++ -std=c++14 -O2 -c DiskScheduler.cpp -o DiskScheduler.o
g++ -std=c++14 -O2 -c main.cpp -o main.o

# Enlazar y crear ejecutable
g++ -std=c++14 -O2 DiskScheduler.o main.o -o disk_scheduler.exe
```

✅ **Compilación exitosa**

---

## Ejecución 1: Posición Inicial 2500 (Centro del Disco)

```powershell
.\disk_scheduler.exe 2500
```

## Ejecución 2: graficos

```powershell
python visualizar.py
```