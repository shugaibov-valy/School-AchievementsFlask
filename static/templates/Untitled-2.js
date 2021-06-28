const modal = document.querySelector(".modal")
const openButton = document.querySelector('.modal-button_open')
const closeButton = document.querySelector('.modal-button_close')
const modalContent = document.querySelector('.modal_content')

function toggleModal(e) {
    console.log(e.target.classList.contains('.modal'));
    modal.classList.toggle('modal_active')
}

openButton.addEventListener('click', toggleModal)
modal.addEventListener('click', toggleModal)
modalContent.addEventListener('click', function(e){
    e.stopPropagation()
})
