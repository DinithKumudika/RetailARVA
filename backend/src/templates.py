product_profile = """
    # {{ name }}
    ---
    ## Product Overview
    - Name: {{ name }}
    - Brand: {{ brand }}
    - Category: {{ category }}
    - Price: {{ price }} (in LKR)
    - Natural: {{ is_natural }} 

    ## Ingredients
    - Key Ingredients: {{ key_ingredients }}
    - Concentrations: {{ concentrations }}
    - Full Ingredient List: {{ ingredients }}
/
    ## Benefits and Claims
    - Benefits: {{ benefits }}
    - Claims: {{ claims }}

    ## Usage and Application
    - Usage: {{ usage }}
    - Application Tips: {{ application_tips }}

    ## Skin Suitability
    - Suitable for Skin Types: {{ skin_types }}
    - Addresses Skin Concerns: {{ skin_concerns }}
    - For Sensitive Skin: {{ for_sensitive_skin }}

    ## Safety Information
    - Potential Side Effects: {{ side_effects }}
    - Allergens: {{ allergens }}

    ## Reviews and Ratings
    - Average Rating: {{ average_rating }}/5
    - Customer Reviews:
        {% for review in customer_reviews %}
        - {{ review.review }} - {{ review.rating }} stars
        {% endfor %}
    - Expert Review: {{ expert_review }}
"""

user_profile = """
    # User Profile
    ---
    ## Personal Information
    - Age: {{age }}
    - Gender: {{ gender }}

    ## Skin Profile
    - Skin Type: {{ skin_type }}
    - Sensitive Skin: {{ sensitive }}
    - Skin Concerns: {{ skin_concerns }}

    ## Product Preferences
    - Preferred Price Range: LKR {{ min_price }} - {{ max_price }}
    - Preferences: {{ preferences }}

    ## Safety Information
    - Ingredients to Avoid: {{ ingredients_to_avoid }}
    - Known Allergies: {{ known_allergies }}
"""