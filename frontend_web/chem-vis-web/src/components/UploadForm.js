import React, { useState } from 'react';
import { uploadDataset } from '../services/api';
import { Form, Button, Alert } from 'react-bootstrap';

const UploadForm = ({ onUpload }) => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError('Please select a file to upload.');
            return;
        }
        try {
            await uploadDataset(file);
            setSuccess('File uploaded successfully!');
            setError('');
            onUpload(); // Callback to refresh dataset list
        } catch (err) {
            setError('Error uploading file.');
            setSuccess('');
        }
    };

    return (
        <div>
            <h2>Upload CSV</h2>
            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}
            <Form onSubmit={handleSubmit}>
                <Form.Group>
                    <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button variant="primary" type="submit" style={{ marginTop: '10px' }}>
                    Upload
                </Button>
            </Form>
        </div>
    );
};

export default UploadForm;
