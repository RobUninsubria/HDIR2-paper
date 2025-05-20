
from rdflib import Graph

# Carica il file RDF
g = Graph()
g.parse("ntp_amplification_O6_risk_feedback.ttl", format="ttl")

# Esegui la query SPARQL
query = '''
PREFIX ntp: <http://example.org/ntp#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?packet ?riskScore
WHERE {
  ?packet a ntp:Packet ;
          ntp:hasRiskScore ?riskScore ;
          ntp:underMitigation "true"^^xsd:boolean .
}
ORDER BY DESC(?riskScore)
'''

# Esegui e stampa i risultati
results = g.query(query)
for row in results:
    print(f"Packet: {row.packet}, Risk Score: {row.riskScore}")
