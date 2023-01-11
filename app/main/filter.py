from app.models import Product


def filter_products_with_category(category_id):
    if not category_id or category_id == '0':
        filtered_data = Product.query.all()
    else:
        filtered_data = Product.query.filter_by(category_id=category_id).all()
    return [product.to_dict() for product in filtered_data]
