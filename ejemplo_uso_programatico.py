"""
Ejemplo de uso programático del procesador de datos
Muestra cómo usar las funciones de procesamiento sin interfaz gráfica
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataProcessor:
    """Clase para procesar datos experimentales"""
    
    def __init__(self, csv_file, separator=';'):
        """
        Inicializar procesador de datos
        
        Args:
            csv_file (str): Ruta al archivo CSV
            separator (str): Separador de columnas
        """
        self.csv_file = csv_file
        self.separator = separator
        self.df = None
        self.processed_df = None
    
    def load_data(self):
        """Cargar datos desde archivo CSV"""
        try:
            self.df = pd.read_csv(self.csv_file, sep=self.separator)
            print(f"✓ Archivo cargado: {Path(self.csv_file).name}")
            print(f"  Filas: {len(self.df)}, Columnas: {len(self.df.columns)}")
            return True
        except Exception as e:
            print(f"❌ Error al cargar archivo: {str(e)}")
            return False
    
    def filter_by_lote(self, lote_number):
        """
        Filtrar datos por número de lote
        
        Args:
            lote_number (int): Número de lote
        """
        if self.df is None:
            print("❌ Primero debes cargar datos con load_data()")
            return
        
        self.processed_df = self.df[self.df['Num_Lote'] == lote_number].copy()
        print(f"✓ Filtrado por lote {lote_number}: {len(self.processed_df)} registros")
    
    def filter_by_index_range(self, min_index=None, max_index=None):
        """
        Filtrar datos por rango de índices
        
        Args:
            min_index (int): Índice mínimo
            max_index (int): Índice máximo
        """
        if self.processed_df is None:
            self.processed_df = self.df.copy()
        
        if min_index is not None:
            self.processed_df = self.processed_df[
                self.processed_df['T1_Index'] >= min_index
            ]
        
        if max_index is not None:
            self.processed_df = self.processed_df[
                self.processed_df['T1_Index'] <= max_index
            ]
        
        print(f"✓ Filtrado por rango: {len(self.processed_df)} registros")
    
    def remove_empty_rows(self):
        """Eliminar filas vacías"""
        if self.processed_df is None:
            self.processed_df = self.df.copy()
        
        initial_rows = len(self.processed_df)
        self.processed_df = self.processed_df.dropna(how='all')
        removed = initial_rows - len(self.processed_df)
        print(f"✓ Filas vacías eliminadas: {removed}")
    
    def normalize_numeric_columns(self):
        """Normalizar columnas numéricas a rango 0-1"""
        if self.processed_df is None:
            self.processed_df = self.df.copy()
        
        numeric_cols = self.processed_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            min_val = self.processed_df[col].min()
            max_val = self.processed_df[col].max()
            
            if max_val - min_val != 0:
                self.processed_df[f'{col}_norm'] = (
                    (self.processed_df[col] - min_val) / (max_val - min_val)
                )
        
        print(f"✓ Normalización completada: {len(numeric_cols)} columnas normalizadas")
    
    def convert_decimal_format(self):
        """Convertir formato decimal de coma a punto"""
        if self.processed_df is None:
            self.processed_df = self.df.copy()
        
        numeric_cols = ['T1_ResetCount', 'T1_FineNS', 'T2_ResetCount', 'T2_FineNS']
        
        for col in numeric_cols:
            if col in self.processed_df.columns:
                self.processed_df[col] = pd.to_numeric(
                    self.processed_df[col].astype(str).str.replace(',', '.'),
                    errors='coerce'
                )
        
        print(f"✓ Formato decimal convertido")
    
    def calculate_statistics(self):
        """Calcular estadísticas descriptivas"""
        if self.processed_df is None:
            print("❌ Primero procesa los datos")
            return None
        
        stats = {}
        numeric_cols = self.processed_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            valid = self.processed_df[col].notna().sum()
            if valid > 0:
                stats[col] = {
                    'válidos': valid,
                    'mínimo': float(self.processed_df[col].min()),
                    'máximo': float(self.processed_df[col].max()),
                    'promedio': float(self.processed_df[col].mean()),
                    'std': float(self.processed_df[col].std())
                }
        
        return stats
    
    def export_csv(self, output_file):
        """
        Exportar datos a CSV
        
        Args:
            output_file (str): Ruta del archivo de salida
        """
        if self.processed_df is None:
            print("❌ Primero procesa los datos")
            return
        
        try:
            self.processed_df.to_csv(output_file, sep=';', index=False, decimal=',')
            print(f"✓ Exportado a: {output_file}")
        except Exception as e:
            print(f"❌ Error al exportar: {str(e)}")
    
    def export_excel(self, output_file):
        """
        Exportar datos a Excel
        
        Args:
            output_file (str): Ruta del archivo de salida
        """
        if self.processed_df is None:
            print("❌ Primero procesa los datos")
            return
        
        try:
            self.processed_df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"✓ Exportado a: {output_file}")
        except Exception as e:
            print(f"❌ Error al exportar: {str(e)}")
    
    def get_summary(self):
        """Obtener resumen del procesamiento"""
        if self.processed_df is None:
            print("❌ Primero procesa los datos")
            return
        
        summary = {
            'filas_totales': len(self.processed_df),
            'columnas': len(self.processed_df.columns),
            'nombres_columnas': list(self.processed_df.columns),
            'memoria_mb': round(self.processed_df.memory_usage(deep=True).sum() / 1024**2, 2)
        }
        
        return summary


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EJEMPLOS DE USO - PROCESADOR DE DATOS EXPERIMENTALES")
    print("=" * 70)
    
    # Crear instancia del procesador
    processor = DataProcessor('Reporte_de_Datos.csv')
    
    # ========================================================================
    # EJEMPLO 1: Procesar lote completo
    # ========================================================================
    print("\n📌 EJEMPLO 1: Procesar lote 1 completo")
    print("-" * 70)
    
    processor.load_data()
    processor.filter_by_lote(1)
    processor.convert_decimal_format()
    
    stats = processor.calculate_statistics()
    print(f"\n📊 Estadísticas de T1_ResetCount:")
    if 'T1_ResetCount' in stats:
        for key, value in stats['T1_ResetCount'].items():
            print(f"   {key}: {value:.2f}")
    
    processor.export_csv('lote_1.csv')
    processor.export_excel('lote_1.xlsx')
    
    # ========================================================================
    # EJEMPLO 2: Procesar rango específico de índices
    # ========================================================================
    print("\n\n📌 EJEMPLO 2: Procesar rango de índices 50-150")
    print("-" * 70)
    
    processor2 = DataProcessor('Reporte_de_Datos.csv')
    processor2.load_data()
    processor2.filter_by_index_range(min_index=50, max_index=150)
    processor2.remove_empty_rows()
    processor2.convert_decimal_format()
    
    summary = processor2.get_summary()
    print(f"\n📋 Resumen:")
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    processor2.export_csv('rango_50_150.csv')
    
    # ========================================================================
    # EJEMPLO 3: Procesar, normalizar y exportar
    # ========================================================================
    print("\n\n📌 EJEMPLO 3: Procesar, normalizar y analizar")
    print("-" * 70)
    
    processor3 = DataProcessor('Reporte_de_Datos.csv')
    processor3.load_data()
    processor3.filter_by_lote(1)
    processor3.remove_empty_rows()
    processor3.convert_decimal_format()
    processor3.normalize_numeric_columns()
    
    stats = processor3.calculate_statistics()
    print(f"\n📊 Estadísticas después de normalización:")
    print(f"   Total de columnas: {len(stats)}")
    
    processor3.export_excel('lote_1_normalizado.xlsx')
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("\n\n" + "=" * 70)
    print("✓ EJEMPLOS COMPLETADOS")
    print("=" * 70)
    print("""
Archivos generados:
  • lote_1.csv
  • lote_1.xlsx
  • rango_50_150.csv
  • lote_1_normalizado.xlsx

Para usar esta clase en tus propios scripts:

    from ejemplo_uso_programatico import DataProcessor
    
    processor = DataProcessor('tu_archivo.csv')
    processor.load_data()
    processor.filter_by_lote(1)
    processor.convert_decimal_format()
    processor.export_excel('resultado.xlsx')
    
Métodos disponibles:
    • load_data()
    • filter_by_lote(lote_number)
    • filter_by_index_range(min, max)
    • remove_empty_rows()
    • normalize_numeric_columns()
    • convert_decimal_format()
    • calculate_statistics()
    • export_csv(file)
    • export_excel(file)
    • get_summary()
    """)
