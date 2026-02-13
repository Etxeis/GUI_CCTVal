# Procesador Avanzado de Datos Experimentales 🔬

Aplicación GUI profesional para procesamiento de datos experimentales con interface moderna y funcionalidades avanzadas de análisis.

---

## 📦 Contenido del Proyecto

Este paquete incluye todo lo necesario para desarrollar e implementar una interfaz gráfica de procesamiento de datos:

### Archivos Principales

| Archivo | Descripción |
|---------|-----------|
| **data_processor_advanced.py** | ⭐ Versión recomendada - Aplicación completa con todas las características |
| **data_processor_gui.py** | Versión simple - Más ligera y básica |
| **config.py** | Archivo de configuración centralizado |
| **Reporte_de_Datos.csv** | Archivo de ejemplo de datos |

### Documentación

| Archivo | Contenido |
|---------|----------|
| **INICIO_RAPIDO.md** | Guía rápida (5 minutos) |
| **INSTRUCCIONES.md** | Documentación completa y detallada |
| **README.md** | Este archivo |

---

## 🚀 Inicio Rápido

### 1. Instalación (2 minutos)

```bash
# Instalar dependencias
pip install PyQt6 pandas numpy openpyxl

# Clonar o descargar el proyecto
# (ya descargaste los archivos)
```

### 2. Ejecutar la aplicación (1 minuto)

```bash
# Versión recomendada
python data_processor_advanced.py

# O versión simple
python data_processor_gui.py
```

### 3. Procesar datos (2 minutos)

```
1. Click en "Cargar" → Selecciona archivo CSV
2. Ajusta parámetros (lote, índices, opciones)
3. Click en "▶ Procesar Datos"
4. Click en "💾 Exportar CSV" o "📊 Exportar Excel"
```

---

## ✨ Características Principales

### ✓ Carga de Datos
- Importar archivos CSV con formato estándar
- Validación automática de estructura
- Vista previa de datos cargados (primeras 50 filas)
- Información en tiempo real: filas × columnas

### ✓ Filtros Avanzados
- **Filtro por lote**: Seleccionar número de lote específico
- **Filtro por índice**: Rango mínimo-máximo de T1_Index
- **Limpieza**: Eliminar filas vacías automáticamente
- **Normalización**: Escalar valores a rango 0-1

### ✓ Procesamiento
- Procesamiento asincrónico (no congela interfaz)
- Barra de progreso visual
- Manejo robusto de errores
- Conversión automática de decimales (coma a punto)

### ✓ Visualización
- **4 pestañas informativas**:
  - Datos Crudos: Vista de archivo original
  - Datos Procesados: Resultado después de filtros
  - Estadísticas: Tabla resumida con min/máx/promedio
  - Resumen: Informe completo del procesamiento

### ✓ Exportación
- **Formato CSV**: Separador `;`, decimales `,`
- **Formato Excel**: `.xlsx` moderno con formato
- Diálogos de selección de carpeta
- Confirmación de exportación exitosa

### ✓ Interfaz Intuitiva
- Diseño profesional con colores temáticos
- Iconos en botones principales
- Mensajes de estado en tiempo real
- Panel lateral para fácil acceso a parámetros

---

## 📊 Estadísticas Disponibles

Para cada columna numérica, se calculan automáticamente:

| Métrica | Descripción |
|---------|-----------|
| **Válidos** | Cantidad de valores no nulos |
| **Mínimo** | Valor más bajo |
| **Máximo** | Valor más alto |
| **Promedio** | Media aritmética |

---

## 🎯 Casos de Uso

### 1. Procesar un lote completo
```
Lote: 1
Índices: Sin límite (0 a 0)
→ Obtener todos los datos del lote 1
```

### 2. Extraer rango específico
```
Lote: Cualquiera
Índice Mín: 100
Índice Máx: 500
→ Datos solo del rango 100-500
```

### 3. Limpiar y normalizar
```
✓ Eliminar filas vacías
✓ Normalizar valores
→ Datos listos para análisis
```

### 4. Generar reporte
```
1. Procesar datos
2. Ver estadísticas completas en pestaña "Estadísticas"
3. Exportar como Excel para presentación
```

---

## 🔧 Requisitos del Sistema

### Software
- **Python**: 3.8 - 3.11 (se recomienda 3.10+)
- **SO**: Windows, macOS, Linux

### Dependencias
```
PyQt6        >= 6.0      (GUI moderna)
pandas       >= 1.3      (procesamiento datos)
numpy        >= 1.20     (cálculos)
openpyxl     >= 3.0      (Excel)
```

### Hardware Mínimo
- RAM: 512 MB
- Disco: 100 MB (instalación)
- Procesador: Cualquiera (Intel/AMD dual core o superior)

---

## 📝 Formato de Datos Esperado

