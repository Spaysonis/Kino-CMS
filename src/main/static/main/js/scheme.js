

cookie_userr = document.cookie
console.log(cookie_userr)
document.querySelectorAll('.btn').forEach(function (button){
        button.addEventListener('click', function (e) {

            const Row= this.dataset.row
            const SeatUser = this.dataset.seat
            const DateSession = this.dataset.session
            console.log(Row)
            console.log(SeatUser)
            console.log(DateSession)


             // window.location.pathname = '/booking/'+ DateSession + SeatUser + Row+'/';
             window.location.pathname = '/booking/'+ 'session/'+ DateSession +'/seat/'+ SeatUser + '/row/' + Row+'/';


            if (this.classList.contains('active')) {
                this.classList.remove('active')
                this.classList.remove('btn-success')
                this.classList.add('btn-outline-light')

            }
            else {
                this.classList.add('active');
                this.classList.remove('btn-outline-light')
                this.classList.add('btn-success')
            }
        })




})