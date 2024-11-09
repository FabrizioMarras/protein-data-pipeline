# Protein Data Pipeline with Apache Beam

This project leverages Apache Beam to create a scalable pipeline for processing protein data. It is designed to efficiently handle large datasets and can be extended to run on different backends like Google Cloud Dataflow, Apache Flink, and Apache Spark.

## Prerequisites
Before starting, make sure you have the following installed on your system:

- Python 3.12
- `pip` (Python package installer)
- Virtual environment package (`venv`)

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

### Step 3: Create a Cloud-based SQL Database

This step involves setting up a cloud-based PostgreSQL database and connecting to it using Python.

1. **Create a PostgreSQL Database**:
- Use Google Cloud Platform (or your preferred cloud provider) to create a PostgreSQL database.
- Database Name: `protein_data`
- Allow connections from your local IP for testing.

2. **Set Up Environment Variables**:
Create a `.env` file in the project root:
```bash
DB_HOST=<your-database-host>
DB_PORT=5432
DB_NAME=protein_data
DB_USER=<your-username>
DB_PASSWORD=<your-password>
```

3. **Connecting to the Database**:
- The `db_connection.py` script handles the connection using `psycopg2`.
- Run `python3 db_connection.py` to verify the connection.
If successful you should read `Successfully connected to the database!` in the console.

**Note**: Make sure to exclude the `.env` file from version control by adding it to `.gitignore`.

### Step 4: Set up Auth
