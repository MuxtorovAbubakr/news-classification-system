# News Classification System

A machine learning project for classifying news articles into four categories:
- World
- Sports
- Business
- Sci/Tech

This project combines data exploration, baseline modeling, a feedforward neural network, and a simple web-based inference system for a news article classification model.

## Overview

The system is built around the AG News dataset and uses text preprocessing with TF-IDF features to train and serve a news article classifier. It includes:

- Data exploration notebooks
- A logistic regression baseline
- A PyTorch feedforward neural network
- A FastAPI prediction API
- A Streamlit frontend for interactive use
- Docker configuration for local deployment

## Highlights

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | 91.39% |
| PyTorch FNN | 91.96% |

The best-performing model in this project is the PyTorch feedforward neural network, outperforming the logistic regression baseline by 0.57 percentage points on the test set.

## Architecture

The application follows a simple client-server architecture:

1. The user enters an article in the Streamlit frontend.
2. Streamlit sends a POST request to the FastAPI API with the article text.
3. FastAPI validates the input and calls `predict_category()` from the model inference pipeline.
4. The pipeline:
   - cleans the raw text,
   - transforms it with the saved TF-IDF vectorizer,
   - passes the feature vector to the trained PyTorch model,
   - returns the predicted category.
5. The result is displayed in the Streamlit UI.

This keeps the model logic separate from the user interface and makes the prediction pipeline easy to reuse in other applications.

## Dataset

The project uses the AG News dataset, a widely used text classification benchmark with four topic categories:
- World
- Sports
- Business
- Sci/Tech

The dataset was split as follows:
- Original AG News training set: 120,000 examples
- Train/dev split: 80/20 of the training data
  - Train: 96,000 articles
  - Development: 24,000 articles
- Test set: 7,600 articles, kept untouched for final evaluation

This setup allows for reliable model selection and performance comparison without leaking test-set information into training.

## Experiments and Results

Two main models were evaluated:

### 1. Logistic Regression
A TF-IDF + Logistic Regression baseline was trained first. It achieved:
- Test accuracy: 91.39%

This served as a strong baseline and helped confirm the task was well suited for text-based classification.

### 2. PyTorch Feedforward Neural Network
A shallow feedforward neural network was trained on the same TF-IDF features. It achieved:
- Test accuracy: 91.96%

This outperformed the logistic regression model and provided the strongest final result in the project.

### Summary
The FNN slightly outperformed the logistic regression baseline, while still being compact and easy to deploy. The project also explored preprocessing and model-training choices such as HTML-artifact cleanup and early stopping to reduce overfitting.

## Project Structure

```text
news-classification-system/
├── api/
│   ├── __init__.py
│   └── main.py
├── app/
│   └── streamlit_app.py
├── models/
│   ├── fnn_weights.pth
│   └── tfidf_vectorizer.joblib
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_model.ipynb
│   └── 03_pytorch_fnn.ipynb
├── src/
│   ├── __init__.py
│   ├── inference.py
│   ├── models.py
│   └── preprocessing.py
├── .dockerignore
├── .gitignore
├── Dockerfile.api
├── Dockerfile.app
├── compose.yaml
├── README.md
├── requirements.txt
├── requirements-api.txt
├── requirements-app.txt