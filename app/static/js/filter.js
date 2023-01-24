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
    $("#searchInput").on("keyup", function() {
        searchValue = $(this).val();
        filterProducts(selectedCategoryId, selectedAvailability, searchValue);
    });
});

// get filtered products
function filterProducts(categoryId, availability, search) {
    $.ajax({
        type: "GET",
        url: "/filter-products",
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
    let container = document.querySelector('.box-container');
    container.innerHTML = '';

    products.forEach(function(product) {
        let productElement = createProductElement(product);
        container.appendChild(productElement);
    });
}

// create product card
function createProductElement(product) {
    // Create a container element for the product
    const productElement = document.createElement("div");
    productElement.classList.add("box");

    // Create a span element for the availability status
    const availability = document.createElement("span");
    if (product.amount) {
        availability.classList.add("available");
    } else {
        availability.classList.add("not-available");
    }
    productElement.appendChild(availability);

    // Create a div element for the product image
    const imageContainer = document.createElement("div");
    imageContainer.classList.add("image");
    const image = document.createElement("img");
    image.src = 'static/img/default_image.jpg';
    if (product.image) {
        image.src = `${'static/img/uploads/' + product.image}`;
    }
    imageContainer.appendChild(image);
    productElement.appendChild(imageContainer);

    // Create a div element for the product details
    const textContainer = document.createElement("div");
    textContainer.classList.add("text");

    // Create a h5 element for the category name
    const category = document.createElement("h5");
    category.innerText = product.category.name;
    textContainer.appendChild(category);

    // Create a h3 element for the product name
    const name = document.createElement("h3");
    name.innerText = product.name;
    textContainer.appendChild(name);

    // Create a div element for the product price
    const price = document.createElement("div");
    price.classList.add("price");
    price.innerHTML = `${product.price} &#x058f;`;
    textContainer.appendChild(price);

    productElement.appendChild(textContainer);

    return productElement;
}
