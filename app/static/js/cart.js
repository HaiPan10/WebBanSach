function addToCart(id, bookName, unitPrice, image){
    //console.info("hello")
    fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "book_name": bookName,
            "unit_price": unitPrice,
            "image": image
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
            console.info(data)
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity
        })
}

function deleteCart(productId){
    fetch(`/api/cart/${productId}`, {
        method: "delete"
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")

        let c = document.getElementById(`cart${productId}`)
        c.style.display = 'none'
    }).catch(err => console.info(err))
}

function updateCart(productId, obj, unitPrice){
fetch(`/api/cart/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value,
            "unit_price": unitPrice
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter')
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName('cart-amount')
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")

        let amount = document.getElementById(`cart${productId}-amount`)
        console.log(amount)
        amount.innerText = parseInt(obj.value) * unitPrice


    }).catch(err => console.info(err))
}