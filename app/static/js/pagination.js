const pg = document.getElementById("pagination");
const btnNextPg = document.querySelector("button.next-page");
const btnPrevPg = document.querySelector("button.prev-page");
const btnFirstPg = document.querySelector("button.first-page");
const btnLastPg = document.querySelector("button.last-page");;
// when page load
// curPage.setAttribute('max', pages.value);
const valuePage = {
  truncate: true,
  curPage: 1,
  numLinksTwoSide: 1,
  totalPages: page_count
};
pagination();

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
        if (
          (curPage < range && pos <= range) ||
          (curPage > totalPages - range && pos >= totalPages - range + 1) ||
          pos === totalPages ||
          pos === 1
        ) {
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
    renderTwoSide =
      renderPage(1) + dot + renderTwoSide + dot + renderPage(totalPages);
    pg.innerHTML = renderTwoSide;
  } else {
    pg.innerHTML = render;
  }
}

function renderPage(index, active = "") {
    let url = window.location.pathname;
    let stringPath = null;
    if (!(index === "...")){
        stringPath = url + "?page=" + index;
    }
    return `<li class="pg-item  ${active}" href="${stringPath}" data-page="${index}">
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
      let isTruncate = confirm(
        `Are you sure you want to render all the links? number of pages: ${pages.value}`
      );
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

document.querySelector(".page-container").onclick = function (e) {
  handleButton(e.target);
};

function handleButton(element) {
  if (element.classList.contains("first-page")) {
    valuePage.curPage = 1;
  } else if (element.classList.contains("last-page")) {
    valuePage.curPage = parseInt(pages.value, 10);
  } else if (element.classList.contains("prev-page")) {
    valuePage.curPage--;
    handleButtonLeft();
    btnNextPg.disabled = false;
    btnLastPg.disabled = false;
  } else if (element.classList.contains("next-page")) {
    valuePage.curPage++;
    handleButtonRight();
    btnPrevPg.disabled = false;
    btnFirstPg.disabled = false;
  }
  pagination();
}
function handleButtonLeft() {
  if (valuePage.curPage === 1) {
    btnPrevPg.disabled = true;
    btnFirstPg.disabled = true;
  } else {
    btnPrevPg.disabled = false;
    btnFirstPg.disabled = false;
  }
}
function handleButtonRight() {
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
        let a = $(this).children("li.pg-item.active").children("a.pg-link")
        window.location.href = a.attr("href");
    });
});

