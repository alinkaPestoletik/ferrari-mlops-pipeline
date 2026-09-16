# Scuderia Ferrari Podium Predictor

This repository contains an automated MLOps pipeline for predicting Scuderia Ferrari podium finishes in Formula 1.

The project encompasses three main stages of the machine learning lifecycle, fully automated and containerized:
1. **Data Engineering:** Loading, cleaning, and preprocessing historical F1 data.
2. **Model Engineering:** Training a Random Forest classifier and logging metrics using MLflow.
3. **Deployment:** Serving the model via a **FastAPI** backend and interacting with it through a **Streamlit** frontend, both running in separate **Docker** containers.

## Repository structure

```yaml
├── code
│   ├── datasets             
│   ├── deployment         
│   │   ├── api     
│   │   └── app
│   └── models      
├── data
│   ├── processed 
│   └── raw
├── models                
├── notebooks          
├── requirements.txt   
├── run_pipeline.py  
└── README.md
```

## Prerequisites
Before running the pipeline, ensure you have the following installed:

1. Python 3.9+
2. Docker Desktop

## How to run the project
### 1. Setup the environment

Clone the repository and install the required dependencies:

```Bash
git clone <your-repository-url>
cd <your-repository-name>

python -m venv venv
# On Windows: venv\Scripts\activate
# On Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
```

### 2. Start the deployment services
The API and Streamlit application must run in separate Docker containers. To build and start them, navigate to the deployment folder:

```Bash
cd code/deployment
docker compose up --build -d
```

### 3. Run the automated pipeline
To automate the data processing, model training, and model reloading, run the orchestrator script from the root directory in a new terminal window:

```Bash
python run_pipeline.py
```
This script will execute all three stages and automatically re-run the pipeline every 5 minutes. The FastAPI container is configured with Docker Volumes to automatically pick up the newly trained model.pkl upon restart.

## Accessing the application
Once the Docker containers are running, you can access the services via your web browser:

1. Streamlit web app: http://localhost:8501

2. FastAPI documentation: http://localhost:8000/docs

3. MLflow dashboard: Run ```mlflow ui --backend-store-uri sqlite:///mlflow.db``` locally and open http://127.0.0.1:5000          