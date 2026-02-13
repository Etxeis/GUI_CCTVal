# Guía Rápida - Procesador de Datos Experimentales

## ⚡ Inicio Rápido (5 minutos)

### 1. Instalar dependencias
```bash
pip install PyQt6 pandas numpy openpyxl
```

### 2. Ejecutar aplicación
```bash
python data_processor_advanced.py
```

---

## 📋 Pasos Básicos

```
1. [Cargar]     → Seleccionar archivo CSV
                   ↓
2. [Configurar] → Ajustar parámetros (lote, índices)
                   ↓
3. [Procesar]   → Click en "▶ Procesar Datos"
                   ↓
4. [Exportar]   → Click en "💾 Exportar CSV" o "📊 Exportar Excel"
```

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Procesar lote completo
```
✓ Archivo: Reporte_de_Datos.csv
✓ Número de lote: 1
✓ Índice mín: 0 (sin límite)
✓ Índice máx: 0 (sin límite)
✓ Click → Procesar
→ Resultado: Todos los datos del lote 1
```

### Ejemplo 2: Extraer rango específico
```
✓ Archivo: Reporte_de_Datos.csv
✓ Número de lote: 0 (todos)
✓ Índice mín: 100
✓ Índice máx: 200
✓ Click → Procesar
→ Resultado: Registros con índices 100-200
```

### Ejemplo 3: Limpiar y normalizar
```
✓ Marcar: ✓ Eliminar filas vacías
✓ Marcar: ✓ Normalizar valores (0-1)
✓ Click → Procesar
→ Resultado: Datos limpios y normalizados
```

---

## 📊 Vistas Disponibles

| Pestaña | Contenido |
|---------|----------|
| **Datos Crudos** | Primeros 50 registros del archivo original |
| **Datos Procesados** | Primeros 50 registros después de aplicar filtros |
| **Estadísticas** | Tabla con min/máx/promedio de columnas numéricas |
| **Resumen** | Informe completo del procesamiento realizado |

---

## 💾 Exportación

### Formato CSV
- Separador: `;` (punto y coma)
- Decimales: `,` (coma)
- Compatible con Excel, programas científicos

### Formato Excel
- Formato: `.xlsx` (Excel moderno)
- Mejor presentación visual
- Más compatibilidad empresarial

---

## ❓ Preguntas Frecuentes

**P: ¿El archivo debe tener un formato específico?**
A: Sí, debe ser CSV con separador `;` (punto y coma). Ver ejemplo en archivo adjunto.

**P: ¿Puedo procesar múltiples archivos a la vez?**
A: En esta versión no. Procese uno a la vez y exporte. Próxima versión tendrá procesamiento en lotes.

**P: ¿Qué significa "Índice mín: 0"?**
A: Significa "sin límite inferior". Use 0 para no filtrar, o indique un número específico.

**P: ¿Puedo personalizar las columnas del resultado?**
A: Edite el archivo Python, sección "DataProcessingThread.run()" (avanzado).

**P: ¿Los datos se modifican permanentemente?**
A: No, solo al exportar. El archivo original no se afecta.

---

## 🔧 Requerimientos Técnicos

| Componente | Especificación |
|-----------|----------------|
| Python | 3.8 - 3.11 (recomendado 3.10) |
| PyQt6 | v6.0+ (GUI moderna) |
| pandas | v1.3+ (procesamiento datos) |
| numpy | v1.20+ (cálculos numéricos) |
| openpyxl | v3.0+ (Excel) |

---

## 📁 Estructura de Archivos

```
proyecto/
├── data_processor_advanced.py    ← Ejecutar ESTO
├── data_processor_gui.py          ← Versión simple (alternativa)
├── INSTRUCCIONES.md               ← Documentación completa
├── INICIO_RAPIDO.md               ← Este archivo
└── Reporte_de_Datos.csv           ← Archivo de ejemplo
```

---

## 🚀 Próximas Mejoras

- [ ] Procesamiento de múltiples archivos en lote
- [ ] Gráficos interactivos (líneas, dispersión)
- [ ] Filtros avanzados por fecha/rango de valores
- [ ] Base de datos SQLite para histórico
- [ ] Generación de reportes PDF
- [ ] Temas oscuro/claro
- [ ] Exportación a JSON

---

## 🆘 Solución de Problemas

```
Problema: "ModuleNotFoundError: No module named 'PyQt6'"
Solución: pip install PyQt6

Problema: Tabla vacía después de procesar
Solución: Verificar que el archivo tenga datos que cumplan criterios

Problema: Errores al exportar
Solución: Asegurar permisos de escritura en carpeta destino
```

---

**¿Necesitas más ayuda?** 
Consulta INSTRUCCIONES.md para documentación completa.

**Versión:** 1.0 Avanzada | **Actualizado:** Febrero 2026
