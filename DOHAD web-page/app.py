from flask import Flask, request, render_template
from py2neo import Graph
import pandas as pd

app = Flask(__name__)

# Conexión a la base de datos Neo4j
graph = Graph("neo4j+s://60b05b36.databases.neo4j.io", auth=("neo4j", "YgmAkA0V0mcizKeKc63YLjWLLfXh-AexHRy5YzXGS90"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    keywords = request.form.get('keywords')
    sort_by = request.form.get('sort_by', 'score')

    if not keywords:
        return render_template('index.html', error="Please enter some keywords.")
    
    node_names = [keyword.strip() for keyword in keywords.split(',')]

    # Consulta única a Neo4j
    query = """
    MATCH (paper:Paper)-[r:MENTIONS|AUTHORED|SIMILAR_TO|PUBLISHED_IN|CO_CONCURRENCE]->(n)
    WHERE n.name IN $node_names
    RETURN paper.name AS title, paper.doi AS doi, paper.publication_date AS publication_date, SUM(r.tfidf_value) AS total_score, paper.cites AS cites
    """
    result = graph.run(query, node_names=node_names).to_data_frame()

    if not result.empty:
        # Convertir 'publication_date' a tipo de dato fecha
        result['publication_date'] = pd.to_datetime(result['publication_date'], errors='coerce', format='%d-%m-%Y')

        # Limitar a los top 10 antes de calcular el porcentaje
        result = result.nlargest(10, 'total_score')

        # Asegurarse de que 'total_score' no tenga valores nulos
        result['total_score'] = pd.to_numeric(result['total_score'], errors='coerce')
        result = result.dropna(subset=['total_score'])

        # Calcular el total de los scores
        total_score_sum = result['total_score'].sum()

        if total_score_sum > 0:
            # Calcular el porcentaje para cada paper
            result['normalized_score'] = (result['total_score'] / total_score_sum * 100).round(2)
        else:
            result['normalized_score'] = 0

        # Ordenar según la preferencia del usuario
        if sort_by == 'publication_date':
            result = result.sort_values(by='publication_date', ascending=False)
        elif sort_by == 'cites':
            result = result.sort_values(by='cites', ascending=False)
        else:
            result = result.sort_values(by='total_score', ascending=False)

    return render_template('results.html', papers=result.to_dict('records'), keywords=keywords, sort_by=sort_by)

if __name__ == "__main__":
    app.run(debug=True)