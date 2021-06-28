const modal = document.querySelector(".modal");
const modal1 = document.querySelector("#modal1");
const modal2 = document.querySelector("#modal2");

const authBtn = document.querySelector('#auth-btn')
const regBtn = document.querySelector('#reg-btn')
const modalContent = document.querySelector('.modal_content')
const close = document.querySelector('#modal1 .close');


authBtn.onclick = function(event) {
    modal1.style.display = "block";
}

regBtn.onclick = function(event) {
    modal2.style.display = "block";
}

close.onclick = function(event) {
    modal.style.display = "none";
}

