"use strict"
console.log("cart")
const updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function (e)  {
        e.preventDefault()
        const productId = this.dataset.product
        const action = this.dataset.action
        const quantity = parseInt(document.getElementById("quantity").value)

        console.log('Product:', productId, 'Quantity', quantity, 'Action:', action)
        console.log('USER', user)
        if (user === "AnonymousUser") {
            console.log("Not log in")
        } else {
            console.log("Authorized")

            updateCart(productId, quantity, action)
        }
    })
}


function updateCart(productId, quantity, action){
    console.log("User is logged in.")
    const url = '/cart/'
    let method = ''
    let object = {
        ProductId:productId,
        Quantity:quantity,
        Action: action
    }

    switch (action){
        case 'remove':
            method = 'DELETE'
            break;
        case 'update':
            method = 'PUT'
            break
        case 'add':
            method = 'POST'
            break
        default:
            method = 'GET'
    }

    const obj = {
        ProductId:productId,
        Quantity:quantity,
        Action: action
    }

    const data = {
        method: method,
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(obj)
    }

    fetch(url, data)
        .then(res => {
            return res.json()
        })
        .then(data => {
            console.log('data', data)
            // need to be fixed
            location.reload()
        })
}