# Protein Data Pipeline with Apache Beam

This project leverages Apache Beam to create a scalable pipeline for processing protein data. It is designed to efficiently handle large datasets and can be extended to run on different backends like Google Cloud Dataflow, Apache Flink, and Apache Spark.

## Prerequisites
Before starting, make sure you have the following installed on your system:

- Python 3.12
- `pip` (Python package installer)
- Virtual environment package (`venv`)

#

## Step 1: Project Setup

### Clone the Repository
```bash
git clone https://github.com/FabrizioMarras/protein-data-pipeline.git
cd protein-data-pipeline
```
### Create a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows, use `venv\Scripts\activate`

## Step 2: Install Dependencies
Install Required Packages:
```bash
pip install -r requirements.txt
```

To verify if installation of all dependencies is correct, run:
```bash
pip list
```

You can also test the Apache Beam Installation: Run the `apache_beam.py` script to ensure everything is set up correctly:
```bash
python3 beam_test.py
```

If the setup is successful, you should see:
```bash
Hello
Apache
Beam
```

