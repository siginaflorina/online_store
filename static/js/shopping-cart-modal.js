const shoppingCartIcon = document.querySelector('.fa-shopping-cart');
const shoppingCartModal = document.querySelector(".shopping-cart-modal");
const middleContainer = document.querySelector(".shopping-cart-modal .middle-container");
const shoppingCartModalCloseButton = document.querySelector(".shopping-cart-modal .close-button");
const removeAllProductsButton = document.querySelector(".shopping-cart-modal .remove-all-products-button");
const spanNumberOfCheckoutProducts = document.querySelector("span.number-of-checkout-products");
const hrContainer = document.querySelector(".shopping-cart-modal .hr-container");
const bottomContainer = document.querySelector(".shopping-cart-modal .bottom-container");
const spanTotalProducts = document.querySelector(".shopping-cart-modal .total-products");
const spanTotalPrice = document.querySelector(".shopping-cart-modal .total-price");
const confirmButton = document.querySelector(".shopping-cart-modal .confirm-button");
const nextContainer = document.querySelector(".shopping-cart-modal .next-container");
const checkoutForm = document.querySelector(".shopping-cart-modal form");
const useUserAddressCheckbox = document.querySelector(".shopping-cart-modal form .checkbox-address-wrapper input");
const addressFormField = document.querySelector(".shopping-cart-modal form .address-form-field");
const addressTextArea = document.querySelector(".shopping-cart-modal form .form-field #address");
const messageTextArea = document.querySelector(".shopping-cart-modal form .form-field #message");

let lsListProducts = JSON.parse(localStorage.getItem("listProducts")) || [];

spanNumberOfCheckoutProducts.textContent = lsListProducts.reduce((totalQuantity, food) => totalQuantity += food.quantity, 0).toString();

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const formatNumber = (number) => new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(number);

const getIntegerPart = (number) => formatNumber(number).toString().split('.')[0]

const getDecimalPart = (number) => formatNumber(number).toString().split('.')[1]

const getProductHTML = (product) => {
    return `
        <div class="product-container" data-id=${product.id}>
            <div class="product-image">
                <img src="/static/images/products/${product.category}/${product.image}" alt="Poza produs">
            </div>
            <div class="product-details">
                <span class="product-name">${product.title}</span>
                <div class="product-rating">
                    <i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i><i class="far fa-star"></i>
                </div>
            </div>
            <div class="product-quantity">
                <button class="add-quantity-button">
                    +
                </button>
                <div class="quantity">
                    ${product.quantity}
                </div>
                <button class="remove-quantity-button">
                    -
                </button>
            </div>
            <div class="product-price">
                <span>
                    ${getIntegerPart(product.price)}
                    <sup>
                         ${getDecimalPart(product.price)}
                    </sup> Lei
                </span>
                <span class="remove-button">Sterge</span>
            </div>
        </div>`
};

const addRemoveEventListenersToButtons = () => {
    const allRemoveButtons = document.querySelectorAll(".shopping-cart-modal .product-container .remove-button");

    for(const removeButton of allRemoveButtons){
        removeButton.addEventListener("click", (e) => {
            const closestProductContainer = e.target.closest('.product-container');
            const productId = closestProductContainer.dataset.id;

            lsListProducts = JSON.parse(localStorage.getItem("listProducts"));
            lsListProducts = lsListProducts.filter((product) => product.id !== parseInt(productId));
            localStorage.setItem("listProducts", JSON.stringify(lsListProducts));
            spanNumberOfCheckoutProducts.textContent = lsListProducts.length.toString();

            generateContent();
        });
    }
};

const addAddQuantityEventListenersToButtons = () => {
    const allAddQuantityButtons = document.querySelectorAll(".shopping-cart-modal .product-container .add-quantity-button");

    for(const addQuantityButton of allAddQuantityButtons){
        addQuantityButton.addEventListener("click", (e) => {
            const closestProductContainer = e.target.closest('.product-container');
            const productId = closestProductContainer.dataset.id;

            lsListProducts = JSON.parse(localStorage.getItem("listProducts"));

            console.log(lsListProducts);

            for(let idx = 0; idx < lsListProducts.length; idx++)
                if(lsListProducts[idx].id === parseInt(productId))
                    lsListProducts[idx].quantity++;

            localStorage.setItem("listProducts", JSON.stringify(lsListProducts));

            generateContent();
        });
    }
};

