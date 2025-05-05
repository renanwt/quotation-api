# Quotation API 🌍💱

Quotation API is a **Django-based** application that provides currency quotation data and visualizations using Highcharts. It supports fetching and storing financial records for multiple currencies and offers endpoints for retrieving data in JSON format or as interactive charts.

## Features ✨
- 📊 Fetch and store currency quotations (USD, BRL, EUR, JPY).
- 🔍 Retrieve financial records with optional filters (date range, currency).
- 📈 Visualize currency trends using Highcharts.
- 🌐 RESTful API endpoints for integration with other applications.

## Installation 🛠️

### Prerequisites
- 🐍 Python 3.8+
- 🗄️ MySQL database
- 🌟 Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/quotation-api.git
   cd quotation-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Update your `settings.py` file with your MySQL database credentials.

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage 🚀

### Running the API Locally
Start the server and access the API at `http://127.0.0.1:8000`.

### Endpoints

#### Development Endpoints
- **[GET]** `http://127.0.0.1:8000/api/records/`
  - Query Params (optional):
    - `start_date`: e.g., `"2023-12-11"`
    - `end_date`: e.g., `"2023-12-10"`
    - `currency`: e.g., `"brl"`

- **[POST]** `http://127.0.0.1:8000/api/records/`
  - Request Body:
    ```json
    { "quotation_date": "2023-11-12" }
    ```

- **[GET]** `http://127.0.0.1:8000/api/chart`
  - Query Params (optional):
    - `start_date`: e.g., `"2023-12-11"`
    - `end_date`: e.g., `"2023-12-10"`
    - `currency`: e.g., `"brl"`

#### Production Endpoints
- **[GET, POST]** `https://quotation-api-iljn.onrender.com/api/records/`
- **[GET]** `https://quotation-api-iljn.onrender.com/api/chart`

### Visualizing Charts 📉
Access the chart visualization at `http://127.0.0.1:8000/api/chart` with optional query parameters for filtering.

### Populating Recent Data 📅
Run the `data_populating.py` script to fetch and store recent currency data. Update the date on line 22 of the script before running.

```bash
python data_populating.py
```

## Testing ✅
Run the test suite to ensure everything is working correctly:
```bash
python manage.py test app
```

## Contributing 🤝
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Postman Collection 📬
Use the provided Postman collection (`QuotationApi.postman_collection.json`) to test the API endpoints.

## Contact 📧
For questions or support, please contact Renan L. W. Teixeira.
