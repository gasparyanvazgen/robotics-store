from sqlalchemy import or_, case, text

from app.models import Product
from config import PRODUCTS_PER_PAGE


def filter_or_search_products(page, category_id, availability, search):
    query = Product.query

    if category_id and category_id != 0:
        # Filter the products by the selected category
        query = query.filter(Product.category_id == category_id)
    if availability == 'on':
        # Filter the products by the selected availability
        query = query.filter(Product.amount > 0)
    if search:
        # Filter the products by name or description that match the search term
        query = query.filter(or_(Product.name.ilike(f'%{search}%'), Product.description.ilike(f'%{search}%')))

        '''
        Create a custom ordering criteria for the search matches it first checks for
        matches in the name field and if it finds any, it assigns a score of 1, otherwise
        it assigns a score of 2. Then it does the same for the description field. 
        Finally, it orders the results based on those scores, name, and description fields.
        '''
        query = query.order_by(
            case([(Product.name.ilike(f'%{search}%'), 1)], else_=2),
            case([(Product.description.ilike(f'%{search}%'), 1)], else_=2),
            text('name'),
            text('description')
        )
    pagination = query.paginate(page=page, per_page=PRODUCTS_PER_PAGE)
    filtered_data = pagination.items

    return [product.to_dict() for product in filtered_data], pagination
