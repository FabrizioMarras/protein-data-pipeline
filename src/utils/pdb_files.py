import requests
from datetime import datetime
from typing import Optional, Tuple
from db.db_connection import connect_to_db

class ProteinStructurePipeline:
    def fetch_pdb_info(self, gene_name: str) -> Optional[Tuple[str, str, datetime]]:
        """
        Fetch PDB information for a given gene name.
        Returns tuple of (pdb_id, structure_url, release_date) if found, None otherwise.
        """
        query = """
        {
          entries(first: 10, filter: {molecule_names: "%s"}, orderBy: {field: RELEASE_DATE, direction: DESC}) {
            edges {
              node {
                rcsb_id
                rcsb_entry_info {
                  initial_release_date
                }
              }
            }
          }
        }
        """ % gene_name
        
        try:
            response = requests.post(
                'https://data.rcsb.org/graphql',
                json={'query': query}
            )
            data = response.json()
            
            if data['data']['entries']['edges']:
                # Get the first (most recent) entry
                entry = data['data']['entries']['edges'][0]['node']
                pdb_id = entry['rcsb_id']
                release_date = datetime.fromisoformat(
                    entry['rcsb_entry_info']['initial_release_date'].replace('Z', '+00:00')
                )
                # Store the direct URL to the PDB structure
                structure_url = f"https://files.rcsb.org/view/{pdb_id}.pdb"
                return pdb_id, structure_url, release_date
            return None
            
        except Exception as e:
            print(f"Error fetching PDB info for {gene_name}: {e}")
            return None

    def fetch_alphafold_url(self, gene_name: str) -> Optional[str]:
        """
        Get AlphaFold structure URL for a given gene name.
        Returns the URL if structure exists, None otherwise.
        """
        try:
            # This is a template URL - you might need to adjust it based on your specific gene naming convention
            structure_url = f"https://alphafold.ebi.ac.uk/entry/{gene_name}"
            
            # Verify if the entry exists
            response = requests.head(structure_url)
            if response.status_code == 200:
                return structure_url
            return None
        except Exception as e:
            print(f"Error fetching AlphaFold URL for {gene_name}: {e}")
            return None

    def update_database(self, gene_name: str, structure_url: str, source: str):
        """Update the database with structure URL information."""
        connection = connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            update_query = '''
            UPDATE proteins 
            SET structure_file_path = %s, source = %s 
            WHERE gene_name = %s;
            '''
            cursor.execute(update_query, (structure_url, source, gene_name))
            connection.commit()
            print(f"Updated structure information for {gene_name}")
        except Exception as e:
            print(f"Error updating database: {e}")
        finally:
            cursor.close()
            connection.close()

    def process_gene(self, gene_name: str):
        """Process a single gene to fetch and store its structure URL."""
        # First try PDB
        pdb_info = self.fetch_pdb_info(gene_name)
        if pdb_info:
            pdb_id, structure_url, _ = pdb_info
            self.update_database(gene_name, structure_url, f"PDB:{pdb_id}")
            return True

        # Fallback to AlphaFold
        alphafold_url = self.fetch_alphafold_url(gene_name)
        if alphafold_url:
            self.update_database(gene_name, alphafold_url, "AlphaFold")
            return True

        print(f"No structure found for {gene_name}")
        return False

    def process_all_genes(self):
        """Process all genes in the database."""
        connection = connect_to_db()
        if connection is None:
            print("Failed to connect to the database.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT gene_name FROM proteins WHERE structure_file_path IS NULL;")
            genes = cursor.fetchall()
            
            for (gene_name,) in genes:
                print(f"Processing {gene_name}...")
                self.process_gene(gene_name)
                
        except Exception as e:
            print(f"Error processing genes: {e}")
        finally:
            cursor.close()
            connection.close()

def main():
    pipeline = ProteinStructurePipeline()
    pipeline.process_all_genes()

if __name__ == "__main__":
    main()

    #
    # 
    # I'll break down the code and explain each part:

# Main Class and First Method:

# pythonCopyclass ProteinStructurePipeline:
#     def fetch_pdb_info(self, gene_name: str) -> Optional[Tuple[str, str, datetime]]:
# This class contains all the logic for fetching protein structures. The first method fetch_pdb_info tries to find a protein structure in the PDB database based on a gene name. It returns a tuple containing:

# pdb_id (string)
# structure_url (string)
# release_date (datetime)
# Or None if nothing is found.


# PDB GraphQL Query:

# pythonCopyquery = """
# {
#   entries(first: 10, filter: {molecule_names: "%s"}, orderBy: {field: RELEASE_DATE, direction: DESC}) {
#     edges {
#       node {
#         rcsb_id
#         rcsb_entry_info {
#           initial_release_date
#         }
#       }
#     }
#   }
# }
# """ % gene_name
# This is a GraphQL query to the PDB database that:

# Searches for entries matching the gene name
# Orders them by release date (newest first)
# Returns the first 10 matches
# For each match, gets the PDB ID and release date


# AlphaFold URL Method:

# pythonCopydef fetch_alphafold_url(self, gene_name: str) -> Optional[str]:
# This is a fallback method that runs if no PDB structure is found. It tries to construct an AlphaFold URL for the gene and checks if it exists.

# Database Update Method:

# pythonCopydef update_database(self, gene_name: str, structure_url: str, source: str):
# This method updates your database with:

# The URL to the structure (PDB or AlphaFold)
# The source of the structure (either "PDB:[id]" or "AlphaFold")
# Matches these to the gene name


# Single Gene Processing:

# pythonCopydef process_gene(self, gene_name: str):
# This method handles the full workflow for one gene:

# First tries to find a PDB structure
# If that fails, tries to find an AlphaFold structure
# Updates the database with whatever it finds
# Returns True if it found a structure, False if not
# Batch Processing:

# pythonCopydef process_all_genes(self):
# This method:

# Connects to your database
# Gets all genes that don't have a structure URL yet
# Processes each one using process_gene()
# Main Execution:

# pythonCopydef main():
#     pipeline = ProteinStructurePipeline()
#     pipeline.process_all_genes()

# if __name__ == "__main__":
#     main()
# This is the entry point that creates the pipeline and starts processing all genes.
# The overall workflow is:

# For each gene in your database:

# Try to find a PDB structure
# If none found, try to find an AlphaFold structure
# Store the URL to whichever structure was found
# Record the source of the structure



# A typical URL stored might look like:

# PDB: https://files.rcsb.org/view/1ABC.pdb (where 1ABC is the PDB ID)
# AlphaFold: https://alphafold.ebi.ac.uk/entry/GENENAME

# These URLs can then be used in your web application with the mol* viewer to display the 3D structures.
# Would you like me to explain any particular part in more detail? CopyRetryClaude does not have the ability to run the code it generates yet.