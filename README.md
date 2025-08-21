# stock-data-pipeline

This project automates the process of fetching stock market data and processing
it using Python and Airflow. The pipeline is fully containerized using Docker.

## Features
- Fetches stock data from Alpha Vantage API
- Scheduled DAGs in Airflow
- Data storage and processing scripts
- Containerized with Docker

## Installation
1. Copy .env.template to .env and add your API key.
2. Build Docker images: docker-compose build
3. Start the services: docker-compose up -d
4. Access Airflow UI at http://localhost:8080

# Project Structure

stock-data-pipeline/
├── docker-compose.yml
├── Dockerfile
├── .env.template
├── dags/
│   └── stock_pipeline.py
└── scripts/
    └── fetch_stock_data.py
