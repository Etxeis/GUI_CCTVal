"""
Archivo de configuración para la aplicación de procesamiento de datos
Este archivo contiene parámetros que pueden ser ajustados sin modificar el código principal
"""

# CONFIGURACIÓN DE INTERFAZ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Procesador Avanzado de Datos Experimentales"

# CONFIGURACIÓN DE FUENTES
TITLE_FONT_SIZE = 12
LABEL_FONT_SIZE = 10
SMALL_FONT_SIZE = 9
FONT_FAMILY = "Arial"

# CONFIGURACIÓN DE DATOS
CSV_SEPARATOR = ';'
DECIMAL_SEPARATOR = ','
MAX_ROWS_DISPLAY = 50  # Máximo de filas mostradas en tablas
MAX_INITIAL_ROWS = 100  # Máximo de filas iniciales en carga

# CONFIGURACIÓN DE PROCESAMIENTO
DEFAULT_LOTE_NUMBER = 1
DEFAULT_MIN_INDEX = 0
DEFAULT_MAX_INDEX = 0
DEFAULT_REMOVE_NULLS = True
DEFAULT_NORMALIZE = False

# COLUMNAS ESPERADAS (para validación)
EXPECTED_COLUMNS = [
    'Timestamp_PC',
    'Num_Lote',
    'T1_Index',
    'T1_ResetCount',
    'T1_FineNS',
    'T2_Index',
    'T2_ResetCount',
    'T2_FineNS',
    't1_nS'
]

# COLUMNAS NUMÉRICAS (para procesamiento)
NUMERIC_COLUMNS = [
    'T1_ResetCount',
    'T1_FineNS',
    'T2_ResetCount',
    'T2_FineNS'
]

# ESTILOS
COLORS = {
    'success': '#4CAF50',
    'primary': '#2196F3',
    'warning': '#FF9800',
    'error': '#f44336',
    'light_bg': '#f5f5f5',
    'border': '#ddd'
}

BUTTON_STYLES = {
    'success': (
        "background-color: #4CAF50; color: white; font-weight: bold; "
        "padding: 10px; border-radius: 5px; font-size: 11px;"
    ),
    'primary': (
        "background-color: #2196F3; color: white; font-weight: bold; "
        "padding: 8px; border-radius: 5px; font-size: 10px;"
    ),
    'warning': (
        "background-color: #FF9800; color: white; font-weight: bold; "
        "padding: 8px; border-radius: 5px; font-size: 10px;"
    )
}

# MENSAJES
MESSAGES = {
    'no_file_loaded': 'Por favor, cargue un archivo primero',
    'processing': '⏳ Procesando datos...',
    'success': '✓ Procesado',
    'error': '❌ Error',
    'no_data': 'No data found with the specified parameters',
    'export_success': 'Archivo exportado exitosamente',
    'file_loaded': 'Archivo cargado'
}

# CONFIGURACIÓN DE EXPORTACIÓN
EXPORT_FORMATS = {
    'csv': {
        'extension': 'csv',
        'separator': ';',
        'decimal': ','
    },
    'xlsx': {
        'extension': 'xlsx',
        'engine': 'openpyxl'
    }
}

# CONFIGURACIÓN DE LOGGING
LOG_ENABLED = False
LOG_FILE = 'data_processor.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# CONFIGURACIÓN DE BASE DE DATOS (para versiones futuras)
DATABASE_ENABLED = False
DATABASE_TYPE = 'sqlite'  # sqlite, postgresql, mysql
DATABASE_FILE = 'experiments.db'
DATABASE_HOST = 'localhost'
DATABASE_PORT = 5432
DATABASE_NAME = 'data_processor'

# VALIDACIÓN DE DATOS
VALIDATE_ON_LOAD = True
VALIDATE_NUMERIC_COLUMNS = True
REMOVE_INVALID_ROWS = False

# ESTADÍSTICAS A MOSTRAR
STATISTICS_TO_CALCULATE = [
    'count',      # Cantidad de valores
    'min',        # Valor mínimo
    'max',        # Valor máximo
    'mean',       # Promedio
    'std',        # Desviación estándar
    'median'      # Mediana
]

# CACHÉ
ENABLE_CACHE = True
CACHE_SIZE = 100  # MB
CACHE_TIMEOUT = 3600  # segundos

# VERSIÓN DE LA APLICACIÓN
APP_VERSION = '1.0'
APP_BUILD_DATE = 'February 2026'
AUTHOR = 'Data Processing Team'
