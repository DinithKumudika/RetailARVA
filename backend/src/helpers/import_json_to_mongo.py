from flask import json
import pandas as pd
from src.models.models import Product
from typing import List

def load_from_csv(csv_file_path: str):
    """
    Loads product data from a CSV file and converts it into a list of Product objects.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        List[Product]: A list of Product objects created from the CSV data.
    """
    try:
        df = pd.read_csv(csv_file_path)
        print("CSV file successfully loaded.")
        
        products : List[Product] = []
        
        for index, row in df.iterrows():
            allergens = row['Allergens']
            if pd.isna(allergens) or allergens.strip() == "":
                allergens = None
            else:
                allergens = [item.strip() for item in str(allergens).split(', ')]
                
            sensitivities = row['Sensitivities']
            if pd.isna(sensitivities) or sensitivities.strip() == "":
                sensitivities = None
            else:
                sensitivities = [item.strip() for item in str(sensitivities).split(', ')]
            
            side_effects = row['Potential Side Effects']
            if pd.isna(side_effects) or str(side_effects).strip() == "":
                side_effects = None
            elif side_effects == 'None reported':
                side_effects = None
            else:
                side_effects = [item.strip() for item in str(side_effects).split(', ')]
            
            skin_concerns = row['Skin Concern']
            if pd.isna(skin_concerns) or str(skin_concerns).strip() == "":
                skin_concerns = None
            else:
                skin_concerns = [item.strip() for item in str(skin_concerns).split(', ')]
                
            product = Product(
                product_id=row['Id'],
                name=row['Name'],
                brand=row['Brand'],
                category=row['Category'],
                price=float(row['Price'].replace(',', '')),  # Remove commas and convert to float
                ingredients=row['Ingredients'].split(', '),
                key_ingredients=row['Key Ingredients'].split(', '),
                benefits=row['Benefit'],
                is_natural=row['Natural'].lower() == 'yes',
                concentrations=row['Concentrations'],
                usage=row['Usage'],
                application_tips=row['Application Tips'],
                skin_types=row['Skin Type'],
                skin_concerns=skin_concerns,
                side_effects=side_effects,
                allergens=allergens,
                sensitivities=sensitivities,
            )
            products.append(product)
        return products
        
    except FileNotFoundError:
        print(f"Error: The file at path '{csv_file_path}' does not exist.")
        raise
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def save_to_json(json_path: str, data: List[Product]):
    with open(json_path, 'r') as f:
        json.dump(data, f)
    

def load_from_json(json_file_path: str):
    with open(json_file_path, 'r') as f:
        products_json = json.load(f)
    return products_json
