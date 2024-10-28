# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

import matplotlib.pyplot as plt
import seaborn as sns

#LIMPIEZA DE DATOS

# Load the dataset
file_path = file_path = 'C:/Users/saral/OneDrive - Universidad de los andes/ARCHVIOS MAC SARA/SARA GG 8/OCTAVO SEMESTRE/ANALITICA/PROYECTO 2/bank-full.csv'

data = pd.read_csv(file_path, sep=';')


# Label encoding for binary categorical columns
binary_columns = ['default', 'housing', 'loan', 'y']
for col in binary_columns:
    data[col] = LabelEncoder().fit_transform(data[col])

data['job'].fillna(data['job'].mode()[0], inplace=True)
data['education'].fillna(data['education'].mode()[0], inplace=True)


# One-hot encoding for multi-category columns
multi_category_columns = ['job', 'marital', 'education', 'contact', 'month', 'poutcome']
data = pd.get_dummies(data, columns=multi_category_columns, drop_first=True)


# Replace 'unknown' with a more appropriate label or strategy (e.g., 'unknown' -> NaN, then impute or remove)
data.replace('unknown', pd.NA, inplace=True)

# Optionally drop rows with missing values or impute them (here we impute with the mode for simplicity)
data.fillna(data.mode().iloc[0], inplace=True)

# Step 3: Verify the data is ready for analysis
print(data.info())
print(data.head())
print(data.columns)


#EXPLORACION DE DATOS

# Histogramas
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
data['age'].hist(ax=axes[0, 0])
axes[0, 0].set_title('Histograma de Edad')

data['balance'].hist(ax=axes[0, 1])
axes[0, 1].set_title('Histograma de Saldo')
    
sns.countplot(x='housing', data=data, ax=axes[1, 0])
axes[1, 0].set_title('Distribución de Crédito de Vivienda')

sns.countplot(x='loan', data=data, ax=axes[1, 1])
axes[1, 1].set_title('Distribución de Crédito Personal')
plt.tight_layout()
plt.show()

#Diagrama de Cajas

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
data.boxplot(column='age', ax=axes[0])
axes[0].set_title('Diagrama de Caja de Edad')
data.boxplot(column='balance', ax=axes[1])
axes[1].set_title('Diagrama de Caja de Saldo')
plt.tight_layout()
plt.show()

# Diagramas de violín

# Crear una nueva columna que indique el tipo de contacto
data['contact'] = data[['contact_telephone', 'contact_unknown']].idxmax(axis=1)

# Reemplazar los nombres de las columnas para que sean más descriptivos
data['contact'] = data['contact'].replace({'contact_telephone': 'Telephone', 'contact_unknown': 'Unknown'})

# Graficar el diagrama de violín con la nueva columna 'contact'
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(x='contact', y='duration', data=data, ax=ax)
ax.set_title('Distribución de Duración de Campaña por Tipo de Contacto')
ax.set_xlabel('Tipo de Contacto')
ax.set_ylabel('Duración de Campaña (días)')
plt.tight_layout()
plt.show()


# Diagramas de dispersión
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
data.plot(kind='scatter', x='age', y='balance', ax=axes[0])
axes[0].set_title('Edad vs. Saldo')

data.plot(kind='scatter', x='age', y='y', ax=axes[1])
axes[1].set_title('Edad vs. y')
plt.tight_layout()
plt.show()