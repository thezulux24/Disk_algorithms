import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuración de directorios de salida
DIR_RESULTADOS = "resultados"
DIR_CSV = os.path.join(DIR_RESULTADOS, "datos_csv")
DIR_GRAFICAS = os.path.join(DIR_RESULTADOS, "graficas")

os.makedirs(DIR_CSV, exist_ok=True)
os.makedirs(DIR_GRAFICAS, exist_ok=True)

def cargar_datos():
    """Carga los datos de los archivos CSV generados por el programa C++"""
    ruta_resumen = os.path.join(DIR_CSV, 'resumen.csv')
    resumen = pd.read_csv(ruta_resumen)
    
    movimientos = {}
    for algoritmo in resumen['algoritmo']:
        nombre_archivo = os.path.join(DIR_CSV, f'movimientos_{algoritmo}.csv')
        if os.path.exists(nombre_archivo):
            movimientos[algoritmo] = pd.read_csv(nombre_archivo)
    
    return resumen, movimientos

def graficar_movimiento_cabeza(movimientos):
    """Genera gráfica del movimiento de la cabeza a lo largo del tiempo"""
    figura, ejes = plt.subplots(3, 1, figsize=(14, 10))
    figura.suptitle('Movimiento de la Cabeza del Disco a lo Largo del Tiempo', 
                 fontsize=16, fontweight='bold')
    
    algoritmos = ['FCFS', 'SCAN', 'C-SCAN']
    colores = ['#e74c3c', '#3498db', '#2ecc71']
    
    for indice, (algoritmo, color) in enumerate(zip(algoritmos, colores)):
        if algoritmo not in movimientos:
            continue
            
        datos = movimientos[algoritmo]
  
        datos = datos.rename(columns={'desde': 'origen', 'hasta': 'destino', 'distancia': 'distancia', 'paso': 'paso'})
        eje = ejes[indice]
        
        # Crear secuencia de posiciones
        posiciones = [datos['origen'].iloc[0]] + datos['destino'].tolist()
        pasos = list(range(len(posiciones)))
        
        eje.plot(pasos, posiciones, color=color, linewidth=1.5, alpha=0.7)
        eje.scatter(pasos, posiciones, s=1, color=color, alpha=0.3)
        
        eje.set_ylabel('Posición del Cilindro', fontsize=11)
        eje.set_title(f'{algoritmo} - Trayectoria de la Cabeza', 
                    fontsize=12, fontweight='bold')
        eje.grid(True, alpha=0.3, linestyle='--')
        eje.set_xlim(0, len(posiciones))
        eje.set_ylim(0, 5000)
        
        if indice == 2:
            eje.set_xlabel('Paso/Solicitud', fontsize=11)
    
    plt.tight_layout()
    ruta_salida = os.path.join(DIR_GRAFICAS, 'movimiento_cabeza_tiempo.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"Grafica guardada: {ruta_salida}")
    plt.close()

def graficar_comparacion_rendimiento(resumen):
    """Genera gráfica de comparación de rendimiento entre algoritmos"""
    figura, (eje1, eje2) = plt.subplots(1, 2, figsize=(14, 6))
    figura.suptitle('Comparación de Rendimiento de Algoritmos de Planificación', 
                 fontsize=16, fontweight='bold')
    
    algoritmos = resumen['algoritmo']
    movimientos = resumen['movimiento_total']
    colores = ['#e74c3c', '#3498db', '#2ecc71']
    
    # Gráfica de barras
    barras = eje1.bar(algoritmos, movimientos, color=colores, alpha=0.8, edgecolor='black', linewidth=1.5)
    eje1.set_ylabel('Movimiento Total (cilindros)', fontsize=12, fontweight='bold')
    eje1.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    eje1.set_title('Movimiento Total por Algoritmo', fontsize=13, fontweight='bold')
    eje1.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Agregar valores en las barras
    for barra in barras:
        altura = barra.get_height()
        eje1.text(barra.get_x() + barra.get_width()/2., altura,
                f'{int(altura):,}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Calcular eficiencia relativa (menor es mejor)
    movimiento_minimo = movimientos.min()
    eficiencia = (movimientos / movimiento_minimo) * 100
    
    # Gráfica de eficiencia
    barras2 = eje2.bar(algoritmos, eficiencia, color=colores, alpha=0.8, edgecolor='black', linewidth=1.5)
    eje2.set_ylabel('Eficiencia Relativa (%)', fontsize=12, fontweight='bold')
    eje2.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    eje2.set_title('Eficiencia Relativa (100% = Mejor)', fontsize=13, fontweight='bold')
    eje2.grid(True, alpha=0.3, axis='y', linestyle='--')
    eje2.axhline(y=100, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Óptimo')
    eje2.legend()
    
    # Agregar valores en las barras
    for barra in barras2:
        altura = barra.get_height()
        eje2.text(barra.get_x() + barra.get_width()/2., altura,
                f'{altura:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    ruta_salida = os.path.join(DIR_GRAFICAS, 'comparacion_rendimiento.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"Grafica guardada: {ruta_salida}")
    plt.close()

def graficar_distribucion_distancias(movimientos):
    """Genera gráfica de distribución de distancias de búsqueda"""
    figura, ejes = plt.subplots(1, 3, figsize=(16, 5))
    figura.suptitle('Distribución de Distancias de Búsqueda', 
                 fontsize=16, fontweight='bold')
    
    algoritmos = ['FCFS', 'SCAN', 'C-SCAN']
    colores = ['#e74c3c', '#3498db', '#2ecc71']
    
    for indice, (algoritmo, color) in enumerate(zip(algoritmos, colores)):
        if algoritmo not in movimientos:
            continue
            
        datos = movimientos[algoritmo]
        distancias = datos['distancia']
        
        eje = ejes[indice]
        eje.hist(distancias, bins=50, color=color, alpha=0.7, edgecolor='black')
        eje.set_xlabel('Distancia (cilindros)', fontsize=11)
        eje.set_ylabel('Frecuencia', fontsize=11)
        eje.set_title(f'{algoritmo}', fontsize=12, fontweight='bold')
        eje.grid(True, alpha=0.3, linestyle='--')
        
        # Agregar estadísticas
        media = distancias.mean()
        mediana = distancias.median()
        eje.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.1f}')
        eje.axvline(mediana, color='blue', linestyle='--', linewidth=2, label=f'Mediana: {mediana:.1f}')
        eje.legend()
    
    plt.tight_layout()
    ruta_salida = os.path.join(DIR_GRAFICAS, 'distribucion_distancias.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"Grafica guardada: {ruta_salida}")
    plt.close()

def graficar_movimiento_acumulado(movimientos):
    """Genera gráfica del movimiento acumulado de la cabeza"""
    figura, eje = plt.subplots(figsize=(14, 8))
    figura.suptitle('Movimiento Acumulado de la Cabeza del Disco', 
                 fontsize=16, fontweight='bold')
    
    algoritmos = ['FCFS', 'SCAN', 'C-SCAN']
    colores = ['#e74c3c', '#3498db', '#2ecc71']
    
    for algoritmo, color in zip(algoritmos, colores):
        if algoritmo not in movimientos:
            continue
            
        datos = movimientos[algoritmo]
        distancias = datos['distancia']
        movimiento_acum = distancias.cumsum()
        
        eje.plot(range(len(movimiento_acum)), movimiento_acum, 
                color=color, linewidth=2, label=algoritmo, alpha=0.8)
    
    eje.set_xlabel('Paso/Solicitud', fontsize=12, fontweight='bold')
    eje.set_ylabel('Movimiento Acumulado (cilindros)', fontsize=12, fontweight='bold')
    eje.set_title('Comparación del Movimiento Acumulado', fontsize=13, fontweight='bold')
    eje.grid(True, alpha=0.3, linestyle='--')
    eje.legend(fontsize=11)
    
    plt.tight_layout()
    ruta_salida = os.path.join(DIR_GRAFICAS, 'movimiento_acumulado.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"Grafica guardada: {ruta_salida}")
    plt.close()

def graficar_comparacion_tiempo_busqueda(resumen):
    """Genera gráfica de comparación del tiempo de búsqueda promedio"""
    figura, eje = plt.subplots(figsize=(10, 6))
    
    algoritmos = resumen['algoritmo']
    movimientos = resumen['movimiento_total']
    
    # Calcular tiempo promedio por solicitud (1000 solicitudes)
    tiempo_promedio = movimientos / 1000
    
    colores = ['#e74c3c', '#3498db', '#2ecc71']
    barras = eje.bar(algoritmos, tiempo_promedio, color=colores, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    eje.set_ylabel('Distancia Promedio por Solicitud (cilindros)', fontsize=12, fontweight='bold')
    eje.set_xlabel('Algoritmo', fontsize=12, fontweight='bold')
    eje.set_title('Comparación de Distancia Promedio de Búsqueda', fontsize=14, fontweight='bold')
    eje.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # Agregar valores en las barras
    for barra in barras:
        altura = barra.get_height()
        eje.text(barra.get_x() + barra.get_width()/2., altura,
                f'{altura:.2f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    ruta_salida = os.path.join(DIR_GRAFICAS, 'comparacion_tiempo_busqueda.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"Grafica guardada: {ruta_salida}")
    plt.close()

def generar_reporte(resumen, movimientos):
    """Genera un reporte estadístico en formato texto"""
    ruta_reporte = os.path.join(DIR_RESULTADOS, 'reporte.txt')
    
    with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
        archivo.write("=" * 80 + "\n")
        archivo.write("REPORTE DE ANÁLISIS DE ALGORITMOS DE PLANIFICACIÓN DE DISCO\n")
        archivo.write("=" * 80 + "\n\n")
        
        archivo.write("RESUMEN GENERAL\n")
        archivo.write("-" * 80 + "\n")
        archivo.write(f"Número de cilindros: 5,000\n")
        archivo.write(f"Número de solicitudes: 1,000\n\n")
        
        for _, fila in resumen.iterrows():
            algoritmo = fila['algoritmo']
            movimiento_total = fila['movimiento_total']
            
            archivo.write(f"\nALGORITMO: {algoritmo}\n")
            archivo.write("-" * 80 + "\n")
            archivo.write(f"Movimiento total de la cabeza: {movimiento_total:,} cilindros\n")
            
            if algoritmo in movimientos:
                datos = movimientos[algoritmo]
                distancias = datos['distancia']
                
                archivo.write(f"Distancia promedio por solicitud: {distancias.mean():.2f} cilindros\n")
                archivo.write(f"Distancia mínima: {distancias.min()} cilindros\n")
                archivo.write(f"Distancia máxima: {distancias.max()} cilindros\n")
                archivo.write(f"Distancia mediana: {distancias.median():.2f} cilindros\n")
                archivo.write(f"Desviación estándar: {distancias.std():.2f} cilindros\n")
        
        archivo.write("\n" + "=" * 80 + "\n")
        archivo.write("ANÁLISIS COMPARATIVO\n")
        archivo.write("=" * 80 + "\n\n")
        
        movimiento_minimo = resumen['movimiento_total'].min()
        mejor_algoritmo = resumen.loc[resumen['movimiento_total'].idxmin(), 'algoritmo']
        
        archivo.write(f"Mejor algoritmo (menor movimiento): {mejor_algoritmo}\n")
        archivo.write(f"Movimiento mínimo: {movimiento_minimo:,} cilindros\n\n")
        
        archivo.write("Eficiencia relativa (100% = mejor):\n")
        for _, fila in resumen.iterrows():
            algoritmo = fila['algoritmo']
            movimiento = fila['movimiento_total']
            eficiencia = (movimiento / movimiento_minimo) * 100
            archivo.write(f"  {algoritmo}: {eficiencia:.2f}%\n")
        
        archivo.write("\n" + "=" * 80 + "\n")
    
    print(f"Reporte generado: {ruta_reporte}")

def main():
    """Función principal que genera todas las visualizaciones"""
    print("\n" + "="*80)
    print("GENERADOR DE VISUALIZACIONES DE PLANIFICACIÓN DE DISCO")
    print("="*80 + "\n")
    
    try:
        # Cargar datos
        print("Cargando datos desde archivos CSV...")
        resumen, movimientos = cargar_datos()
        print(f"Datos cargados exitosamente: {len(resumen)} algoritmos\n")
        
        # Generar gráficas
        print("Generando visualizaciones...")
        print("-" * 80)
        
        graficar_movimiento_cabeza(movimientos)
        graficar_comparacion_rendimiento(resumen)
        graficar_distribucion_distancias(movimientos)
        graficar_movimiento_acumulado(movimientos)
        graficar_comparacion_tiempo_busqueda(resumen)
        
        # Generar reporte
        print("-" * 80)
        generar_reporte(resumen, movimientos)
        
        print("\n" + "="*80)
        print("PROCESO COMPLETADO EXITOSAMENTE")
        print("="*80)
        print(f"\nArchivos generados:")
        print(f"  - Gráficas en: {DIR_GRAFICAS}/")
        print(f"  - Reporte en: {os.path.join(DIR_RESULTADOS, 'reporte.txt')}")
        print()
        
    except FileNotFoundError as e:
        print(f"\nError: No se encontraron los archivos CSV necesarios.")
        print(f"Asegúrese de ejecutar primero el programa C++ para generar los datos.")
        print(f"Detalles: {e}\n")
    except Exception as e:
        print(f"\nError inesperado: {e}\n")


main()
