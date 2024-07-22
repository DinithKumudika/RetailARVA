from configs.database import Database
from models.product_model import ProductModel
from models.entities import Product

class ProductRepository:
    def __init__(self, db : Database) -> None:
        self.session = db.get_session()

    def fetch_all(self):
        return self.session.query(Product).all()