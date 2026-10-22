# 🛡️ Network Security — Phishing Detection MLOps Project

An end-to-end Machine Learning project for phishing-related network classification, featuring a modular training pipeline, data validation, preprocessing, model training, and a FastAPI-based prediction service.

## 📌 Project Overview

Phishing is a cybersecurity threat that attempts to deceive users into interacting with malicious websites or disclosing sensitive information.

This project demonstrates a structured machine learning workflow for processing network-related data, training a classification model, and serving predictions through a REST API.

The architecture separates data ingestion, validation, transformation, model training, and inference to improve maintainability and support future MLOps enhancements.

## ✨ Key Features

- Modular end-to-end ML training pipeline
- Dataset ingestion and schema validation
- Data transformation and preprocessing
- Machine learning model training
- Model and preprocessor artifact persistence
- FastAPI prediction endpoint
- CSV upload for batch predictions
- Prediction results exported to CSV
- MongoDB integration for data ingestion
- Logging and custom exception handling
- Environment-based configuration for sensitive settings

## 🧰 Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| API Framework | FastAPI |
| API Server | Uvicorn |
| Database | MongoDB |
| Configuration | Python-dotenv |
| Model Persistence | Pickle-based serialization |
| Version Control | Git, GitHub |

## 🏗️ Project Structure

```text
NetworkSecurity/
├── app.py
├── main.py
├── requirements.txt
├── setup.py
├── .gitignore
│
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline/
│   │   └── training_pipeline.py
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── utils/
│   └── constant/
│
├── Network_Data/
│   └── phisingData.csv
│
├── README.md
└── ...
```

*Generated artifacts, credentials, and local environment files should remain excluded from version control.*

## 🔄 ML Pipeline Workflow

1. **Data Ingestion:** Loads the dataset from the configured source.
2. **Data Validation:** Checks the expected dataset structure and feature columns.
3. **Data Transformation:** Prepares features and applies preprocessing.
4. **Model Training:** Trains and evaluates the configured classification model.
5. **Artifact Persistence:** Saves the trained model and preprocessing object.
6. **API Inference:** Accepts CSV files through the FastAPI prediction endpoint.
7. **Output Generation:** Produces predictions and exports results to CSV.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd NetworkSecurity
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Use a Python version compatible with the dependencies specified in `requirements.txt`.

## 🔐 Environment Configuration

Create a local `.env` file in the project root if MongoDB integration is required.

```dotenv
MONGODB_URL_KEY=your_mongodb_connection_string
MONGO_DB_URL=your_mongodb_connection_string
```

Replace these placeholders with your own connection string and credentials.

**Security best practices:**

- Never commit `.env` or real credentials to GitHub.
- Keep database passwords and API tokens out of source code.
- Rotate credentials if they have previously been exposed.
- Ensure `.env` is excluded through `.gitignore`.

## 🚀 Run the Training Pipeline

From the project root, execute:

```bash
python main.py
```

Wait for the pipeline to finish successfully and verify that the expected model and preprocessing artifacts have been generated.

If the configured ingestion process requires MongoDB, configure the database connection before training.

## 🌐 Run the FastAPI Application

Start the API server:

```bash
uvicorn app:app --reload
```

Open the interactive API documentation:

**http://127.0.0.1:8000/docs**

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Redirects to API documentation |
| GET | `/train` | Executes the training pipeline |
| POST | `/predict` | Accepts a CSV upload and returns prediction results |

Endpoint behavior is defined by the application implementation.

## 🧪 Make Predictions

1. Start the FastAPI server.
2. Open `/docs` in your browser.
3. Expand `POST /predict`.
4. Click **Try it out**.
5. Upload a CSV containing the expected model input features.
6. Click **Execute**.
7. Inspect the response and generated prediction output.

### Input Requirements

- The CSV must contain the feature columns expected by the fitted preprocessor.
- Feature names and data types must match the training pipeline.
- If `Result` is the target column, it should not be included as a prediction feature.
- Missing or unexpected columns may cause validation errors.

### Prediction Output

The application can save prediction results to:

```text
prediction_output/output.csv
```

The output includes a `predicted_column` containing the model's predictions.

Interpretation of each predicted class should be confirmed against the dataset and training configuration.

## 📊 Model Evaluation

For classification tasks, evaluate the model using suitable metrics:

- Precision
- Recall
- F1-score
- Confusion matrix
- ROC-AUC, where appropriate

Accuracy alone may be insufficient for imbalanced datasets. Add measured results from an actual training run before publishing performance claims.

## 🔒 Security Considerations

- Store credentials in environment variables.
- Exclude secrets and local configuration files from version control.
- Validate uploaded files before processing them.
- Avoid logging credentials or sensitive input data.
- Restrict access to training endpoints in deployed environments.
- Treat serialized model files as trusted artifacts only.

## 🚧 Future Improvements

Potential enhancements for a more production-oriented MLOps workflow:

- Unit and API tests using Pytest
- Continuous integration with GitHub Actions
- Docker-based packaging and deployment
- Experiment tracking using MLflow
- Dataset and model versioning
- Automated model evaluation reports
- Data drift and model performance monitoring
- Cloud deployment and controlled API access
- Structured application metrics and health checks

These improvements should be marked as completed only after implementation and testing.

## ⚠️ Disclaimer

This project is intended for educational and research purposes. Model predictions depend on training data, feature quality, and evaluation methodology. The system should not be used as a standalone cybersecurity defense without independent validation and additional security controls.

## 👨‍💻 Author

**Krish Naik**

This project is based on the Network Security MLOps project taught by Krish Naik.

