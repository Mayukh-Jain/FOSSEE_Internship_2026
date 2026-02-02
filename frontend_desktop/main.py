import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QMessageBox, QListWidget, QFileDialog, QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox)
import api_client
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(300, 200) # Increase window size
        self.layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login')

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if api_client.login(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.layout = QGridLayout()

        # Left panel
        self.upload_button = QPushButton('Upload CSV')
        self.dataset_list = QListWidget()
        
        left_panel_layout = QVBoxLayout()
        left_panel_layout.addWidget(self.upload_button)
        left_panel_layout.addWidget(QLabel("Recent Datasets:"))
        left_panel_layout.addWidget(self.dataset_list)

        # Right panel - Top (Summary and Chart)
        right_top_layout = QHBoxLayout()

        # Summary Group
        summary_group = QGroupBox("Data Summary")
        summary_layout = QVBoxLayout()
        self.summary_total_label = QLabel("Total Count: N/A")
        self.summary_flowrate_label = QLabel("Avg Flowrate: N/A")
        self.summary_pressure_label = QLabel("Avg Pressure: N/A")
        self.summary_temp_label = QLabel("Avg Temperature: N/A")
        summary_layout.addWidget(self.summary_total_label)
        summary_layout.addWidget(self.summary_flowrate_label)
        summary_layout.addWidget(self.summary_pressure_label)
        summary_layout.addWidget(self.summary_temp_label)
        summary_group.setLayout(summary_layout)

        # Chart
        self.chart = FigureCanvas(Figure())

        right_top_layout.addWidget(summary_group)
        right_top_layout.addWidget(self.chart)

        # Right panel - Bottom (Table and Button)
        self.table = QTableWidget()
        self.download_report_button = QPushButton("Download Report")

        # Main Layout Assembly
        self.layout.addLayout(left_panel_layout, 0, 0)
        self.layout.addLayout(right_top_layout, 0, 1)
        self.layout.addWidget(self.table, 1, 0, 1, 2)
        self.layout.addWidget(self.download_report_button, 2, 0, 1, 2)

        self.setLayout(self.layout)

        self.upload_button.clicked.connect(self.upload_file)
        self.dataset_list.itemClicked.connect(self.dataset_selected)
        self.download_report_button.clicked.connect(self.download_report)

        self.load_datasets()

    def load_datasets(self):
        self.dataset_list.clear()
        datasets = api_client.get_datasets()
        if datasets:
            for ds in datasets:
                self.dataset_list.addItem(f"{ds['name']} ({ds['id']})")
        self.datasets = datasets

    def upload_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if filepath:
            if api_client.upload_dataset(filepath):
                self.load_datasets()
                QMessageBox.information(self, 'Success', 'File uploaded successfully.')
            else:
                QMessageBox.warning(self, 'Upload Failed', 'Could not upload file.')

    def dataset_selected(self, item):
        dataset_id = int(item.text().split('(')[-1][:-1])
        self.selected_dataset_id = dataset_id
        
        data = api_client.get_dataset_data(dataset_id)
        if data:
            self.table.setRowCount(len(data))
            if len(data) > 0:
                self.table.setColumnCount(len(data[0]))
                self.table.setHorizontalHeaderLabels(data[0].keys())
                for i, row in enumerate(data):
                    for j, (key, val) in enumerate(row.items()):
                        self.table.setItem(i, j, QTableWidgetItem(str(val)))

        dataset = next((ds for ds in self.datasets if ds['id'] == dataset_id), None)
        if dataset and 'summary' in dataset:
            summary = dataset['summary']
            
            # Update Summary Labels
            self.summary_total_label.setText(f"Total Count: {summary['total_count']}")
            self.summary_flowrate_label.setText(f"Avg Flowrate: {summary['averages']['Flowrate']:.2f}")
            self.summary_pressure_label.setText(f"Avg Pressure: {summary['averages']['Pressure']:.2f}")
            self.summary_temp_label.setText(f"Avg Temperature: {summary['averages']['Temperature']:.2f}")

            # Update Chart
            type_dist = summary['type_distribution']
            labels = type_dist.keys()
            sizes = type_dist.values()

            self.chart.figure.clear()
            ax = self.chart.figure.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title('Equipment Type Distribution')
            self.chart.draw()

    def download_report(self):
        if hasattr(self, 'selected_dataset_id'):
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"report_{self.selected_dataset_id}.pdf", "PDF Files (*.pdf)")
            if save_path:
                if api_client.download_report(self.selected_dataset_id, save_path):
                    QMessageBox.information(self, 'Success', 'Report downloaded successfully.')
                else:
                    QMessageBox.warning(self, 'Download Failed', 'Could not download report.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.resize(1200, 800)
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)