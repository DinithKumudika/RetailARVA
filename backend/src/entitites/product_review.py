from sqlalchemy import Column, String, Integer, CHAR, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class Reviews():
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    customer_review_id = Column(Integer, ForeignKey("customer_reviews.id"), index = True, nullable = False)
    average_rating = Column(Float, nullable=False)
    expert_review = Column(String, nullable=False)
    claims = Column(String, nullable=True)

    def __init__(self, product_id, avg_rating, customer_review_id, expert_review, claims = None):
        self.product_id = product_id
        self.average_rating = avg_rating
        self.customer_review_id = customer_review_id
        self.expert_review = expert_review
        self.claims = claims