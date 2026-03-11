import pandas as pd
import numpy as np


def learn_pandas():
    # Buat dataframe dengan label dan vector masing-masing hewan/kendaraan
    df = pd.DataFrame({
        'label': ["kucing","anjing","motor","mobil"],
        'vector': [
            # [kucing, anjing, motor, mobil]
            [1,   0.9, 0.1, 0.2],  # kucing: mirip diri sendiri & anjing
            [0.9, 1,   0.2, 0.1],  # anjing: mirip kucing
            [0.1, 0.2, 1,   0.8],  # motor: mirip mobil
            [0.2, 0.1, 1,   0.8],  # mobil: mirip motor
        ]
    })

    # Query: "cari yang mirip motor & mobil"
    query = [0.15, 0.15, 1, 0.8]

    # Hitung cosine similarity antara query dan setiap vector di df
    df['similarity'] = df['vector'].apply(lambda v: cosine_sim(query, v))

    # Tampilkan hasil, diurutkan dari yang paling mirip
    print(df.sort_values('similarity', ascending=False))


def cosine_sim(a, b):
    # Konversi ke numpy array
    a, b = np.array(a), np.array(b)

    # Rumus: dot(a,b) / (||a|| * ||b||)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


