//
// const hallEl = document.getElementById('hall');
// const sessionId = hallEl.dataset.session;
//
// console.log(sessionId)
// 1. Получаем или создаём уникальный client_id


let clientId = localStorage.getItem('client_id');
const sessionID = document.getElementById('hall').dataset.session



const socket = new WebSocket(
    'ws://' + window.location.host + "/ws/booking/session/" + sessionID + '/'

);



/// onmessage дает ответ только когда бэкенд делает send ()
socket.onmessage = function (e) {
    const response = JSON.parse(e.data)
    const data = response.data;
    console.log('data with server',data)



    const seatBtn = document.querySelector(
        `[data-row="${data.row}"][data-seat="${data.seat}"]`);

    if (!seatBtn) return;

    if (data.action === 'cancel') {
        seatBtn.disabled = false;
        seatBtn.classList.remove('btn-info', 'btn-warning');
        seatBtn.classList.add('btn-outline-light');
        seatBtn.dataset.bookedByMe = 'false';
        return;
    }



    if (data.client_id === clientId) {
        seatBtn.disabled = false;
        seatBtn.classList.remove('btn-outline-light', 'btn-danger');
        seatBtn.classList.add('btn-info');
        seatBtn.dataset.bookedByMe = 'true';
    }

    else {
        seatBtn.disabled = false;
        seatBtn.classList.remove('btn-outline-light', 'btn-warning');
        seatBtn.classList.add('btn-warning');
        seatBtn.dataset.bookedByMe = 'false';
    }
}


document.querySelectorAll('.btn[data-row][data-seat]').forEach(function(button) {
    button.addEventListener('click', function() {

    let action;
    console.log(sessionID)

    if (this.dataset.bookedByMe === 'true') {
        action = 'cancel';
    }
    else {
        action = 'book';
    }

    console.log(action)

    socket.send(JSON.stringify({
        action: action,
        row: this.dataset.row,
        seat: this.dataset.seat,
        client_id: clientId,
        session_id:sessionID
    }));

});})



// const socket = new WebSocket(
//
//     "ws://" + window.location.host + "/ws/booking/session/" + sessionId + "/"
// );
//
// socket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     const seatBtn = document.querySelector(
//         `[data-row="${data.row}"][data-seat="${data.seat}"]`
//     );
//     if (seatBtn) {
//         seatBtn.disabled = true;
//         seatBtn.classList.remove('btn-outline-light');
//         seatBtn.classList.add('btn-danger');
//     }
// };
//
// document.querySelectorAll('.btn').forEach(button => {
//     button.addEventListener('click', function() {
//         const row = this.dataset.row;
//         const seat = this.dataset.seat;
//
//         // отправка на сервер
//         console.log('отправляю даннеые неа сервер - Косьтюмер' , row, seat)
//         socket.send(JSON.stringify({ row, seat}));
//
//         // визуально отмечаем
//         this.classList.add('btn-success');
//         this.classList.remove('btn-outline-light');
//     });
// });

// cookie_userr = document.cookie
// console.log(cookie_userr)
// document.querySelectorAll('.btn').forEach(function (button){
//         button.addEventListener('click', function (e) {
//
//             const Row= this.dataset.row
//             const SeatUser = this.dataset.seat
//             const DateSession = this.dataset.session
//             console.log(Row)
//             console.log(SeatUser)
//             console.log(DateSession)
//
//
//              // window.location.pathname = '/booking/'+ DateSession + SeatUser + Row+'/';
//
//
//
//             if (this.classList.contains('active')) {
//                 this.classList.remove('active')
//                 this.classList.remove('btn-success')
//                 this.classList.add('btn-outline-light')
//
//             }
//             else {
//                 this.classList.add('active');
//                 this.classList.remove('btn-outline-light')
//                 this.classList.add('btn-success')
//             }
//         })
//
//
//
//
// })
