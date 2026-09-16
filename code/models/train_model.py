import pandas as pd
import mlflow
import mlflow.sklearn
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score


def train_and_log():
    train_data = pd.read_csv('data/processed/train.csv')
    test_data = pd.read_csv('data/processed/test.csv')

    X_train = train_data.drop('target', axis=1)
    y_train = train_data['target']
    X_test = test_data.drop('target', axis=1)
    y_test = test_data['target']

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("Ferrari_Podium_Prediction")

    with mlflow.start_run():
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['driverRef'])
            ],
            remainder='passthrough'
        )
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42))
        ])

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"Metrics - Accuracy: {acc:.4f}, F1-score: {f1:.4f}")

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")
        print("Success")


if __name__ == "__main__":
    train_and_log()