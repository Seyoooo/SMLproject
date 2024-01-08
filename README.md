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

At the center of the system is Hopsworks. It receives and stores the features created in *movies_feature_pipeline.ipynb*, sends them to *movies_training_pipeline.ipynb* and get back a trained model, interacts with workflows and with Huggingface. The offline dataset is fetched from TMDB API in the feature pipeline. Data is also fetched in the workflows for daily inference, and from Huggingface for details of movies.

This project involves different online services. In the code, we need API private keys to access Hopsworks and TMDB API. We added them as secret keys on Github for the workflows, and you will not have access to them on the repository. If you want to run this code, you should either ask us the keys or create your owns. 

For clarity, all functions basic functions and functions for feature extraction and TMDB API interactions are coded in *utils.py*.

### 2.2 Features selection and pipeline

TMDB API has some interesting pre-computed features : vote_average of the movie on their website and popularity.

### 2.3 Training pipeline

### 2.4 Workflows

### 2.5 HuggingFace app

### 2.6 Improvements

- features : transformer with overview to get context
- more data?
- Other models?
