
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === CONFIG ===
INPUT_SCORES = "arnn_output_scores.csv"
NODE_FEATURES = "o3_vectorized_dao_dio.csv"
OUTPUT_IMAGE = "nag_graph.png"
RISK_THRESHOLD = 0.6
TOP_K = 10  # numero di nodi critici da evidenziare

# === CARICAMENTO DATI ===
scores_df = pd.read_csv(INPUT_SCORES)
features_df = pd.read_csv(NODE_FEATURES)
scores_df["node_id"] = features_df["node_id"].values

# === COSTRUZIONE GRAFO ===
G = nx.DiGraph()

# Aggiunta nodi e punteggio di rischio
for idx, row in scores_df.iterrows():
    node = f"Node_{int(row['node_id'])}"
    risk = row["risk_score"]
    G.add_node(node, risk=risk, high_risk=row["high_risk"])

# Aggiunta archi simulati tra nodi consecutivi (per test visivo)
nodes = list(G.nodes())
for i in range(len(nodes) - 1):
    w = (G.nodes[nodes[i]]['risk'] + G.nodes[nodes[i+1]]['risk']) / 2
    G.add_edge(nodes[i], nodes[i+1], weight=w)

# === IDENTIFICAZIONE NODI CRITICI ===
critical_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['risk'], reverse=True)[:TOP_K]

# === VISUALIZZAZIONE ===
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
node_colors = ['red' if G.nodes[n]['high_risk'] else 'lightblue' for n in G.nodes()]
node_sizes = [500 + 3000 * G.nodes[n]['risk'] for n in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
nx.draw_networkx_edges(G, pos, alpha=0.4)
nx.draw_networkx_labels(G, pos, font_size=8)

# Evidenzia nodi critici
for node, data in critical_nodes:
    x, y = pos[node]
    plt.text(x, y + 0.03, f"{data['risk']:.2f}", fontsize=7, ha='center', color='black')

plt.title("Network Attack Graph (DAO–DIO)")
plt.axis('off')
plt.tight_layout()
plt.savefig(OUTPUT_IMAGE)
print(f"✅ Grafo salvato in: {OUTPUT_IMAGE}")
