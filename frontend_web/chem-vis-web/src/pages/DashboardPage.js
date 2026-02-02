import React, { useState, useEffect } from 'react';
import { Button, Container, ListGroup, Card, Row, Col, Alert } from 'react-bootstrap';
import { logout, getDatasets, getDatasetData, downloadReport } from '../services/api';
import UploadForm from '../components/UploadForm';
import DatasetTable from '../components/DatasetTable';
import SummaryCharts from '../components/SummaryCharts';

const DashboardPage = ({ onLogout }) => {
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState(null);
    const [datasetData, setDatasetData] = useState(null);
    const [error, setError] = useState('');

    const fetchDatasets = async () => {
        try {
            const response = await getDatasets();
            setDatasets(response.data);
        } catch (err) {
            setError('Could not fetch recent datasets.');
            console.error(err);
        }
    };

    useEffect(() => {
        fetchDatasets();
    }, []);

    const handleLogout = () => {
        logout();
        onLogout();
    };

    const handleDatasetSelect = async (dataset) => {
        // Clear previous data and errors
        setDatasetData(null);
        setError('');
        setSelectedDataset(dataset);

        try {
            const response = await getDatasetData(dataset.id);
            setDatasetData(response.data);
        } catch (err) {
            setError(`Failed to fetch data for ${dataset.name}. Please check the console for details.`);
            console.error(err);
        }
    };
    
    const handleReportDownload = async () => {
        try {
            const response = await downloadReport(selectedDataset.id);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${selectedDataset.name}_report.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            setError('Failed to download report.');
            console.error(err);
        }
    };

    return (
        <Container>
            <div className="d-flex justify-content-between align-items-center mt-3 mb-3">
                <h1>Dashboard</h1>
                <Button variant="primary" onClick={handleLogout}>
                    Logout
                </Button>
            </div>
            
            <UploadForm onUpload={fetchDatasets} />

            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

            <Row className="mt-4">
                <Col md={4}>
                    <h2>Recent Datasets</h2>
                    <ListGroup>
                        {datasets.map((dataset) => (
                            <ListGroup.Item 
                                key={dataset.id} 
                                action 
                                onClick={() => handleDatasetSelect(dataset)}
                                active={selectedDataset && selectedDataset.id === dataset.id}
                            >
                                {dataset.name} - {new Date(dataset.uploaded_at).toLocaleString()}
                            </ListGroup.Item>
                        ))}
                    </ListGroup>
                </Col>
                <Col md={8}>
                    {selectedDataset && (
                        <Card>
                            <Card.Header>
                                <div className="d-flex justify-content-between align-items-center">
                                    <h3>{selectedDataset.name}</h3>
                                    <Button variant="secondary" onClick={handleReportDownload} disabled={!selectedDataset}>Download Report</Button>
                                </div>
                            </Card.Header>
                            <Card.Body>
                                <Card.Title>Summary</Card.Title>
                                <ul>
                                    <li>Total Count: {selectedDataset.summary.total_count}</li>
                                    <li>Avg Flowrate: {selectedDataset.summary.averages.Flowrate.toFixed(2)}</li>
                                    <li>Avg Pressure: {selectedDataset.summary.averages.Pressure.toFixed(2)}</li>
                                    <li>Avg Temperature: {selectedDataset.summary.averages.Temperature.toFixed(2)}</li>
                                </ul>
                                <hr/>
                                <SummaryCharts summary={selectedDataset.summary} />
                                <hr/>
                                <Card.Title>Data</Card.Title>
                                <DatasetTable data={datasetData} />
                            </Card.Body>
                        </Card>
                    )}
                </Col>
            </Row>
        </Container>
    );
};

export default DashboardPage;