const addRemoveQuantityEventListenersToButtons = () => {
    const allRemoveQuantityButtons = document.querySelectorAll(".shopping-cart-modal .product-container .remove-quantity-button");

    for(const removeQuantityButton of allRemoveQuantityButtons){
        removeQuantityButton.addEventListener("click", (e) => {
            const closestProductContainer = e.target.closest('.product-container');
            const productId = closestProductContainer.dataset.id;

            lsListProducts = JSON.parse(localStorage.getItem("listProducts"));

            for(let idx = 0; idx < lsListProducts.length; idx++)
                if(lsListProducts[idx].id === parseInt(productId))
                    if(lsListProducts[idx].quantity > 1)
                        lsListProducts[idx].quantity--;

            localStorage.setItem("listProducts", JSON.stringify(lsListProducts));

            generateContent();
        });
    }
};

const generateContent = () => {
    const lsListProducts = JSON.parse(localStorage.getItem("listProducts")) || [];

    if(lsListProducts.length === 0) {
        middleContainer.innerHTML = '<p class="no-products-text">Nu este niciun produs in cos</p>';
        removeAllProductsButton.style.display = "none";
        hrContainer.style.display = "none";
        bottomContainer.style.display = "none";
    }
    else
    {
        let nrProducts = 0;
        let totalPrice = 0;
        let productsHTML = "";

        for(const product of lsListProducts) {
            productsHTML += getProductHTML(product);
            nrProducts += product.quantity;
            totalPrice += product.price * product.quantity;
        }

        totalPrice = formatNumber(totalPrice);

        middleContainer.innerHTML = productsHTML;
        removeAllProductsButton.style.display = "block";
        hrContainer.style.display = "flex";
        bottomContainer.style.display = "flex";
        spanTotalProducts.textContent = `${nrProducts} produse`;
        spanTotalPrice.innerHTML = `
            ${getIntegerPart(totalPrice)}
            <sup>
                ${getDecimalPart(totalPrice)}
            </sup> Lei
        `;

        addRemoveEventListenersToButtons();
        addAddQuantityEventListenersToButtons();
        addRemoveQuantityEventListenersToButtons();

        spanNumberOfCheckoutProducts.textContent = nrProducts.toString();
    }
}

const removeAllProducts = () => {
    localStorage.setItem("listProducts", JSON.stringify([]));
    spanNumberOfCheckoutProducts.textContent = "0";
    nextContainer.style.display = 'none';
    generateContent();
}

window.onclick = function(event) {
    if (event.target === shoppingCartModal) {
        shoppingCartModal.style.display = "none";
    }
};

shoppingCartIcon.addEventListener("click", function(e){
    e.preventDefault();

    generateContent();

    shoppingCartModal.style.display = "flex";
});

removeAllProductsButton.addEventListener("click", removeAllProducts);

shoppingCartModalCloseButton.addEventListener("click", function(){
    shoppingCartModal.style.display = "none"
});

confirmButton.addEventListener("click", () => {

   nextContainer.style.display = "block";
});

useUserAddressCheckbox.addEventListener("change", (e) => {
    if(e.target.checked)
        addressFormField.style.display = 'none';
    else
        addressFormField.style.display = 'flex';
});

checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const data = {
        products: [],
        useUserAddress: useUserAddressCheckbox.checked,
        address: addressTextArea.value,
        message: messageTextArea.value.length > 0 ? messageTextArea.value : null
    }

    const productContainers = document.querySelectorAll('.shopping-cart-modal .product-container')

    for(const productContainer of productContainers){
        const id = productContainer.dataset.id;
        const quantityDiv = productContainer.querySelector('.quantity');
        const nr = parseInt(quantityDiv.textContent);
        data.products.push({
            id,
            nr
        })
    }

    fetch('/api/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
        .then((response) => response.json())
        .then((data) => {
            if(data.messageType === 'success') {
                removeAllProducts()
                shoppingCartModal.style.display = 'none';
                toastr.success(data.message)
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});