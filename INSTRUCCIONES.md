# Procesador de Datos Experimentales - Guía de Instalación y Uso

## Descripción
Aplicación GUI profesional para el procesamiento de datos experimentales con capacidad de ajuste de parámetros, similar al software ZEUS mencionado. Permite:

- ✅ Cargar archivos de datos (CSV)
- ✅ Ajustar parámetros del experimento (número de lote, rango de índices)
- ✅ Procesar datos en tiempo real con barra de progreso
- ✅ Visualizar datos crudos y procesados
- ✅ Ver estadísticas detalladas
- ✅ Exportar resultados (CSV, XLSX)

---

## Requisitos del Sistema

- **Python 3.8+** (recomendado 3.10 o superior)
- **Sistema operativo**: Windows, macOS, Linux

---

## Instalación

### Paso 1: Instalar dependencias

```bash
pip install PyQt6 pandas numpy openpyxl
```

**Detalle de dependencias:**
- `PyQt6`: Framework GUI moderno
- `pandas`: Procesamiento de datos
- `numpy`: Cálculos numéricos
- `openpyxl`: Exportar a Excel

### Paso 2: Descargar la aplicación

Guarde el archivo `data_processor_gui.py` en una carpeta de su preferencia.

---

## Uso de la Aplicación

### Interfaz General

La aplicación está dividida en dos paneles:

**Panel Izquierdo - Parámetros:**
- Carga de archivos
- Configuración de parámetros del experimento
- Opciones de procesamiento
- Botones de control

**Panel Derecho - Resultados:**
- 3 pestañas: Datos Crudos | Datos Procesados | Estadísticas

### Flujo de trabajo típico

#### 1. Cargar archivo de datos
```
a) Click en "Cargar..." junto a "Archivo de datos"
b) Seleccionar archivo CSV con los datos del experimento
c) Los datos aparecerán en la pestaña "Datos Crudos"
```

#### 2. Ajustar parámetros
```
Parámetro                    | Descripción
-----------------------------|-----------------------------------------------
Número de lote               | Filtrar por lote específico (0 = todos)
Índice mínimo               | Valor mínimo de T1_Index (0 = sin límite)
Índice máximo               | Valor máximo de T1_Index (0 = sin límite)
Eliminar filas vacías       | Remover registros incompletos
Normalizar valores numéricos | Aplicar normalización (0-1)
```

#### 3. Procesar datos
```
Click en "Procesar Datos"
- Se mostrará una barra de progreso
- Los datos filtrados aparecerán en "Datos Procesados"
- Las estadísticas se calcularán automáticamente
```

#### 4. Exportar resultados
```
Click en "Exportar Resultado"
- Seleccionar formato: CSV o XLSX
- Elegir ubicación y nombre del archivo
- Los datos procesados se guardarán con el formato seleccionado
```

---

## Ejemplos de Uso

### Ejemplo 1: Procesar un lote específico

```
1. Cargar archivo: Reporte_de_Datos.csv
2. Número de lote: 1
3. Dejar índices en 0 (sin filtro)
4. Click en "Procesar Datos"
5. Exportar resultado como "Lote_1_procesado.csv"
```

### Ejemplo 2: Extraer rango de datos

```
1. Cargar archivo: Reporte_de_Datos.csv
2. Número de lote: 0 (todos)
3. Índice mínimo: 50
4. Índice máximo: 150
5. Marcar "Eliminar filas vacías"
6. Click en "Procesar Datos"
7. Exportar resultado como "Rango_50_150.xlsx"
```

---

## Ejecutar la Aplicación

### Opción 1: Desde terminal/consola

```bash
# Windows
python data_processor_gui.py

# macOS/Linux
python3 data_processor_gui.py
```

### Opción 2: Crear acceso directo (Windows)

Crear archivo `ejecutar.bat`:
```batch
@echo off
python data_processor_gui.py
pause
```

### Opción 3: Crear archivo ejecutable (opcional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed data_processor_gui.py
```

El ejecutable se generará en la carpeta `dist/`.

---

## Estructura de Datos Esperada

El archivo CSV debe tener las siguientes columnas (mínimo):

```
Timestamp_PC | Num_Lote | T1_Index | T1_ResetCount | T1_FineNS | 
T2_Index | T2_ResetCount | T2_FineNS | t1_nS | ... (más columnas)
```

**Ejemplo de formato esperado:**
```
17:19:38.494;1;0;42568;21,82;0;143806;40;4256821,82;14380640;
17:19:38.494;1;1;310792;40;1;351068;3,64;31079240;35106803,64;
```

**Nota:** Los valores decimales usan coma (,) como separador.

---

## Estadísticas Disponibles

La pestaña "Estadísticas" muestra:

- Número total de filas procesadas
- Número de columnas
- Para cada columna numérica:
  - Cantidad de valores válidos
  - Valor mínimo
  - Valor máximo
  - Promedio
- Timestamp del primer registro

---

## Solución de Problemas

### Problema: "No module named 'PyQt6'"
```bash
# Solución: Instalar PyQt6
pip install PyQt6
```

### Problema: "No such file or directory"
```bash
# Verificar que el archivo existe:
- Usar ruta absoluta o colocar archivo en carpeta actual
- Usar path con "/" en lugar de "\"
```

### Problema: Aplicación se congela
```bash
# La aplicación usa threads para procesamiento asincrónico
# Si aún se congela, reinicie la aplicación
```

### Problema: Datos no se muestran en tabla
```bash
- Verificar que el archivo CSV está bien formado
- Verificar separador (debe ser ";")
- Verificar que no hay caracteres especiales problemáticos
```

---

## Características Avanzadas (Código)

Para personalizar la aplicación, puede editar:

### Cambiar separador de archivo
Línea ~116 en `data_processor_gui.py`:
```python
self.df = pd.read_csv(file_path, sep=';')  # Cambiar ';' por ','
```

### Aumentar número de filas mostradas
Línea ~173:
```python
self.raw_table.setRowCount(min(100, len(self.df)))  # Cambiar 100 a otro valor
```

### Agregar nuevas columnas calculadas
En la función `DataProcessingThread.run()` (línea ~57), agregar lógica como:
```python
filtered_df['Nueva_Columna'] = filtered_df['Col1'] * filtered_df['Col2']
```

---

## Próximas Mejoras Sugeridas

1. **Visualización gráfica**: Agregar gráficos de líneas y dispersión
2. **Base de datos**: Guardar experimentos en SQL
3. **Validación de datos**: Verificar integridad antes de procesar
4. **Filtros avanzados**: Por rangos de tiempo, valores específicos
5. **Múltiples archivos**: Procesar lotes de archivos
6. **Reportes PDF**: Generar reportes formales
7. **Historial**: Guardar y restaurar parámetros previos

---

## Contacto y Soporte

Para reportar bugs o sugerencias, revise el código y agregue funcionalidades según necesite.

---

**Última actualización**: Febrero 2026
**Versión**: 1.0