### Estructura CSV
```
Timestamp_PC;Num_Lote;T1_Index;T1_ResetCount;T1_FineNS;T2_Index;T2_ResetCount;T2_FineNS;t1_nS;t1_nS;
17:19:38.494;1;0;42568;21,82;0;143806;40;4256821,82;14380640;
17:19:38.494;1;1;310792;40;1;351068;3,64;31079240;35106803,64;
```

### Características
- **Separador**: `;` (punto y coma)
- **Decimales**: `,` (coma)
- **Codificación**: UTF-8
- **Formato**: CSV estándar

---

## 🎨 Interfaz Gráfica

### Panel Izquierdo
Lugar para ajustar parámetros del experimento:
- Carga de archivos
- Filtros
- Opciones de procesamiento
- Controles principales

### Panel Derecho
4 pestañas con resultados:
1. **Datos Crudos** - Primeros 50 registros originales
2. **Datos Procesados** - Primeros 50 registros procesados
3. **Estadísticas** - Tabla con métricas por columna
4. **Resumen** - Informe completo del procesamiento

---

## 💾 Exportación

### CSV
```
Formato: data_procesada.csv
Separador: ;
Decimales: ,
Codificación: UTF-8
```

### Excel
```
Formato: data_procesada.xlsx
Motor: openpyxl
Validación: Automática
```

---

## 🔍 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install PyQt6 pandas numpy openpyxl
```

### Error: Tabla vacía
- Verificar que el archivo tiene datos
- Verificar formato CSV (separador `;`)
- Revisar criterios de filtrado

### Aplicación lenta
- Aplicación es asincrónica, esperar a barra de progreso
- Para archivos grandes (>100k registros), considerar procesamiento en partes

### Datos no se muestran bien
- Verificar codificación: debe ser UTF-8
- Verificar separador: debe ser `;`
- Verificar que no hay valores especiales problemáticos

---

## 📚 Documentación Completa

Para más información detallada:
1. Leer **INSTRUCCIONES.md** - Documentación técnica completa
2. Leer **INICIO_RAPIDO.md** - Guía de 5 minutos
3. Revisar comentarios en código Python
4. Consultar archivo **config.py** para personalizaciones

---

## 🚀 Próximas Características

Mejoras planeadas para futuras versiones:

- [ ] Procesamiento en lotes (múltiples archivos)
- [ ] Gráficos interactivos (líneas, dispersión, histogramas)
- [ ] Filtros avanzados por fecha y rangos de valores
- [ ] Base de datos para histórico de experimentos
- [ ] Generación de reportes PDF
- [ ] Tema oscuro/claro
- [ ] Exportación a JSON
- [ ] API REST para integración

---

## 🛠️ Personalización

### Cambiar colores
```python
# Editar archivo config.py
COLORS = {
    'success': '#4CAF50',
    'primary': '#2196F3',
    # ...
}
```

### Agregar columnas calculadas
```python
# En data_processor_advanced.py
# Función: DataProcessingThread.run()
filtered_df['nueva_columna'] = filtered_df['col1'] * filtered_df['col2']
```

### Cambiar separador CSV
```python
# Línea ~200 en data_processor_advanced.py
self.df = pd.read_csv(file_path, sep=',')  # Cambiar de ';' a ','
```

---

## 📋 Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas: `pip install PyQt6 pandas numpy openpyxl`
- [ ] Archivo `data_processor_advanced.py` en carpeta
- [ ] Archivo de datos (CSV) disponible
- [ ] Permisos de lectura/escritura en carpeta

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Procesar experimento simple
```python
# Línea de comandos
python data_processor_advanced.py

# En la interfaz:
# 1. Click "Cargar" → Reporte_de_Datos.csv
# 2. Número de lote: 1
# 3. Click "▶ Procesar Datos"
# 4. Click "📊 Exportar Excel"
# → Se genera: resultado.xlsx
```

### Ejemplo 2: Analizar rango específico
```
# Parámetros:
# • Lote: 0 (todos)
# • Índice mín: 50
# • Índice máx: 150
# ✓ Eliminar filas vacías
# ✓ Normalizar valores

# Resultado: Datos normalizados del rango 50-150
```

---

## 📞 Soporte

Para reportar problemas o sugerencias:
1. Revisar guías de troubleshooting arriba
2. Verificar formato de datos
3. Consultar documentación en INSTRUCCIONES.md

---

## 📄 Licencia

Proyecto desarrollado para procesamiento de datos experimentales.
Libre para uso académico y comercial.

---

## 🎉 ¡Lista para Usar!

La aplicación está completamente funcional y lista para usar.

**Próximos pasos:**
1. ✅ Descargar todos los archivos
2. ✅ Instalar dependencias
3. ✅ Ejecutar aplicación
4. ✅ Cargar datos
5. ✅ ¡Procesar y analizar!

---

**Versión:** 1.0  
**Actualizado:** Febrero 2026  
**Estado:** ✅ Funcional y listo para producción

