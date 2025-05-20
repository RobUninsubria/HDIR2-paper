
from pyspark.sql import SparkSession
from pyspark.sql.functions import window
import pandas as pd

# === CONFIGURAZIONE INIZIALE ===
# Caricamento del dataset DAO-DIO (estratto da 25_Markov.xlsx salvato in CSV)
csv_path = "dao_dio_cleaned.csv"  # Assicurati che questo file sia disponibile nel container

# === AVVIO SPARK ===
spark = SparkSession.builder \
    .appName("DAO-DIO Spark Windowing") \
    .getOrCreate()

# === LETTURA CSV ===
df = pd.read_csv(csv_path, parse_dates=["timestamp"])
spark_df = spark.createDataFrame(df)

# === FINESTRA TEMPORALE 5s ===
windowed_df = spark_df.groupBy(window("timestamp", "5 seconds")).agg(
    {"Energy consumption": "avg", "Hops from sink": "avg", "Error": "avg"}
)

# === OUTPUT ===
windowed_df.orderBy("window").show(truncate=False)

# === CHIUSURA ===
spark.stop()
