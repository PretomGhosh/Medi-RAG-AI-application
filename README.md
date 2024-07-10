## Medi RAG AI Application ##
Medi RAG is a Retrieval-Augmented Generation (RAG) AI application designed to answer questions about canine dental diseases. It leverages the power of Large Language Models (LLMs) to process, summarize, and store information from various sources, providing accurate and detailed responses to user queries.

## Table of Contents
Overview
Features
Technologies Used
Installation
Usage
Contributing
License
Acknowledgments

## Overview
Medi RAG processes information from a PDF document on canine periodontal disease, including text, tables, and images. It stores this information in a vector store and retrieves relevant data to answer user queries using a web-based interface. The application is designed to improve information dissemination for veterinarians and pet owners.

## Features
--> Extracts text, tables, and images from PDF documents.

--> Summarizes extracted content using GPT-3.5-turbo.

--> Stores summarized content in a FAISS vector store.

--> Retrieves relevant documents and generates responses using GPT-4.

--> Interactive web interface for querying and displaying answers.

## Technologies Used
Python
Langchain
GPT-3.5-turbo and GPT-4
FAISS
FastAPI
HTML, CSS, JavaScript

## Installation

--> Prerequisites
Python 3.7 or higher
Virtual environment (optional but recommended)

## Steps
1) Create a virtual environment and activate it:
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

2) Install the required packages:
pip install -r requirements.txt

3) Install additional system dependencies:
sudo apt install tesseract-ocr libtesseract-dev poppler-utils

4) Usage
Start the FastAPI server:
uvicorn app1:app --reload

5) Open your web browser and go to:
http://127.0.0.1:8001
Enter your query in the provided text box and get detailed answers about canine dental diseases.

## Contribution to the project
Contributions are welcome! Please follow these steps:

--> Fork the repository.

--> Create a new branch:

git checkout -b feature-branch

--> Make your changes and commit them:

git commit -m "Description of your changes"

--> Push to the branch:

git push origin feature-branch

--> Open a pull request on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Special thanks to the developers and the community who contributed to the libraries and tools used in this project.


