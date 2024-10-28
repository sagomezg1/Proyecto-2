# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


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

