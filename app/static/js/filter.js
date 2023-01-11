let products;

// get selected category
$(document).ready(function() {
    $('#categorySelect').on('change', function() {
        let selectedCategoryId = $(this).val();
        filterProductsWithCategory(selectedCategoryId);
    });
});

// get filtered products
function filterProductsWithCategory(category_id) {
    $.ajax({
        type: "GET",
        url: "/filter-products",
        data: {category_id: category_id},
        success: function (data) {
            products = data;
            render();
        }
    });
}

// update the contents of the webpage with the filtered data
function render() {
    let container = document.querySelector('.row');
    container.innerHTML = '';

    products.forEach(function(product) {
        let productElement = createProductElement(product);
        container.appendChild(productElement);
    });
}

// create product card
function createProductElement(product) {
    let productElement = document.createElement('div');
    productElement.classList.add('col-md-12', 'col-lg-4', 'mb-4', 'mb-lg-0');

    let card = document.createElement('div');
    card.classList.add('card');
    productElement.appendChild(card);

    let image = document.createElement('img');
    image.src = `${'static/img/uploads/' + product.image}`;
    image.classList.add('card-img-top');
    image.alt = `${product.name}`;
    card.appendChild(image);

    let cardBody = document.createElement('div');
    cardBody.classList.add('card-body');
    card.appendChild(cardBody);

    let div1 = document.createElement('div');
    div1.classList.add('d-flex', 'justify-content-between');
    cardBody.appendChild(div1);

    let category = document.createElement('p');
    category.classList.add('small');
    category.innerText = `${product.category.name}`;
    div1.appendChild(category);

    let div2 = document.createElement('div');
    div2.classList.add('d-flex', 'justify-content-between', 'mb-3');
    cardBody.appendChild(div2);

    let title = document.createElement('h5');
    title.classList.add('mb-0');
    title.innerText = `${product.name}`;
    div2.appendChild(title);

    let price = document.createElement('h5');
    price.classList.add('text-dark', 'mb-0');
    price.innerHTML = `${product.price} <span>&#x058f;</span>`;
    div2.appendChild(price);

    let div3 = document.createElement('div');
    div3.classList.add('d-flex', 'justify-content-between', 'mb-2');
    cardBody.appendChild(div3);

    let availability = document.createElement('p');
    availability.classList.add('text-muted', 'mb-0');
    if (product.amount) {
        availability.innerText = 'Առկա է';
    } else {
        availability.innerText = 'Առկա չէ';
    }
    div3.appendChild(availability);

    return productElement;
}
