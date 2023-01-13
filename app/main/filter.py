from sqlalchemy import or_

from app.models import Product


def filter_or_search_products(category_id, availability, search):
    query = Product.query

    if category_id and category_id != '0':
        # Filter the products by the selected category
        query = query.filter(Product.category_id == category_id)
    if availability and availability != '0':
        # Filter the products by the selected availability
        query = query.filter(Product.amount > 0)
    if search:
        # Filter the products by name or description that match the search term
        query = query.filter(or_(Product.name.like(f'%{search}%'), Product.description.like(f'%{search}%')))
        # Order the products so that matches by name are shown first, followed by matches by description
        query = query.order_by(Product.name.desc(), Product.description.desc())

    filtered_data = query.all()
    return [product.to_dict() for product in filtered_data]
