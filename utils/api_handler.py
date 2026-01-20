# =====================================
# PART 3: API INTEGRATION
# This file is responsible for connecting
# our sales system with the DummyJSON product API
# =====================================
# Handle fetching and mapping product data from external API

import requests


def fetch_all_products():
    """
    This function fetches all products
    from the DummyJSON Products API.

    We use limit=100 to make sure we get
    all available products in one call.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)

        # If API does not respond correctly
        if response.status_code != 200:
            print("Failed to fetch products from API")
            return []

        data = response.json()

        print("Successfully fetched products from API")

        # We only return the 'products' list from API response
        return data.get("products", [])

    except Exception as e:
        print("API Error:", e)
        return []


def create_product_mapping(api_products):
    """
    This function creates a dictionary
    that maps API product ID to useful product information.

    Example:
    {
        1: {
            'title': 'iPhone',
            'category': 'mobile-accessories',
            'brand': 'Apple',
            'rating': 4.6
        }
    }

    NOTE:
    DummyJSON API contains mixed product categories
    (like beauty, fragrances, etc.).
    Since this project is based on electronics sales,
    we logically map those categories to electronics-related ones.
    """

    # Category mapping to keep data relevant to electronics sales
    CATEGORY_MAP = {
        "fragrances": "mobile-accessories",
        "beauty": "electronics",
        "skincare": "electronics"
    }

    # Brand mapping to keep brand names realistic
    BRAND_MAP = {
        "Chanel": "Apple",
        "Gucci": "Asus",
        "Dior": "Seagate",
        "Dolce & Gabbana": "TechGear",
        "Calvin Klein": "Logitech"
    }

    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")

        # Raw values from API
        raw_category = product.get("category", "")
        raw_brand = product.get("brand", "")

        # Apply logical mapping
        mapped_category = CATEGORY_MAP.get(raw_category, "electronics")
        mapped_brand = BRAND_MAP.get(raw_brand, "Generic")

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": mapped_category,
            "brand": mapped_brand,
            "rating": product.get("rating")
        }

    return product_mapping
