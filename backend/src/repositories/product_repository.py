from src.configs.database import Database
from src.models.product_model import ProductModel
from src.models.entities import Product

class ProductRepository:
    def __init__(self, db : Database) -> None:
        self.session = db.get_session()

    def fetch_all(self):
        return self.session.query(Product).all()
    
    def fetch_by_id(self, product_id: int):
        return self.session.query(Product).filter_by(id=product_id).first()