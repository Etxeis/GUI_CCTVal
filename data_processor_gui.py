"""
Data Processor GUI Application
Interfaz gráfica para procesamiento de datos experimentales con ajuste de parámetros
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QTabWidget, QFileDialog,
    QMessageBox, QProgressBar, QCheckBox, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF


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
            
            # Calcular estadísticas
            if len(filtered_df) > 0:
                # Procesar datos numéricos
                numeric_cols = ['T1_ResetCount', 'T1_FineNS', 'T2_ResetCount', 'T2_FineNS']
                for col in numeric_cols:
                    if col in filtered_df.columns:
                        filtered_df[col] = pd.to_numeric(
                            filtered_df[col].astype(str).str.replace(',', '.'),
                            errors='coerce'
                        )
                
                self.progress.emit(75)
                
                # Agregar columnas calculadas
                if 't1_nS' in filtered_df.columns and 't1_nS' in filtered_df.columns:
                    filtered_df['Time_Difference'] = pd.to_numeric(
                        filtered_df['t1_nS'].astype(str).str.replace(',', '.'),
                        errors='coerce'
                    )
                
                self.progress.emit(100)
                self.finished.emit(filtered_df)
            else:
                self.error.emit("No data found with the specified parameters")
                
        except Exception as e:
            self.error.emit(f"Error during processing: {str(e)}")


class DataProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.processed_df = None
        self.initUI()
    
    def initUI(self):
        """Inicializar la interfaz de usuario"""
        self.setWindowTitle("Procesador de Datos Experimentales")
        self.setGeometry(100, 100, 1400, 900)
        
        # Tema de fuente
        self.title_font = QFont("Arial", 12, QFont.Weight.Bold)
        self.label_font = QFont("Arial", 10)
        
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
        group = QGroupBox("Parámetros del Experimento")
        group.setFont(self.title_font)
        layout = QVBoxLayout()
        
        # Archivo
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Archivo de datos:"))
        self.file_label = QLabel("No seleccionado")
        self.file_label.setStyleSheet("color: gray;")
        file_layout.addWidget(self.file_label)
        file_btn = QPushButton("Cargar...")
        file_btn.clicked.connect(self.load_file)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)
        
        layout.addSpacing(15)
        
        # Número de lote
        lote_layout = QHBoxLayout()
        lote_layout.addWidget(QLabel("Número de lote:"))
        self.lote_spinbox = QSpinBox()
        self.lote_spinbox.setValue(1)
        self.lote_spinbox.setMinimum(0)
        self.lote_spinbox.setMaximum(9999)
        lote_layout.addWidget(self.lote_spinbox)
        lote_layout.addStretch()
        layout.addLayout(lote_layout)
        
        # Rango de índices
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Índice mínimo:"))
        self.min_index_spinbox = QSpinBox()
        self.min_index_spinbox.setValue(0)
        self.min_index_spinbox.setMinimum(0)
        self.min_index_spinbox.setMaximum(9999)
        range_layout.addWidget(self.min_index_spinbox)
        layout.addLayout(range_layout)
        
        range_layout2 = QHBoxLayout()
        range_layout2.addWidget(QLabel("Índice máximo:"))
        self.max_index_spinbox = QSpinBox()
        self.max_index_spinbox.setValue(0)
        self.max_index_spinbox.setMinimum(0)
        self.max_index_spinbox.setMaximum(9999)
        range_layout2.addWidget(self.max_index_spinbox)
        layout.addLayout(range_layout2)
        
        layout.addSpacing(15)
        
        # Opciones adicionales
        self.remove_nulls_check = QCheckBox("Eliminar filas vacías")
        self.remove_nulls_check.setChecked(True)
        layout.addWidget(self.remove_nulls_check)
        
        self.normalize_check = QCheckBox("Normalizar valores numéricos")
        self.normalize_check.setChecked(False)
        layout.addWidget(self.normalize_check)
        
        layout.addSpacing(20)
        
        # Botones de control
        button_layout = QVBoxLayout()
        
        process_btn = QPushButton("Procesar Datos")
        process_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        process_btn.clicked.connect(self.process_data)
        button_layout.addWidget(process_btn)
        
        export_btn = QPushButton("Exportar Resultado")
        export_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        export_btn.clicked.connect(self.export_data)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_results_panel(self):
        """Crear panel de resultados y visualización"""
        tab_widget = QTabWidget()
        
        # Tab 1: Datos crudos
        raw_tab = QWidget()
        raw_layout = QVBoxLayout(raw_tab)
        
        raw_title = QLabel("Datos Cargados")
        raw_title.setFont(self.title_font)
        raw_layout.addWidget(raw_title)
        
        self.raw_table = QTableWidget()
        self.raw_table.setColumnCount(0)
        self.raw_table.setRowCount(0)
        raw_layout.addWidget(self.raw_table)
        
        tab_widget.addTab(raw_tab, "Datos Crudos")
        
        # Tab 2: Datos procesados
        processed_tab = QWidget()
        processed_layout = QVBoxLayout(processed_tab)
        
        processed_title = QLabel("Datos Procesados")
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
        
        stats_title = QLabel("Estadísticas")
        stats_title.setFont(self.title_font)
        stats_layout.addWidget(stats_title)
        
        self.stats_text = QLabel("Cargue y procese datos para ver estadísticas")
        self.stats_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.stats_text.setStyleSheet("background-color: #f5f5f5; padding: 10px; border-radius: 5px;")
        stats_layout.addWidget(self.stats_text)
        
        tab_widget.addTab(stats_tab, "Estadísticas")
        
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
                self.statusBar().showMessage(f"Archivo cargado: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo: {str(e)}")
                self.statusBar().showMessage("Error al cargar archivo")
    
    def display_raw_data(self):
        """Mostrar datos crudos en tabla"""
        if self.df is not None:
            self.raw_table.setColumnCount(len(self.df.columns))
            self.raw_table.setHorizontalHeaderLabels(self.df.columns)
            self.raw_table.setRowCount(min(100, len(self.df)))
            
            for i in range(min(100, len(self.df))):
                for j, col in enumerate(self.df.columns):
                    item = QTableWidgetItem(str(self.df.iloc[i, j]))
                    self.raw_table.setItem(i, j, item)
            
            self.statusBar().showMessage(f"Datos cargados: {len(self.df)} filas, {len(self.df.columns)} columnas")
    
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
        self.processed_table.setRowCount(min(100, len(df)))
        
        for i in range(min(100, len(df))):
            for j, col in enumerate(df.columns):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.processed_table.setItem(i, j, item)
        
        # Mostrar estadísticas
        self.display_statistics(df)
        
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage(f"Datos procesados: {len(df)} filas")
    
    def display_statistics(self, df):
        """Mostrar estadísticas de los datos procesados"""
        stats_text = "<b>Información del Conjunto de Datos</b><br><br>"
        stats_text += f"<b>Filas:</b> {len(df)}<br>"
        stats_text += f"<b>Columnas:</b> {len(df.columns)}<br><br>"
        
        stats_text += "<b>Campos detectados:</b><br>"
        for col in df.columns:
            try:
                numeric_df = pd.to_numeric(
                    df[col].astype(str).str.replace(',', '.'),
                    errors='coerce'
                )
                if numeric_df.notna().sum() > 0:
                    stats_text += f"<br><b>{col}</b><br>"
                    stats_text += f"&nbsp;&nbsp;Válidos: {numeric_df.notna().sum()}<br>"
                    stats_text += f"&nbsp;&nbsp;Mínimo: {numeric_df.min():.2f}<br>"
                    stats_text += f"&nbsp;&nbsp;Máximo: {numeric_df.max():.2f}<br>"
                    stats_text += f"&nbsp;&nbsp;Promedio: {numeric_df.mean():.2f}<br>"
            except:
                pass
        
        # Timestamp info
        if 'Timestamp_PC' in df.columns:
            stats_text += f"<br><b>Timestamp (primer registro):</b> {df['Timestamp_PC'].iloc[0]}<br>"
        
        self.stats_text.setText(stats_text)
    
    def export_data(self):
        """Exportar datos procesados"""
        if self.processed_df is None:
            QMessageBox.warning(self, "Advertencia", "Procese datos primero antes de exportar")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", "", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    self.processed_df.to_excel(file_path, index=False)
                else:
                    self.processed_df.to_csv(file_path, sep=';', index=False, decimal=',')
                
                QMessageBox.information(self, "Éxito", f"Archivo exportado: {Path(file_path).name}")
                self.statusBar().showMessage(f"Exportado: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar: {str(e)}")
    
    def handle_error(self, error_msg):
        """Manejar errores durante procesamiento"""
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Error de Procesamiento", error_msg)
        self.statusBar().showMessage("Error durante procesamiento")


def main():
    app = QApplication(sys.argv)
    window = DataProcessorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
