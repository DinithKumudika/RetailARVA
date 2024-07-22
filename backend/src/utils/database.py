import csv
import re
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from configs.database import Database
from models.entities import Product, CustomerReview
from models.entities import Base

def add_reviews_from_csv(csv_file_path : str, session : Session):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            product_id = int(row['Id'])  # Assuming 'id' in CSV corresponds to 'product_id'
            reviews = row['Customer Reviews'].split('<br>')
            for review_entry in reviews:
                review_match = re.search(r'"(.*?)"', review_entry)
                rating_match = re.search(r'(\d+(\.\d+)?)\s*stars', review_entry)
                if review_match and rating_match:
                    review = review_match.group(1)
                    rating = float(rating_match.group(1))
                    review_record = CustomerReview(
                        product_id=product_id, 
                        review=review, 
                        rating=rating
                    )
                    session.add(review_record)
        session.commit()

def add_products_from_csv(csv_file_path: str, session: Session):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        print(csv_reader.fieldnames)
        for row in csv_reader:
            name = str(row['Name']).strip().replace("'", "''")
            brand = str(row['Brand']).strip().replace("'", "''")
            category = str(row['Category']).strip().replace("'", "''")
            ingredients = str(row['Ingredients']).strip().replace("'", "''")
            key_ingredients = str(row['Key Ingredients']).strip().replace("'", "''")
            benefits =str(row['Benefit']).strip().replace("'", "''")
            concentrations = str(row['Concentrations']).strip().replace("'", "''")
            usage = str(row['Usage']).strip().replace("'", "''")
            application_tips = str(row['Application Tips']).strip().replace("'", "''")
            skin_types = str(row['Skin Type']).strip().replace("'", "''")
            skin_concernes = str(row['Skin Concern']).strip().replace("'", "''")
            is_natural = True if str(row['Natural']).strip().lower() == 'yes' else False
            side_effects = 'NULL' if str(row['Potential Side Effects']).strip().lower() == 'none reported' else str(row['Potential Side Effects']).strip().replace("'", "''")
            price = float(str(row['Price']).replace(',', ''))
            sensitivities = 'NULL' if str(row['Sensitivities']).strip().lower() == 'none' else str(row['Sensitivities']).strip().replace("'", "''")
            allergens = 'NULL' if str(row['Allergens']).strip().lower() == 'none' else str(row['Allergens']).strip().replace("'", "''")

            product = Product(
                name = name,
                brand = brand,
                category = category,
                price = price,
                ingredients = ingredients,
                key_ingredients = key_ingredients,
                benefits = benefits,
                side_effects = side_effects,
                is_natural = is_natural,
                concentrations = concentrations,
                usage = usage,
                application_tips = application_tips,
                skin_types = skin_types,
                skin_concerns = skin_concernes,
                allergens = allergens,
                sensitivities= sensitivities
            )
            session.add(product)
        session.commit()

def is_database_created(db: Database) -> bool:
    metadata = MetaData()
    metadata.reflect(bind=db.get_engine())
    tables = metadata.tables.keys()

    if(len(tables) == 2):
        return True
    return False


def create_all(db: Database):
    Base.metadata.create_all(db.get_engine())

    metadata = MetaData()
    metadata.reflect(bind=db.get_engine())
    tables = metadata.tables.keys()
    print(f"{','.join(tables)} tables created")

    csv_file_path : str = "./data/products.csv"
    add_products_from_csv(csv_file_path, db.get_session())
    add_reviews_from_csv(csv_file_path, db.get_session())