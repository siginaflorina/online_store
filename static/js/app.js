const addToCheckoutButtons = document.querySelectorAll('.add-to-checkout-button');
const addToFavoritesButtons = document.querySelectorAll('.add-to-favorites-button');

const getTotalQuantityLSProducts = () => {
    const lsListProducts = JSON.parse(localStorage.getItem('listProducts')) || []

    let totalQuantity = 0

    for(let idx = 0; idx < lsListProducts.length; idx++)
        totalQuantity += lsListProducts[idx].quantity

    return totalQuantity
}

const getLSProductQuantityById = (id) => {
    const lsListProducts = JSON.parse(localStorage.getItem('listProducts')) || []

    for(let idx = 0; idx < lsListProducts.length; idx++)
        if(lsListProducts[idx].id === id)
            return lsListProducts[idx].quantity

    return 0
}

const getLSProductIndexById = (id) => {
    const lsListProducts = JSON.parse(localStorage.getItem('listProducts')) || []

    for(let idx = 0; idx < lsListProducts.length; idx++) {
        if (lsListProducts[idx].id === id)
            return idx
    }
    return -1
}

addToFavoritesButtons.forEach(addToFavoritesButton =>
    addToFavoritesButton.addEventListener("click", (e) => {
        // cauta cel mai apropiat element cu clasa .card-container
        const cardContainer = e.target.closest('.card-container');
        // extract id-ul din elementul cu clasa .card-container
        const id = cardContainer.dataset.id;

        // apel POST catre backend, trimitem cu ajutorul lui id-ul produsului ce se vrea a fi adaugat la favorite
        fetch('/api/favorites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: id
            })
        })
            .then(response => response.json())
            .then(data => {
                if(data.messageType === 'success')
                    toastr.success(data.message)
            })
            .catch((error) => {
                console.log(error);
            });
    })
);

addToCheckoutButtons.forEach(addToCheckoutButton =>
    addToCheckoutButton.addEventListener("click", (e) => {
        const cardContainer = e.target.closest('.card-container');
        const id = cardContainer.dataset.id;

        fetch(`/api/product/${id}`)
            .then(response => response.json())
            .then((data) => {
                const lsListProducts = JSON.parse(localStorage.getItem('listProducts')) || [];

                const idx = getLSProductIndexById(data.id)

                if(idx === -1)
                    lsListProducts.push({...data, quantity: 1})
                else
                    lsListProducts[idx].quantity = getLSProductQuantityById(data.id) + 1

                localStorage.setItem('listProducts', JSON.stringify(lsListProducts));

                spanNumberOfCheckoutProducts.textContent = getTotalQuantityLSProducts().toString();

                toastr.success(`Produsul ${data.title} a fost adaugat in cos!`)
            })
            .catch((error) => {
                console.log(error);
            })
    })
);