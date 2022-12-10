let timer;

function addToCart(id, bookName, unitPrice, image, quantity, quantityInStocks){
    //console.info("hello")
    fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "book_name": bookName,
            "unit_price": unitPrice,
            "image": image,
            "quantity": quantity,
            "quantity_in_stocks": quantityInStocks
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
            //console.info(data)
            let d = document.getElementsByClassName('cart-counter')
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity
            //handle add to cart message in here
            popup(data);
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

        popup(data);
        let c = document.getElementById(`cart${productId}`)
        c.style.display = 'none'

        if(parseFloat(document.getElementById('total-amount').innerHTML) == 0){
            location.reload();
        }
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
        let money = new Intl.NumberFormat().format(parseInt(obj.value) * unitPrice)
        amount.innerText = `${money} VNĐ`
        popup(data);

    }).catch(err => console.info(err))
}

function pay() {
    fetch("/api/pay").then(res => res.json()).then(data => {
            if(data.status === 200)
                location.reload()
            else
                alert("Hệ thống đang bị lỗi!")
        })
}

function getInputQuantity(){
    let quantity = parseInt(document.getElementById('input-quantity').value)
    return quantity
}

$(function(){
    //code jquery in here for cart.js
    $(".input-number").on('change', function(event){
        if(parseInt($(this).val()) > parseInt($(this).attr("max"))){
            $(this).val(parseInt($(this).attr("max")))
        }
        else if (parseInt($(this).val()) <= 0){
            $(this).val(1)
        }
    })

})

function popup(data){
    $("#message").html(data.message.toLocaleString("en-US"))
    $(".cart_confirmation").hide();
    $(".cart_confirmation").fadeIn();
    timer = setTimeout(() => {
        $(".cart_confirmation").fadeOut();
    }, 1000);
}

$(document).ready(function(){
    $('.pop-up_click').click(function(){
        clearTimeout(timer);
        timer = null;
    });
})
