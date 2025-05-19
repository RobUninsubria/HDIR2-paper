
import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import XSD

# === CONFIG ===
SCORES_CSV = "arnn_output_scores.csv"
FEATURES_CSV = "o3_vectorized_dao_dio.csv"
RDF_OUTPUT = "dao_dio_risk_injected.ttl"
RISK_PREDICATE = "hasRiskScore"

# === NAMESPACE ===
IOT = Namespace("http://example.org/iot/")

# === GRAFO RDF ===
g = Graph()
g.bind("iot", IOT)

# === DATI ===
scores_df = pd.read_csv(SCORES_CSV)
features_df = pd.read_csv(FEATURES_CSV)
scores_df["node_id"] = features_df["node_id"].values

# === INSERIMENTO TRIPLE RDF ===
for _, row in scores_df.iterrows():
    node_uri = IOT[f"Node_{int(row['node_id'])}"]
    risk_literal = Literal(round(float(row["risk_score"]), 4), datatype=XSD.float)
    g.add((node_uri, IOT[RISK_PREDICATE], risk_literal))

# === SALVA RDF ===
g.serialize(destination=RDF_OUTPUT, format="turtle")
print(f"✅ RDF salvato in: {RDF_OUTPUT}")
