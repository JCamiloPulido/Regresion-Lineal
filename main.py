import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# 1) Subir archivo (OBLIGATORIO)
# =========================================================


from tkinter import Tk
from tkinter.filedialog import askopenfilename

print("Abriendo selector de archivos...")

try:
    root = Tk()
    root.withdraw()           # oculta la ventana principal
    root.attributes("-topmost", True)  # fuerza que el diálogo salga al frente

    filename = askopenfilename(
        title="Selecciona archivo Excel o TXT/CSV",
        filetypes=[
            ("Archivos Excel", "*.xlsx *.xls"),
            ("Archivos Texto/CSV", "*.txt *.csv"),
            ("Todos los archivos", "*.*")
        ]
    )

    root.destroy()

except Exception as e:
    print("No se pudo abrir el selector de archivos (tkinter).")
    print("Error:", e)
    filename = input("Escribe la ruta del archivo: ").strip()

if filename == "":
    raise ValueError("No seleccionaste ningún archivo.")

print(f"Archivo seleccionado: {filename}")



# =========================================================
# 2) Leer el archivo según extensión
# =========================================================
if filename.lower().endswith((".xlsx", ".xls")):
    df_in = pd.read_excel(filename)

elif filename.lower().endswith((".txt", ".csv")):
    # Intentar separadores comunes: coma, punto y coma, tab
    try:
        df_in = pd.read_csv(filename)  # coma
    except:
        try:
            df_in = pd.read_csv(filename, sep=";")  # punto y coma
        except:
            df_in = pd.read_csv(filename, sep="\t")  # tab

else:
    raise ValueError("Formato no soportado. Usa .xlsx/.xls o .txt/.csv")

# =========================================================
# 3) Tomar columnas x e y
#    - Si existen columnas 'x' y 'y' (sin importar mayúsculas), las usa
#    - Si no, toma las dos primeras columnas
# =========================================================
df_in.columns = [str(c).strip().lower() for c in df_in.columns]

if ("x" in df_in.columns) and ("y" in df_in.columns):
    x = df_in["x"].astype(float).to_numpy()
    y = df_in["y"].astype(float).to_numpy()
else:
    if df_in.shape[1] < 2:
        raise ValueError("El archivo debe tener al menos 2 columnas (x y y).")
    x = df_in.iloc[:, 0].astype(float).to_numpy()
    y = df_in.iloc[:, 1].astype(float).to_numpy()

# Validación básica
if len(x) != len(y):
    raise ValueError("Las columnas x e y deben tener la misma cantidad de datos.")
if len(x) < 2:
    raise ValueError("Se necesitan al menos 2 puntos para calcular la recta.")

# =========================================================
# 4) Mantener el mismo ejercicio: sumatorias, m y b
# =========================================================
n = len(x)

xy = x * y
x2 = x ** 2

sum_x = x.sum()
sum_y = y.sum()
sum_xy = xy.sum()
sum_x2 = x2.sum()

m = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x2) - (sum_x ** 2))
b = (sum_y - (m * sum_x)) / n

y_hat = m * x + b

# =========================================================
# 5) Tabla de datos
# =========================================================
df = pd.DataFrame({
    "x": x,
    "y": y,
    "x*y": xy,
    "x^2": x2,
    "y_estimado (m*x+b)": y_hat
})

print(f"\nn = {n}")
print(f"sum(x)  = {sum_x:.4f}")
print(f"sum(y)  = {sum_y:.4f}")
print(f"sum(x*y)= {sum_xy:.4f}")
print(f"sum(x^2)= {sum_x2:.4f}")
print("\nEcuación ajustada:")
print(f"y = {m:.6f} * x + {b:.6f}")

print("\nTabla de datos:\n")
print(df.to_string(index=False))


# =========================================================
# 6) Gráfico de dispersión + recta
# =========================================================
plt.figure(figsize=(7,5))
plt.scatter(x, y, label="Datos (x,y)")
plt.plot(x, y_hat, label="Recta ajustada")
plt.title("Dispersión y ajuste lineal: y = m x + b")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
