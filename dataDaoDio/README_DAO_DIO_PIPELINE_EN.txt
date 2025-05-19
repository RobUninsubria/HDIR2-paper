
# DAO–DIO Attack Simulation — (H-DIR)² Pipeline

This directory contains all scripts required to reproduce the DAO–DIO attack simulation
based on the methodology described in the paper "(H-DIR)²: A Scalable Entropy-Based Framework".

## 📁 Main Files

| Script/File                             | Function                                                                 |
|----------------------------------------|--------------------------------------------------------------------------|
| `dao_dio_cleaned.csv`                  | Preprocessed dataset with 10Hz timestamp                                 |
| `o2_windowing_dao_dio.py`              | Operator O2: Spark SQL with 5-second sliding window                      |
| `o3_vectorized_dao_dio.csv`            | One-hot encoded dataset for ARNN training                                |
| `o4_arnn_training_dao_dio.py`          | Operator O4: Train ARNN and compute risk scores                          |
| `arnn_output_scores.csv`               | Output: timestamp, `risk_score`, `high_risk` flag                        |
| `o5_network_attack_graph_dao_dio.py`   | Operator O5: Build and visualize Network Attack Graph (NAG)              |
| `nag_graph.png`                        | NAG image with critical nodes highlighted                                |
| `o6_rdf_injection_dao_dio.py`          | Operator O6: Inject RDF triples with risk scores                         |
| `dao_dio_risk_injected.ttl`            | Output RDF file in Turtle format                                         |

## ▶️ Pipeline Execution

1. Preprocess the original Excel file into `dao_dio_cleaned.csv`
2. Run Spark processing:
   ```
   spark-submit o2_windowing_dao_dio.py
   ```
3. Train ARNN:
   ```
   python o4_arnn_training_dao_dio.py
   ```
4. Build and visualize NAG:
   ```
   python o5_network_attack_graph_dao_dio.py
   ```
5. Inject RDF risk scores:
   ```
   python o6_rdf_injection_dao_dio.py
   ```

## 📊 Experiment Parameters

- Window: 5 seconds (`∆t = 5s`)
- Vector size: `d = 256`
- ARNN: `n_h = 128`, `η = 1e−3`, `α = 0.3`, `β = 0.7`
- High risk if: `R_i > 0.6`

---

© University of Insubria — PAPER² Project (H-DIR)²
