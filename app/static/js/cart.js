function addToCart(id, bookName, unitPrice, image){
    //console.info("hello")
    console.info(id);
    console.info(bookName)
    console.info(unitPrice)
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
            //console.info(data)
//            let d = document.getElementsByClassName('cart-counter')
//            for (let i = 0; i < d.length; i++)
//                d[i].innerText = data.total_quantity
        })
}