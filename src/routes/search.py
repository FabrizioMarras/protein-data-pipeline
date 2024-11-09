from flask import Blueprint, request, jsonify, render_template
from src.db.db_connection import connect_to_db
from src.utils.md_to_html import convert_markdown_to_html
from src.utils.fix_md_ref import fix_markdown_references

search_blueprint = Blueprint('search', __name__)

@search_blueprint.route('/search', methods=['GET'])
def search_protein():
    gene_name = request.args.get('gene_name')
    if not gene_name:
        return render_template('index.html', error="Please provide a gene_name parameter")

    connection = connect_to_db()
    if connection is None:
        return render_template('index.html', error="Failed to connect to the database")

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT content, structure_file_path FROM proteins WHERE gene_name = %s", (gene_name,))
        result = cursor.fetchone()
        if result:
            markdown_content = result[0]
            structure_file_path = result[1] if result[1] else None

            # Debugging: Print out the structure_file_path to check its value
            print(f"Structure file path for {gene_name}: {structure_file_path}")
            
            # Fix references and convert to HTML
            fixed_content = fix_markdown_references(markdown_content)
            html_content = convert_markdown_to_html(fixed_content)
            
            return render_template(
                'index.html', 
                content=html_content, 
                structure_url=structure_file_path, 
                gene_name=gene_name)
        else:
            return render_template('index.html', error="Gene not found", gene_name=gene_name)
    except Exception as e:
        return render_template('index.html', error=str(e), gene_name=gene_name)
    finally:
        cursor.close()
        connection.close()

@search_blueprint.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')
    if not term:
        return jsonify([])

    connection = connect_to_db()
    if connection is None:
        return jsonify([])

    cursor = connection.cursor()
    try:
        # Use parameterized queries to prevent SQL injection
        cursor.execute("SELECT gene_name FROM proteins WHERE gene_name LIKE %s LIMIT 10", (term + '%',))
        results = cursor.fetchall()
        suggestions = [row[0] for row in results]
        return jsonify(suggestions)
    except Exception as e:
        return jsonify([])
    finally:
        cursor.close()
        connection.close()