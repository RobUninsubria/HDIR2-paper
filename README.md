# H-DIR^2
Official repository for the paper “(H‑DIR)²: A Scalable Entropy‑Based Framework…”.
Includes Python/Spark code, Jupyter notebooks, Docker setup, and stress‑test scripts to reproduce step‑by‑step all experiments (SYN‑Flood, DAO‑DIO, NTP Amplification) and the dual‑scalability validation up to 1 million devices.

![immagine](https://github.com/user-attachments/assets/af9ca67e-dc0f-443f-956c-7517f23ab899)

# 1. Clona il repository e scarica i file di grandi dimensioni via Git LFS
git clone https://github.com/RobUninsbria/paper2.git
cd paper2
git lfs pull            # scarica i dataset di esempio e i checkpoint

# 2. lancia un singolo esperimento dallo script helper
bash scripts/run_syn_flood.sh          # ↳ Sezione 4.1 del paper
bash scripts/run_dao_dio.sh            # ↳ Sezione 4.2
bash scripts/run_ntp_amplification.sh  # ↳ Sezione 4.3

# 3. Apri il notebook di validazione dual‑scalability
#    (porta predefinita Jupyter: http://localhost:8888)
firefox (https://github.com/RobUninsbria/paper2/blob/main/stress_test) 


