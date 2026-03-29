//
// const hallEl = document.getElementById('hall');
// const sessionId = hallEl.dataset.session;
//
// console.log(sessionId)
// 1. при конекте к веб сокету я получаю данные с бэжкенда
// 2. при отправвкее данных на бэк я их там обрабатываю и вывожу на фронтенд






function generateSimpleId() {
    return 'client-' + Math.random().toString(36).substring(2, 11) + '-' + Date.now();
}

// 2. Получаем или создаем clientId
let clientId = localStorage.getItem('client_id');
if (!clientId) {
    clientId = generateSimpleId(); // Используем нашу функцию вместо crypto.randomUUID()
    localStorage.setItem('client_id', clientId);
}


const socket = new WebSocket(
    'ws://' + window.location.host + "/ws/booking/session/" + sessionID + '/'

);


/// onmessage дает ответ только когда бэкенд делает send ()
socket.onmessage = function (e) {
    const response = JSON.parse(e.data)
    console.log(response.type)
    let data = response.data;

    console.log(data)
    if (!Array.isArray(data)) {
        data = [data];
    }
    data.forEach(function (seatInfo) {
         const seatBtn = document.querySelector(
            `button[data-row="${seatInfo.row}"][data-seat="${seatInfo.seat}"]`
        );
         if (!seatBtn) return;

         if(seatInfo.action === 'disable') {
             seatBtn.classList.remove("btn-outline-light")
             seatBtn.classList.add("btn-danger")
             seatBtn.dataset.bookedByMe = 'false';
             seatBtn.disabled = true;
             return;
         }


         if (seatInfo.action === "ready_to_buy") {
             seatBtn.dataset.bookedByMe = 'true';
             seatBtn.classList.remove('btn-outline-light')
             seatBtn.classList.add("btn-warning");
             seatBtn.disabled = true;
         }

         if (seatInfo.action === 'cancel') {
             console.log(seatInfo.action)
            seatBtn.disabled = false;
            seatBtn.classList.remove('btn-info', 'btn-warning');
            seatBtn.classList.add('btn-outline-light');
            seatBtn.dataset.bookedByMe = 'false';
            return;
        }

        if (seatInfo.client_id === clientId) {
            seatBtn.disabled = false;
            seatBtn.classList.remove('btn-outline-light', 'btn-warning');
            seatBtn.classList.add('btn-info');
            seatBtn.dataset.bookedByMe = 'true';
        }



        })}



document.querySelectorAll('.btn[data-row][data-seat]').forEach(function(button) {
    button.addEventListener('click', function() {

    let action;

    if (this.dataset.bookedByMe === 'true') {
        action = 'cancel';
    }
    else {
        action = 'ready_to_buy';
    }
    console.log('send socket' , action)
    socket.send(JSON.stringify({
        action: action,
        row: this.dataset.row,
        seat: this.dataset.seat,
        client_id: clientId,
        session_id:sessionID
    }));

});})

/// эта функция собирает места и ряды
function getSelectedSeats() {
    // всегда собираем актуальные данные с DOM
    const seats = [];
    document.querySelectorAll('button[data-row][data-seat]').forEach(btn => {
        if (btn.dataset.bookedByMe === 'true') {
            seats.push({ row: btn.dataset.row, seat: btn.dataset.seat });
        }
    });
    return seats; // возвращаем актуальный массив
}

// -------------
/// эта функция передает на бэкенд данные о местах и юзере

function confirmBookingOrPurchase(action) {
     const seats = getSelectedSeats();
     if (seats.length === 0) {
        alert('Выберите места для действия');
        return;
    }
     fetch(`/sessions/${sessionID}/confirm/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            action: action,
            seats: seats
        })
     })
         .then(res => res.json())
         .then(data => {
             if (data.success) {
                 console.log(data);
             }

         })

}



document.querySelector('button[value="booking"]').addEventListener('click', () => {
    confirmBookingOrPurchase('booking');
});

