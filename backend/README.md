# Chemical Equipment Parameter Visualizer - Backend

This is the Django backend for the Hybrid Web + Desktop Application. It provides a REST API for uploading CSV data, retrieving analysis, and generating reports.

## Setup

1.  **Prerequisites:**
    *   Python 3.8+
    *   Pip

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```
    (Follow the prompts to create an admin user)

7.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The backend will be running at `http://127.0.0.1:8000/`.

## API Endpoints

*   **Admin Panel:** `/admin/`
*   **Authentication:**
    *   `POST /api/token/`: Obtain JWT token pair (username, password).
    *   `POST /api/token/refresh/`: Refresh JWT access token.
*   **Datasets:**
    *   `GET /api/datasets/`: List the 5 most recent datasets.
    *   `POST /api/datasets/`: Upload a new CSV file. (Requires authentication)
    *   `GET /api/datasets/{id}/`: Retrieve summary for a specific dataset. (Requires authentication)
    *   `GET /api/datasets/{id}/data/`: Retrieve full data for a specific dataset. (Requires authentication)
    *   `GET /api/datasets/{id}/generate_report/`: Download a PDF report for a dataset. (Requires authentication)

## Generating requirements.txt

To generate the `requirements.txt` file, run:
```bash
pip freeze > requirements.txt
```
