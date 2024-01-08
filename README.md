# Project : Box-office score prediction

**Course:** Scalable Machine Learning and Deep Learning - Project

**Team Limoncello**: Iga Pawlak, Julien Horvat

## 1. Description

This project is a serverless ML pipeline that creates models for upcoming box office performance predictions of recently released films. The model is trained on well selected features of past films and solving a regression problem tries to infer on the revenue of new films. The datasource we chose is the [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started), an online API giving a free access to a good amount of film description, frequently updated, and with performant and interesting query possibilities. One can get the access via an online formula. 

The pipeline uses Hopsworks for efficient storage (features and models), Huggingface web app for user interface, and Github Actions for workflows.

## 2. Structure and details

**2.3.1 **

**2.3.2 API keys**


talk about utils and the gestion of the API keys

### 2.1. Struture of the project 

At the center of the system is Hopsworks. It receives and store the features created in *movies_feature_pipeline.ipynb*, send them to *movies_training_pipeline.ipynb* and get back a trained model, interact with workflows and with Huggingface. The data are fetched from TMDB API in the feature pipeline. Data for is also fetched in the workflows for daily inference, and in Huggingface for details of movies.

This project involves different online services. Hopsworks and TMDB API both need API private keys 

### 2.2 Features selection and pipeline
c
### 2.3 Training pipeline

### 2.4 Workflows

### 2.5 HuggingFace app

### 2.6 Improvements

- features : transformer with overview to get context
- more data?
- Other models?
