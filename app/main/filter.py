from app.models import Product


def filter_products_with_category(category_id, availability):
    query = Product.query

    if category_id and category_id != '0':
        query = query.filter(Product.category_id == category_id)
    if availability and availability != '0':
        query = query.filter(Product.amount > 0)

    filtered_data = query.all()
    return [product.to_dict() for product in filtered_data]
