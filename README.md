# Scuderia Ferrari Podium Predictor

This repository contains an automated MLOps pipeline for predicting Scuderia Ferrari podium finishes in Formula 1.

The project encompasses three main stages of the machine learning lifecycle, fully automated and containerized:
1. **Data Engineering:** Loading, cleaning, and preprocessing historical F1 data.
2. **Model Engineering:** Training a Random Forest classifier with hyperparameter tuning (GridSearchCV) and logging metrics using **MLflow**.
3. **Deployment:** Serving the model via a **FastAPI** backend and interacting with it through a **Streamlit** frontend, both running in separate **Docker** containers.

*Note: Stages 1 and 2 are orchestrated using Data Version Control to ensure reproducibility and efficient execution of the data pipeline.*

## Repository structure

```yaml
├── code
│   ├── datasets             
│   ├── deployment         
│   │   ├── api     
│   │   └── app
│   │   └── docker-compose.yml
│   └── models      
├── data
│   ├── processed 
│   └── raw
├── models                
├── notebooks          
├── requirements.txt  
├── dvc.yaml
├── dvc.lock
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

### 2. Start the complete automated MLOps workflow

```python run_pipeline.py```

Every pipeline cycle performs the following steps:

1. Run the DVC pipeline
   ↓
2. Process raw data
   ↓
3. Train and evaluate the model
   ↓
4. Save the updated model
   ↓
5. Build/start the Docker deployment
   ↓
6. Run FastAPI and Streamlit
   ↓
7. Reload the API with the latest trained model


## Accessing the application
Once the Docker containers are running, you can access the services via your web browser:

1. Streamlit web app: http://localhost:8501

2. FastAPI documentation: http://localhost:8000/docs

3. MLflow dashboard: Run ```mlflow ui --backend-store-uri sqlite:///mlflow.db``` locally and open http://127.0.0.1:5000          