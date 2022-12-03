const pg = document.getElementById("pagination");
const btnNextPg = document.querySelector("button.next-page");
const btnPrevPg = document.querySelector("button.prev-page");
const btnFirstPg = document.querySelector("button.first-page");
const btnLastPg = document.querySelector("button.last-page");
// when page load
// curPage.setAttribute('max', pages.value);
const valuePage = {
  truncate: true,
  curPage: page_index,
  numLinksTwoSide: 1,
  totalPages: page_count
};

pg.onclick = (e) => {
  const ele = e.target;

  if (ele.dataset.page) {
    const pageNumber = parseInt(e.target.dataset.page, 10);

    valuePage.curPage = pageNumber;
    pagination(valuePage);

    handleButtonLeft();
    handleButtonRight();
  }
};

// DYNAMIC PAGINATION
function pagination() {
    handleButtonLeft();
    handleButtonRight();
    const { totalPages, curPage, truncate, numLinksTwoSide: delta } = valuePage;

    const range = delta + 4; // use for handle visible number of links left side

    let render = "";
    let renderTwoSide = "";
    let dot = `<li class="pg-item"><a class="pg-link">...</a></li>`;
    let countTruncate = 0; // use for ellipsis - truncate left side or right side

    // use for truncate two side
    const numberTruncateLeft = curPage - delta;
    const numberTruncateRight = curPage + delta;

    let active = "";
    for (let pos = 1; pos <= totalPages; pos++) {
        active = pos === curPage ? "active" : "";

        // truncate
        if (totalPages >= 2 * range - 1 && truncate) {
        if (numberTruncateLeft > 3 && numberTruncateRight < totalPages - 3 + 1) {
            // truncate 2 side
            if (pos >= numberTruncateLeft && pos <= numberTruncateRight) {
                renderTwoSide += renderPage(pos, active);
            }
        } else {
            // truncate left side or right side
            if ((curPage < range && pos <= range) ||
                (curPage > totalPages - range && pos >= totalPages - range + 1) ||
                pos === totalPages ||
                pos === 1) {
                render += renderPage(pos, active);
            } else {
                countTruncate++;
                if (countTruncate === 1) render += dot;
            }
        }
        } else {
            // not truncate
            render += renderPage(pos, active);
        }
    }

    if (renderTwoSide) {
        renderTwoSide = renderPage(1) + dot +
            renderTwoSide + dot + renderPage(totalPages);
        pg.innerHTML = renderTwoSide;
    } else {
        pg.innerHTML = render;
    }
}

function renderPage(index, active = "") {
    let stringPath = "";
    let url = window.location.pathname;
    if(typeof categoryId === 'undefined'){
        stringPath = `${url}?page=${index}`;
    }
    else{
        stringPath = `${url}?category_id=${categoryId}&page=${index}`;
    }
    if(active === ""){
        return `<li class="pg-item ${active}" data-page="${index}">
            <a class="pg-link" href="${stringPath}">${index}</a></li>`;
    }
    else
        return `<li class="pg-item ${active}" data-page="${index}">
            <a class="pg-link" href="${stringPath}">${index}</a></li>`;
}

function handleCurPage() {
    if (+curPage.value > pages.value) {
        curPage.value = 1;
        valuePage.curPage = 1;
    } else {
        valuePage.curPage = parseInt(curPage.value, 10);
    }
}

function handleCheckTruncate() {
    const truncate = document.querySelector("input[type=radio]:checked");

    if (truncate.id === "enable") {
        valuePage.truncate = true;
    } else {
        if (pages.value > 1000) {
        let isTruncate = confirm(`Are you sure you want to render all the links? number of pages: ${pages.value}`);
            // true => disable truncate
            if (isTruncate) {
                valuePage.truncate = false;
            } else {
                valuePage.truncate = true;
                truncate.removeAttribute("checked");
                document.getElementById("enable").checked = true;
            }
        } else {
            valuePage.truncate = false;
        }
    }
}

function handleButton(element) {
    let isChange = false;
    if (element.classList.contains("first-page")) {
        valuePage.curPage = 1;
        isChange = true;
    } else if (element.classList.contains("last-page")) {
        valuePage.curPage = parseInt(page_count, 10);
        isChange = true;
    } else if (element.classList.contains("prev-page")) {
        valuePage.curPage--;
        handleButtonLeft();
        btnNextPg.disabled = false;
        btnLastPg.disabled = false;
        isChange = true;
    } else if (element.classList.contains("next-page")) {
        valuePage.curPage++;
        handleButtonRight();
        btnPrevPg.disabled = false;
        btnFirstPg.disabled = false;
        isChange = true;
    }
    if(isChange){
        pagination();
    }
    return isChange;
}
function handleButtonLeft() {
    // Xu ly khi toi nut cuoi ben tay trai
    if (valuePage.curPage === 1) {
        btnPrevPg.disabled = true;
        btnFirstPg.disabled = true;
    } else {
        btnPrevPg.disabled = false;
        btnFirstPg.disabled = false;
    }
}
function handleButtonRight() {
    // Xu ly khi nut toi trang cuoi ben phai
    if (valuePage.curPage === valuePage.totalPages) {
        btnNextPg.disabled = true;
        btnLastPg.disabled = true;
    } else {
        btnNextPg.disabled = false;
        btnLastPg.disabled = false;
    }
}

$(function(){
    $("#pagination").on('click' ,function(event){
        let a = $(this).children("li.pg-item.active").children("a.pg-link");
        window.location.href = a.attr("href");
    });
    $(".page-container").on('click', function(event){
        if(handleButton(event.target)){
            window.location.href = $("#pagination").children("li.pg-item.active").children("a.pg-link").attr("href");
        }
    })
});
