
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# === CONFIG ===
INPUT_CSV = "o3_vectorized_dao_dio.csv"
THRESHOLD_RISK = 0.6
INPUT_DIM = 256  # da paper
HIDDEN_DIM = 128
LEARNING_RATE = 1e-3
ALPHA = 0.3
BETA = 0.7
EPOCHS = 20
BATCH_SIZE = 16

# === MODELLO ARNN ===
class ARNN(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(ARNN, self).__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(hidden_dim, input_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        h = self.relu(self.linear1(x))
        out = self.sigmoid(self.linear2(h))
        return out

# === DATI ===
df = pd.read_csv(INPUT_CSV)
X = df.drop(columns=["timestamp", "error"]).fillna(0).values.astype(np.float32)
y = df["error"].fillna(0).values.astype(np.float32)
y = (y - y.min()) / (y.max() - y.min())  # normalizzazione

X_tensor = torch.tensor(X)
y_tensor = torch.tensor(y).unsqueeze(1)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# === ISTANZA MODELLO ===
model = ARNN(input_dim=INPUT_DIM, hidden_dim=HIDDEN_DIM)
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# === TRAINING ===
for epoch in range(EPOCHS):
    for xb, yb in loader:
        pred = model(xb)
        loss_cls = criterion(pred.mean(1, keepdim=True), yb)
        loss_graph = criterion(pred, xb)  # ricostruzione
        loss = ALPHA * loss_cls + BETA * loss_graph
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {loss.item():.4f}")

# === RISCHIO ===
with torch.no_grad():
    outputs = model(X_tensor)
    risk_scores = outputs.mean(1).numpy()

# === SALVATAGGIO ===
df["risk_score"] = risk_scores
df["high_risk"] = df["risk_score"] > THRESHOLD_RISK
df[["timestamp", "risk_score", "high_risk"]].to_csv("arnn_output_scores.csv", index=False)
print("✅ File salvato: arnn_output_scores.csv")
