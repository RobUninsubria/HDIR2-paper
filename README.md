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
