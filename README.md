# Q&A PDF Splitter & Merger

An AI-powered document processing application that extracts questions and answers from PDF files, separates them into structured outputs, and generates independent question and answer documents.

## Features

* Extract text from PDF documents
* Detect numbered questions and corresponding answers
* Separate questions and answers automatically
* Generate dedicated Question and Answer files
* FastAPI backend for document processing
* Modular architecture for future AI and OCR enhancements
* Support for structured educational and assessment PDFs

## Tech Stack

* Python
* FastAPI
* PyMuPDF
* Regular Expressions (Regex)
* Git & GitHub

## Current Workflow

```text
PDF Upload
    ↓
Text Extraction
    ↓
Question-Answer Detection
    ↓
Question Separation
    ↓
Answer Separation
    ↓
Output Generation
```

## Project Structure

```text
backend/
├── app/
│   ├── main.py
│   └── services/
│       ├── pdf_reader.py
│       └── qa_parser.py
├── local_samples/
├── requirements.txt
└── run_extraction.py
```

## Future Enhancements

* PDF generation for separated outputs
* PDF merge functionality
* Frontend dashboard
* OCR support for scanned PDFs
* Multiple question-answer format support
* AI-assisted document validation
* Cloud deployment

## Learning Outcomes

Through this project, I gained hands-on experience with:

* FastAPI backend development
* PDF processing and text extraction
* Regex-based text parsing
* Modular Python application design
* File handling and automation
* Git and GitHub workflow

## Author

Akash Dubey
