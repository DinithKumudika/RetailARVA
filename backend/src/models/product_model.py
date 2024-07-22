from pydantic import BaseModel
from typing import List, Optional

class ProductModel(BaseModel):
    id : int
    name : str
    brand : str
    category : str
    price : float
    ingredients : List[str]
    key_ingredients : List[str]
    benefits : List[str]
    side_effects : Optional[List[str]] =  None
    is_natural : bool
    concentrations : str
    usage : str
    application_tips : List[str]
    skin_types : List[str]
    skin_concerns : List[str]
    allergens : Optional[List[str]] = None
    sensitivities : Optional[List[str]] = None
