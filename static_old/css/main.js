let menu = document.querySelector('#menu-bar');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}

let slides = document.querySelectorAll('.slide-container');
let index = 0;

function next() {
    slides[index].classList.remove('active');
    index = (index + 1) % slides.length;
    slides[index].classList.add('active');
}

function prev() {
    slides[index].classList.remove('active');
    index = (index - 1 + slides.length) % slides.length;
    slides[index].classList.add('active');
}

$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this
    console.log(id)
    $.ajax({
        type:"GET",
        url: "/removecart",
        data:{
            prod_id: id
        },
        success: function(data){
            console.log(data)
            document.getElementById("amount").innerHTML = data.amount
            document.getElementById("total").innerHTML = data.total
        }
    })
})