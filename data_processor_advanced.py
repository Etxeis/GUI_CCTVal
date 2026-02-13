"""
Advanced Data Processor GUI Application
Interfaz gráfica avanzada para procesamiento de datos experimentales
Incluye visualización de gráficos y análisis estadístico mejorado
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import json

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QTabWidget, QFileDialog,
    QMessageBox, QProgressBar, QCheckBox, QSlider, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt6.QtCore import QPointF, QDateTime


class DataProcessingThread(QThread):
    """Thread para procesar datos sin bloquear la interfaz"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(pd.DataFrame)
    error = pyqtSignal(str)
    
    def __init__(self, df, params):
        super().__init__()
        self.df = df
        self.params = params
    
    def run(self):
        try:
            # Filtrar por número de lote si está especificado
            filtered_df = self.df.copy()
            
            if self.params['lote_number'] > 0:
                filtered_df = filtered_df[filtered_df['Num_Lote'] == self.params['lote_number']]
            
            self.progress.emit(25)
            
            # Filtrar por rango de índices si está especificado
            if self.params['min_index'] > 0:
                filtered_df = filtered_df[filtered_df['T1_Index'] >= self.params['min_index']]
            
            if self.params['max_index'] > 0:
                filtered_df = filtered_df[filtered_df['T1_Index'] <= self.params['max_index']]
            
            self.progress.emit(50)
            
            # Eliminar filas vacías si se indica
            if self.params['remove_nulls']:
                filtered_df = filtered_df.dropna(how='all')
            
            # Procesar datos numéricos
            numeric_cols = ['T1_ResetCount', 'T1_FineNS', 'T2_ResetCount', 'T2_FineNS']
            for col in numeric_cols:
                if col in filtered_df.columns:
                    filtered_df[col] = pd.to_numeric(
                        filtered_df[col].astype(str).str.replace(',', '.'),
                        errors='coerce'
                    )
            
            self.progress.emit(75)
            
            # Normalizar si se indica
            if self.params['normalize']:
                for col in filtered_df.select_dtypes(include=[np.number]).columns:
                    min_val = filtered_df[col].min()
                    max_val = filtered_df[col].max()
                    if max_val - min_val != 0:
                        filtered_df[f'{col}_normalized'] = (filtered_df[col] - min_val) / (max_val - min_val)
            
            self.progress.emit(100)
            
            if len(filtered_df) > 0:
                self.finished.emit(filtered_df)
            else:
                self.error.emit("No data found with the specified parameters")
                
        except Exception as e:
            self.error.emit(f"Error during processing: {str(e)}")


class AdvancedDataProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.processed_df = None
        self.initUI()
    
    def initUI(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("Procesador Avanzado de Datos Experimentales")
        self.setGeometry(50, 50, 1600, 1000)
        
        # Tema de fuente
        self.title_font = QFont("Arial", 12, QFont.Weight.Bold)
        self.label_font = QFont("Arial", 10)
        self.small_font = QFont("Arial", 9)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Panel izquierdo - Parámetros
        left_panel = self.create_parameters_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Panel derecho - Datos y resultados
        right_panel = self.create_results_panel()
        main_layout.addWidget(right_panel, 2)
        
        self.statusBar().showMessage("Ready")
    
    def create_parameters_panel(self):
        """Crear panel de parámetros"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        group = QGroupBox("Parámetros del Experimento")
        group.setFont(self.title_font)
        layout = QVBoxLayout()
        
        # Archivo
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Archivo:"))
        self.file_label = QLabel("No seleccionado")
        self.file_label.setStyleSheet("color: gray; font-style: italic;")
        self.file_label.setFont(self.small_font)
        file_layout.addWidget(self.file_label, 1)
        file_btn = QPushButton("Cargar")
        file_btn.setMaximumWidth(80)
        file_btn.clicked.connect(self.load_file)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)
        
        layout.addSpacing(15)
        layout.addWidget(self.create_separator("FILTROS"))
        
        # Número de lote
        lote_layout = QHBoxLayout()
        lote_layout.addWidget(QLabel("Número de lote:"))
        self.lote_spinbox = QSpinBox()
        self.lote_spinbox.setValue(1)
        self.lote_spinbox.setMinimum(0)
        self.lote_spinbox.setMaximum(99999)
        lote_layout.addWidget(self.lote_spinbox)
        lote_layout.addStretch()
        layout.addLayout(lote_layout)
        
        # Rango de índices
        range_label = QLabel("Rango de índices T1:")
        range_label.setFont(self.small_font)
        range_label.setStyleSheet("color: #555;")
        layout.addWidget(range_label)
        
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Mín:"))
        self.min_index_spinbox = QSpinBox()
        self.min_index_spinbox.setValue(0)
        self.min_index_spinbox.setMinimum(0)
        self.min_index_spinbox.setMaximum(999999)
        range_layout.addWidget(self.min_index_spinbox)
        
        range_layout.addSpacing(10)
        range_layout.addWidget(QLabel("Máx:"))
        self.max_index_spinbox = QSpinBox()
        self.max_index_spinbox.setValue(0)
        self.max_index_spinbox.setMinimum(0)
        self.max_index_spinbox.setMaximum(999999)
        range_layout.addWidget(self.max_index_spinbox)
        range_layout.addStretch()
        layout.addLayout(range_layout)
        
        layout.addSpacing(15)
        layout.addWidget(self.create_separator("OPCIONES"))
        
        # Opciones adicionales
        self.remove_nulls_check = QCheckBox("Eliminar filas vacías")
        self.remove_nulls_check.setChecked(True)
        layout.addWidget(self.remove_nulls_check)
        
        self.normalize_check = QCheckBox("Normalizar valores (0-1)")
        self.normalize_check.setChecked(False)
        layout.addWidget(self.normalize_check)
        
        layout.addSpacing(20)
        layout.addWidget(self.create_separator("CONTROL"))
        
        # Botones de control
        process_btn = QPushButton("▶ Procesar Datos")
        process_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; "
            "padding: 10px; border-radius: 5px; font-size: 11px;"
        )
        process_btn.clicked.connect(self.process_data)
        layout.addWidget(process_btn)
        
        export_csv_btn = QPushButton("💾 Exportar CSV")
        export_csv_btn.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; "
            "padding: 8px; border-radius: 5px; font-size: 10px;"
        )
        export_csv_btn.clicked.connect(lambda: self.export_data('csv'))
        layout.addWidget(export_csv_btn)
        
        export_xlsx_btn = QPushButton("📊 Exportar Excel")
        export_xlsx_btn.setStyleSheet(
            "background-color: #FF9800; color: white; font-weight: bold; "
            "padding: 8px; border-radius: 5px; font-size: 10px;"
        )
        export_xlsx_btn.clicked.connect(lambda: self.export_data('xlsx'))
        layout.addWidget(export_xlsx_btn)
        
        layout.addSpacing(10)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { border: 1px solid #ccc; border-radius: 3px; }")
        layout.addWidget(self.progress_bar)
        
        # Info box
        self.info_box = QLabel("")
        self.info_box.setStyleSheet(
            "background-color: #e3f2fd; padding: 8px; border-radius: 3px; "
            "border-left: 4px solid #2196F3;"
        )
        self.info_box.setFont(self.small_font)
        self.info_box.setWordWrap(True)
        layout.addWidget(self.info_box)
        
        layout.addStretch()
        
        group.setLayout(layout)
        scroll.setWidget(group)
        return scroll
    
    def create_separator(self, text=""):
        """Crear separador visual"""
        label = QLabel(text)
        label.setFont(self.small_font)
        label.setStyleSheet("color: #999; font-weight: bold; padding: 5px 0px;")
        return label
    
    def create_results_panel(self):
        """Crear panel de resultados y visualización"""
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(
            "QTabBar::tab { padding: 8px 20px; } "
            "QTabBar::tab:selected { background-color: #e0e0e0; }"
        )
        
        # Tab 1: Datos crudos
        raw_tab = QWidget()
        raw_layout = QVBoxLayout(raw_tab)
        
        raw_title = QLabel("📋 Datos Cargados")
        raw_title.setFont(self.title_font)
        raw_layout.addWidget(raw_title)
        
        self.raw_table = QTableWidget()
        self.raw_table.setColumnCount(0)
        self.raw_table.setRowCount(0)
        self.raw_table.setMaximumHeight(250)
        raw_layout.addWidget(self.raw_table)
        
        tab_widget.addTab(raw_tab, "Datos Crudos")
        
        # Tab 2: Datos procesados
        processed_tab = QWidget()
        processed_layout = QVBoxLayout(processed_tab)
        
        processed_title = QLabel("✓ Datos Procesados")
        processed_title.setFont(self.title_font)
        processed_layout.addWidget(processed_title)
        
        self.processed_table = QTableWidget()
        self.processed_table.setColumnCount(0)
        self.processed_table.setRowCount(0)
        processed_layout.addWidget(self.processed_table)
        
        tab_widget.addTab(processed_tab, "Datos Procesados")
        
        # Tab 3: Estadísticas
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        
        stats_title = QLabel("📊 Estadísticas Detalladas")
        stats_title.setFont(self.title_font)
        stats_layout.addWidget(stats_title)
        
        self.stats_text = QLabel("Cargue y procese datos para ver estadísticas")
        self.stats_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stats_text.setStyleSheet(
            "background-color: #f5f5f5; padding: 12px; border-radius: 5px; "
            "border: 1px solid #ddd;"
        )
        self.stats_text.setWordWrap(True)
        self.stats_text.setFont(self.small_font)
        stats_layout.addWidget(self.stats_text)
        
        tab_widget.addTab(stats_tab, "Estadísticas")
        
        # Tab 4: Resumen de procesamiento
        summary_tab = QWidget()
        summary_layout = QVBoxLayout(summary_tab)
        
        summary_title = QLabel("🔍 Resumen de Procesamiento")
        summary_title.setFont(self.title_font)
        summary_layout.addWidget(summary_title)
        
        self.summary_text = QLabel("Ejecute un procesamiento para ver el resumen")
        self.summary_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.summary_text.setStyleSheet(
            "background-color: #f9f9f9; padding: 12px; border-radius: 5px; "
            "border: 1px solid #ddd; font-family: monospace;"
        )
        self.summary_text.setWordWrap(True)
        self.summary_text.setFont(QFont("Courier New", 9))
        summary_layout.addWidget(self.summary_text)
        
        tab_widget.addTab(summary_tab, "Resumen")
        
        return tab_widget
    
    def load_file(self):
        """Cargar archivo de datos"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo de datos", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=';')
                self.file_label.setText(Path(file_path).name)
                self.file_label.setStyleSheet("color: green; font-weight: bold;")
                self.display_raw_data()
                
                info_msg = f"✓ {Path(file_path).name}: {len(self.df)} filas × {len(self.df.columns)} columnas"
                self.info_box.setText(info_msg)
                self.info_box.setStyleSheet(
                    "background-color: #e8f5e9; padding: 8px; border-radius: 3px; "
                    "border-left: 4px solid #4CAF50; color: #2e7d32;"
                )
                
                self.statusBar().showMessage(f"Cargado: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")
                self.statusBar().showMessage("Error al cargar archivo")
    
    def display_raw_data(self):
        """Mostrar datos crudos en tabla"""
        if self.df is not None:
            self.raw_table.setColumnCount(len(self.df.columns))
            self.raw_table.setHorizontalHeaderLabels(self.df.columns)
            self.raw_table.setRowCount(min(50, len(self.df)))
            
            for i in range(min(50, len(self.df))):
                for j, col in enumerate(self.df.columns):
                    item = QTableWidgetItem(str(self.df.iloc[i, j]))
                    item.setFont(self.small_font)
                    self.raw_table.setItem(i, j, item)
            
            # Ajustar ancho de columnas
            self.raw_table.resizeColumnsToContents()
    
    def process_data(self):
        """Procesar datos con parámetros seleccionados"""
        if self.df is None:
            QMessageBox.warning(self, "Advertencia", "Por favor, cargue un archivo primero")
            return
        
        # Obtener parámetros
        params = {
            'lote_number': self.lote_spinbox.value(),
            'min_index': self.min_index_spinbox.value(),
            'max_index': self.max_index_spinbox.value(),
            'remove_nulls': self.remove_nulls_check.isChecked(),
            'normalize': self.normalize_check.isChecked()
        }
        
        # Iniciar thread de procesamiento
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.info_box.setText("⏳ Procesando datos...")
        self.info_box.setStyleSheet(
            "background-color: #fff3e0; padding: 8px; border-radius: 3px; "
            "border-left: 4px solid #FF9800; color: #e65100;"
        )
        
        self.thread = DataProcessingThread(self.df, params)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.display_processed_data)
        self.thread.error.connect(self.handle_error)
        self.thread.start()
    
    def update_progress(self, value):
        """Actualizar barra de progreso"""
        self.progress_bar.setValue(value)
    
    def display_processed_data(self, df):
        """Mostrar datos procesados"""
        self.processed_df = df
        
        # Mostrar tabla
        self.processed_table.setColumnCount(len(df.columns))
        self.processed_table.setHorizontalHeaderLabels(df.columns)
        self.processed_table.setRowCount(min(50, len(df)))
        
        for i in range(min(50, len(df))):
            for j, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                item.setFont(self.small_font)
                self.processed_table.setItem(i, j, item)
        
        self.processed_table.resizeColumnsToContents()
        
        # Mostrar estadísticas
        self.display_statistics(df)
        self.display_summary(df)
        
        self.progress_bar.setVisible(False)
        
        info_msg = f"✓ Procesado: {len(df)} filas × {len(df.columns)} columnas"
        self.info_box.setText(info_msg)
        self.info_box.setStyleSheet(
            "background-color: #e8f5e9; padding: 8px; border-radius: 3px; "
            "border-left: 4px solid #4CAF50; color: #2e7d32;"
        )
        
        self.statusBar().showMessage(f"✓ Procesados {len(df)} registros")
    
    def display_statistics(self, df):
        """Mostrar estadísticas de los datos procesados"""
        stats_html = "<table style='width:100%; border-collapse:collapse;'>"
        
        # Header
        stats_html += "<tr style='background-color:#f0f0f0; border-bottom:1px solid #ddd;'>"
        stats_html += "<td style='padding:6px; font-weight:bold;'>Campo</td>"
        stats_html += "<td style='padding:6px; font-weight:bold;'>Válidos</td>"
        stats_html += "<td style='padding:6px; font-weight:bold;'>Mínimo</td>"
        stats_html += "<td style='padding:6px; font-weight:bold;'>Máximo</td>"
        stats_html += "<td style='padding:6px; font-weight:bold;'>Promedio</td>"
        stats_html += "</tr>"
        
        row_color = True
        for col in df.columns:
            try:
                numeric_df = pd.to_numeric(
                    df[col].astype(str).str.replace(',', '.'),
                    errors='coerce'
                )
                valid_count = numeric_df.notna().sum()
                
                if valid_count > 0:
                    bg_color = "#f9f9f9" if row_color else "#ffffff"
                    stats_html += f"<tr style='background-color:{bg_color}; border-bottom:1px solid #eee;'>"
                    stats_html += f"<td style='padding:6px;'><b>{col}</b></td>"
                    stats_html += f"<td style='padding:6px;'>{valid_count}</td>"
                    stats_html += f"<td style='padding:6px;'>{numeric_df.min():.2f}</td>"
                    stats_html += f"<td style='padding:6px;'>{numeric_df.max():.2f}</td>"
                    stats_html += f"<td style='padding:6px;'>{numeric_df.mean():.2f}</td>"
                    stats_html += "</tr>"
                    row_color = not row_color
            except:
                pass
        
        stats_html += "</table>"
        
        # Información general
        info_html = f"<br><b>Información General:</b><br>"
        info_html += f"• Total de registros: {len(df)}<br>"
        info_html += f"• Total de columnas: {len(df.columns)}<br>"
        
        if 'Timestamp_PC' in df.columns:
            info_html += f"• Timestamp (primer): {df['Timestamp_PC'].iloc[0]}<br>"
        
        self.stats_text.setText(stats_html + info_html)
    
    def display_summary(self, df):
        """Mostrar resumen de procesamiento"""
        summary = "RESUMEN DE PROCESAMIENTO\n"
        summary += "=" * 50 + "\n\n"
        summary += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += f"Archivos procesados: 1\n"
        summary += f"Total de filas: {len(df)}\n"
        summary += f"Total de columnas: {len(df.columns)}\n\n"
        
        summary += "Parámetros aplicados:\n"
        summary += f"  • Número de lote: {self.lote_spinbox.value()}\n"
        summary += f"  • Índice mínimo: {self.min_index_spinbox.value()}\n"
        summary += f"  • Índice máximo: {self.max_index_spinbox.value()}\n"
        summary += f"  • Eliminar nulos: {self.remove_nulls_check.isChecked()}\n"
        summary += f"  • Normalizar: {self.normalize_check.isChecked()}\n\n"
        
        summary += "Campos en resultado:\n"
        for i, col in enumerate(df.columns, 1):
            summary += f"  {i:2d}. {col}\n"
        
        self.summary_text.setText(summary)
    
    def export_data(self, format_type):
        """Exportar datos procesados"""
        if self.processed_df is None:
            QMessageBox.warning(self, "Advertencia", "Procese datos primero antes de exportar")
            return
        
        extension = "xlsx" if format_type == "xlsx" else "csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", f"{extension.upper()} Files (*.{extension})"
        )
        
        if file_path:
            try:
                if format_type == 'xlsx':
                    self.processed_df.to_excel(file_path, index=False, engine='openpyxl')
                else:
                    self.processed_df.to_csv(file_path, sep=';', index=False, decimal=',')
                
                QMessageBox.information(
                    self, "Éxito", 
                    f"Archivo exportado exitosamente:\n{Path(file_path).name}"
                )
                self.statusBar().showMessage(f"Exportado: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar:\n{str(e)}")
    
    def handle_error(self, error_msg):
        """Manejar errores durante procesamiento"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Error de Procesamiento", error_msg)
        self.info_box.setText(f"❌ Error: {error_msg}")
        self.info_box.setStyleSheet(
            "background-color: #ffebee; padding: 8px; border-radius: 3px; "
            "border-left: 4px solid #f44336; color: #c62828;"
        )
        self.statusBar().showMessage("Error durante procesamiento")


def main():
    app = QApplication(sys.argv)
    window = AdvancedDataProcessorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
