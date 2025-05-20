# H-DIR^2
Official repository for the paper “(H‑DIR)²: A Scalable Entropy‑Based Framework…”.
Includes Python/Spark code, Jupyter notebooks, Docker setup, and stress‑test scripts to reproduce step‑by‑step all experiments (SYN‑Flood, DAO‑DIO, NTP Amplification) and the dual‑scalability validation up to 1 million devices.

![immagine](https://github.com/user-attachments/assets/af9ca67e-dc0f-443f-956c-7517f23ab899)


# 1. Clone the repository and pull large files via Git LFS
git clone https://github.com/RobUninsbria/paper2.git
cd paper2
git lfs pull              # downloads sample datasets and ARNN checkpoints

# 2. Launch a single experiment via the helper script
bash scripts/run_syn_flood.sh          # ↳ Section 4.1 of the paper
bash scripts/run_dao_dio.sh            # ↳ Section 4.2
bash scripts/run_ntp_amplification.sh  # ↳ Section 4.3

# 3. Open the dual‑scalability validation notebook
#    (default Jupyter port: http://localhost:8888)
firefox http://localhost:8888/notebooks/stress_test.ipynb
firefox (https://github.com/RobUninsbria/paper2/blob/main/stress_test)


**/notebooks/** – Jupyter notebooks that reproduce  experiments; they include inline functions for data conversion, entropy metrics, and ARNN inference, so no extra modules are needed.
# (H-DIR)² – A Scalable Entropy-Based Framework for Anomaly Detection and Cybersecurity in Cloud IoT Data Centers

Official repository for the paper **"(H-DIR)²: A Scalable Entropy-Based Framework for Anomaly Detection and Cybersecurity in Cloud IoT Data Centers"**.

This repository contains the full codebase, datasets, and Jupyter notebooks used to reproduce the experimental results described in the paper. The framework provides a modular and extensible architecture for:
- Real-time anomaly detection
- Entropy-based behavior analysis
- Risk graph inference over IoT networks
- Cloud-integrated training pipelines using containerized environments

---

## 📁 Repository structure

- `dataDaoDio/` – DAO-DIO dataset and processing scripts  
- `dataSynFlood/` – SYN Flood detection experiment  
- `dataNTP_Amplification/` – NTP Amplification case study  
- `notebooks/` – Jupyter notebooks for entropy analysis and RDF graph generation  
- `hdir-code/` – Core code of the (H-DIR)² framework  
- `Docker/` – Docker setup for full reproducibility  
- `stress_test/` – Benchmark scalability tests up to 1M devices  

---

## ⚙️ Reproducibility

All experiments can be reproduced via the included Jupyter notebooks.  
We recommend using the Docker environment for consistent results.

# (H-DIR)² – A Scalable Entropy-Based Framework for Anomaly Detection and Cybersecurity in Cloud IoT Data Centers

[![Reproducibility - Docker Image Available](https://img.shields.io/badge/Reproducibility-Docker%20Image%20Available-blue?logo=docker&style=flat-square)](https://drive.google.com/drive/folders/1N4z_YojP46xP9XWdiLqxism9JbzqV9NKO?usp=drive_link)

Official repository for the paper ...


Contact
For questions, please contact
📧 roberto.pazzi@uninsubria.it
🔬 University of Insubria – Department of Advanced Technologies
