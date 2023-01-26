let products;

// get selected category
$(document).ready(function() {
    // set as default value on page load
    $('#searchInput').val('');
    $('#availabilitySelect').val('0').prop('checked', false);

    let selectedCategoryId;
    let selectedAvailability;
    let searchValue;

    $('#categorySelect .option').on('click', function() {
        selectedCategoryId = $(this).find('input').val();
        filterProducts(selectedCategoryId, selectedAvailability, searchValue);
    });
    $('#availabilitySelect').on('change', function() {
        selectedAvailability = $(this).prop('checked') ? '1' : '0';
        filterProducts(selectedCategoryId, selectedAvailability, searchValue);
    });
    $('#searchInput').on('keyup', function() {
        searchValue = $(this).val();
        filterProducts(selectedCategoryId, selectedAvailability, searchValue);
    });
});

// get filtered products
function filterProducts(categoryId, availability, search) {
    $.ajax({
        type: 'GET',
        url: '/filter-products',
        data: {
            category_id: categoryId,
            availability: availability,
            search: search
        },
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
    // Create a container element for the product
    const productElement = document.createElement('div');
    productElement.classList.add('column');

    // Create the card element
    const card = document.createElement('div');
    card.classList.add('card');
    productElement.appendChild(card);

    // Create a span element for the availability status
    const availability = document.createElement('span');
    if (product.amount) {
        availability.classList.add('available');
    } else {
        availability.classList.add('not-available');
    }
    card.appendChild(availability);

    // Create the image element
    const image = document.createElement('img');
    image.classList.add('card-img-top');
    image.style.width = '100%';
    image.alt = product.name;
    if (product.image) {
        image.src = `static/img/uploads/${product.image}`;
    } else {
        image.src = 'static/img/default_image.jpg';
    }
    card.appendChild(image);

    // Create the category element
    const category = document.createElement('p');
    category.innerText = product.category.name;
    card.appendChild(category);

    // Create the name element
    const name = document.createElement('h1');
    name.innerText = product.name;
    card.appendChild(name);

    // Create the price element
    const price = document.createElement('p');
    price.classList.add("price");
    price.innerHTML = `${product.price} &#x058f;`;
    card.appendChild(price);

    return productElement;
}
