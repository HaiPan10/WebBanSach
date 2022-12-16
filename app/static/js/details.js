function loadComments(productId){
    fetch(`/api/products/product_id=${productId}/comments`).then(res=>res.json()).then(data => {
        let h = ""
        data.forEach( c => {
            h += `
            <div class="comment-list">
                <div class="single-comment justify-content-between d-flex">
                    <div class="user justify-content-between d-flex">
                        <div class="thumb">
                            <img src="${c.user_account.avatar}" alt="">
                        </div>
                        <div class="desc">
                            <p class="comment">
                                ${c.content}
                            </p>
                            <div class="d-flex justify-content-between">
                                <div class="d-flex align-items-center">
                                    <h5>
                                        <a>${c.user_account.name}</a>
                                    </h5>
                                    <p class="date">${moment(c.created_date).locale("vi").fromNow()}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
          `
        })
        let d = document.getElementById("comments")
        d.innerHTML = h
    })
}

function addComment(productId) {
    fetch(`/api/products/product_id=${productId}/comments`, {
        method: "post",
        body: JSON.stringify({
            "content": document.getElementById("comment-content").value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.status === 204) {
            let c = data.comment

            let h = `
            <div class="comment-list">
                <div class="single-comment justify-content-between d-flex">
                    <div class="user justify-content-between d-flex">
                        <div class="thumb">
                            <img src="${c.user_account.avatar}" alt="">
                        </div>
                        <div class="desc">
                            <p class="comment">
                                ${c.content}
                            </p>
                            <div class="d-flex justify-content-between">
                                <div class="d-flex align-items-center">
                                    <h5>
                                        <a>${c.user_account.name}</a>
                                    </h5>
                                    <p class="date">${moment(c.created_date).locale("vi").fromNow()}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
          `
        let d = document.getElementById("comments")
        d.innerHTML = h + d.innerHTML
        } else
        alert("Hệ thống bị lỗi")
    })
    document.getElementById("comment-content").value = "";
}