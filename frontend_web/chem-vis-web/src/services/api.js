import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const apiClient = axios.create({
    baseURL: `${process.env.REACT_APP_API_URL}/api`, 
    headers: {
        'Content-Type': 'application/json',
    },
});

apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    logout();
                    window.location.href = '/';
                    return Promise.reject(error);
                }
                const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/token/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);
                originalRequest.headers['Authorization'] = 'Bearer ' + access;
                
                return axios(originalRequest);
            } catch (refreshError) {
                console.error("Token refresh failed", refreshError);
                logout();
                window.location.href = '/'; 
                return Promise.reject(refreshError);
            }
        }
        return Promise.reject(error);
    }
);


const login = async (username, password) => {
    const response = await apiClient.post('/token/', { username, password });
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
};

const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

const isAuthenticated = () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        return false;
    }
    try {
        const decoded = jwtDecode(token);
        return decoded.exp > Date.now() / 1000;
    } catch (e) {
        return false;
    }
};

const getDatasets = () => {
    return apiClient.get('/datasets/');
};

const getDatasetData = (id) => {
    return apiClient.get(`/datasets/data/?id=${id}`);
};

const uploadDataset = (file) => {
    let formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/datasets/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

const downloadReport = (id) => {
    return apiClient.get(`/datasets/generate_report/?id=${id}`, {
        responseType: 'blob',
    });
};

export {
    login,
    logout,
    isAuthenticated,
    getDatasets,
    getDatasetData,
    uploadDataset,
    downloadReport,
};
