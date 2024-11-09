import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
import os
from datetime import datetime
from ..db.db_connection import connect_to_db

# Function to fetch the latest PDB structure
def fetch_pdb_structure(protein_id):
    pdb_api_url = f'https://data.rcsb.org/rest/v1/core/search'
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_entity_source_organism.taxonomy_lineage.name",
                "operator": "exact_match",
                "value": protein_id
            }
        },
        "return_type": "entry",
        "request_options": {
            "pager": {
                "start": 0,
                "rows": 1
            },
            "sort": [
                {
                    "sort_by": "rcsb_accession_info.deposit_date",
                    "direction": "desc"
                }
            ]
        }
    }
    response = requests.post(pdb_api_url, json=query)
    if response.status_code == 200:
        data = response.json()
        if data['result_set']:
            pdb_id = data['result_set'][0]['identifier']
            pdb_file_url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
            pdb_response = requests.get(pdb_file_url)
            if pdb_response.status_code == 200:
                print(f'{pdb_id}', f'{pdb_file_url}')
                return pdb_id, pdb_response.text
    return None, None

# Function to fetch AlphaFold structure
def fetch_alphafold_structure(protein_id):
    alphafold_url = f'https://alphafold.ebi.ac.uk/files/AF-{protein_id}-F1-model_v1.pdb'
    response = requests.get(alphafold_url)
    if response.status_code == 200:
        return response.text
    return None

# Beam DoFn to process each protein
class FetchAndStoreStructureDoFn(beam.DoFn):
    def setup(self):
        # Establish the database connection
        self.connection = connect_to_db()
        if self.connection is None:
            raise Exception("Failed to connect to the database.")
        self.cursor = self.connection.cursor()

    def process(self, element):
        protein_id = element['protein_id']
        pdb_id, pdb_structure = fetch_pdb_structure(protein_id)
        if pdb_structure:
            filename = f'{protein_id}_{pdb_id}.pdb'
            source = 'PDB'
        else:
            pdb_structure = fetch_alphafold_structure(protein_id)
            if pdb_structure:
                filename = f'{protein_id}_AlphaFold.pdb'
                source = 'AlphaFold'
            else:
                yield {
                    'protein_id': protein_id,
                    'status': 'No structure found',
                    'file_path': None,
                    'source': None,
                    'download_date': None
                }
                return

        # Save the structure file locally
        output_dir = 'protein_structures'
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w') as f:
            f.write(pdb_structure)

        # Update the database
        update_query = '''
        UPDATE proteins
        SET structure_file_path = %s,
            source = %s,
            date_added = %s
        WHERE gene_name = %s;
        '''
        try:
            self.cursor.execute(update_query, (file_path, source, datetime.now(), protein_id))
            self.connection.commit()
            yield {
                'protein_id': protein_id,
                'status': 'Structure fetched and stored',
                'file_path': file_path,
                'source': source,
                'download_date': datetime.now().isoformat()
            }
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating structure for gene {protein_id}: {e}")

    def teardown(self):
        # Clean up the database connection
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'connection'):
            self.connection.close()

# Function to read protein IDs from the database
def read_protein_ids():
    connection = connect_to_db()
    if connection is None:
        raise Exception("Failed to connect to the database.")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT gene_name FROM proteins WHERE structure_file_path IS NULL;")
        results = cursor.fetchall()
        return [{'protein_id': row[0]} for row in results]
    except Exception as e:
        print(f"Error reading protein IDs: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def run_pipeline():
    options = PipelineOptions()
    with beam.Pipeline(options=options) as p:
        (p
         | 'Read Protein IDs' >> beam.Create(read_protein_ids())
         | 'Fetch and Store Structures' >> beam.ParDo(FetchAndStoreStructureDoFn())
         | 'Print Results' >> beam.Map(print)
        )

# if __name__ == '__main__':
#     run_pipeline()
