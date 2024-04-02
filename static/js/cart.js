var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        if (user == 'AnonymousUser') {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload();
        });
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated');

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }
    console.log('CART:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

    location.reload();
}

// Display the star rating value
document.querySelectorAll('.rating-stars .star').forEach(star => {
    star.addEventListener('click', function() {
        const productId = this.closest('.product-rating').dataset.productId;
        const ratingValue = this.dataset.value;
        
        fetch('/update_star_rating/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                productId: productId,
                ratingValue: ratingValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.closest('.product-rating').querySelector('.star-rating').innerText = ratingValue;
            } else {
                console.error('Failed to update star rating');
            }
        })
        .catch(error => {
            console.error('Error updating star rating:', error);
        });
    });
});

// Display the click count
function updateClickCount(productId) {
    var url = '/update_click_count/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId }),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Click count updated successfully.');
        // Display the click count here (if necessary)
    })
    .catch((error) => {
        console.error('Error updating click count:', error);
    });
}
