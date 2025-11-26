# Excel File Comparator

A Python application that compares two Excel files and displays the differences using a Streamlit interface.

## Features

- Upload and compare two Excel files (.xlsx, .xls)
- View column differences (columns unique to each file)
- View value differences in a detailed table
- Summary statistics showing total rows and differences

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bastien-OC20/comparator.git
cd comparator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Then open your browser to the URL shown (typically http://localhost:8501) and upload two Excel files to compare.

## How it works

The comparator:
1. Loads both Excel files
2. Identifies columns unique to each file
3. Compares values in common columns row by row
4. Displays a summary with metrics and a detailed table of differences
