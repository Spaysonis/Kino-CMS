


document.querySelectorAll('.btn').forEach(function (button){
    button.addEventListener('click', function (){

        console.log(this.dataset.row)
        console.log(this.dataset.seat)
    })
})