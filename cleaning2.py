import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load the dataset
df = pd.read_csv(r'C:\Users\ADVAN WORKPRO\OneDrive\Documents\College\Dicoding\Capstone\Indonesian_Food_Recipes.csv')

# Display the first few rows of the dataset
print(df.head())

# Lower case column names for consistency
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Lower case all string columns for consistency
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.lower()

# Check current columns
print("Current columns:", df.columns.tolist())

# Drop unnecessary columns
df.drop(columns=['title'], inplace=True)

# Make column title_cleaned as first column
cols = df.columns.tolist()
if 'title_cleaned' in cols:
    cols.insert(0, cols.pop(cols.index('title_cleaned')))
    df = df[cols]
    
print("Final columns:", df.columns.tolist())

# Rename columns for clarity
df.rename(columns={
    'title_cleaned': 'recipe_name',
    'ingredients': 'ingredients_raw',
    'loves': 'love_count',
    'ingredients_cleaned': 'ingredients_cleaned',
    'total steps': 'total_steps',
    'ingredients final': 'ingredients_list'
}, inplace=True)

# Check for missing values
print(df.isnull().sum())

# Drop rows with missing values
df.dropna(inplace=True)

# Cleaning messy formatting in recipe name column
df['recipe_name'] = (df['recipe_name']
    .str.replace(r"[\"']", '', regex=True)
    .str.replace(r'^_+', '', regex=True)
    .str.strip())
messy_patterns = [
    # Subjektif / promosi
    r'\benak+\b', r'\byumm+y?\b', r'\bmaknyus+\b', r'\bendess*\b',
    r'\bendol+\b', r'\bjoss\b', r'\bwuenak+\b', r'\buenakk*\b',
    r'\buenak+\b', r'\bmantap+\b', r'\bnyuss*\b', r'\blegit\b',
    r'\bgurih\b', r'\bgampang\b', r'\bpraktis\b', r'\bsimpel\b',
    r'\bsimple\b', r'\bsederhana\b', r'\bmudah\b', r'\bhemat\b',
    r'\bekonomi[s]?\b', r'\bmurah\b', r'\bspecial\b', r'\bspesial\b',
    r'\binstan[t]?\b', r'\bkilat\b', r'\bcepat\b', r'\bexpress\b',
    r'\bekspres+\b', r'\brenyah\b', r'\bgaring\b', r'\bkrenyes+\b', 
    r'\bkress+\b', r'\bhome\s*made\b', r'\brumahan\b', r'\bsehat\b', 
    r'\bdiet\b', r'\benaaak\b', r'\bbangeet\b', r'\bramah\b', 
    r'\banak\b', r'\bcocok\b', r'\btidak\b', r'\bga\b', r'\bgak\b', 
    r'\btanpa\b', r'\bpedass\b', r'\btkl\b', r'\bpraktis\b', 
    r'\bsimple\b', r'\bsederhana\b', r'\bmudah\b',
    # Nama / "ala" / "by"
    r'\bala\s+[\w\s]{1,20}', r'\bby\s+[\w\s]{1,20}', r'\bala\b', r'\bkw\b',
    # Alat masak & keterangan
    r'\(.*?\)', r'\bteflon\b', r'\bhappy\s*call\b', r'\boven\b',
    r'\bmagic\s*com\b', r'\b(ma?gi?|me?ji?)com\b', r'\bpresto\b',
    r'\brice?\s*cooker\b', r'\bblender\b', r'\bmicrowave\b', r'\bmejikom\b',
    # Kata tambahan
    r'\bno\s+(msg|ribet|santan)\b', r'\bnon\s+msg\b',
    r'\banti\s+gagal\b', r'\bversi\s+\w+', r'\bresep\s+\w+',
    r'\btips+\b', r'\bstep\s+by\s+step\b', r'\bpart\s+\d+',
    r'\bsuka[\s-]*suka\b', r'\bseadanya\b', r'\balakadarnya\b',
    r'\brecook\b', r'\bpr_\w+', r'\ba\s*k\s*a\b', r'\bvs\b',
    # Simbol
    r'[`\'\"\\()\[\]{}]', r'[\+\*\!]{2,}', r'[^\w\s]',
]
pattern = '|'.join(messy_patterns)
df['recipe_name'] = (df['recipe_name']
    .str.replace(pattern, ' ', flags=re.IGNORECASE, regex=True)
    .str.replace(r'\s+', ' ', regex=True)
    .str.strip())

# Check for duplicates
print(f"Duplicated Recipe Name: {df['recipe_name'].duplicated().sum()}")
print(f"Duplicated Ingredients Cleaned: {df['ingredients_cleaned'].duplicated().sum()}")

# Drop duplicate rows and keep the most loved one based on love count
df.sort_values('love_count', ascending=False, inplace=True)
df.drop_duplicates(subset=['recipe_name'], keep='first', inplace=True)
df.drop_duplicates(subset=['ingredients_cleaned'], keep='first', inplace=True)  

# Check for duplicates again after dropping
print(f"Duplicated Recipe Name: {df['recipe_name'].duplicated().sum()}")
print(f"Duplicated Ingredients Cleaned: {df['ingredients_cleaned'].duplicated().sum()}")

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)

# Display the cleaned dataset
print(df.head())
df.info()

# Save the cleaned dataset to a new CSV file
df.to_csv(r'C:\Users\ADVAN WORKPRO\OneDrive\Documents\College\Dicoding\Capstone\Recipes_Cleaned.csv', index=False)