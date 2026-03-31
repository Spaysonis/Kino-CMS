function generateSimpleId() {
    return 'client-' + Math.random().toString(36).substring(2, 11) + '-' + Date.now();
}

const hallEl = document.getElementById('hall');
const sessionID = hallEl ? hallEl.dataset.session : null;

let clientId = localStorage.getItem('client_id');
if (!clientId) {
    clientId = generateSimpleId();
    localStorage.setItem('client_id', clientId);
}

if (sessionID) {
    const socket = new WebSocket(
        'ws://' + window.location.host + "/ws/booking/session/" + sessionID + '/'
    );

    socket.onmessage = function (e) {
        const response = JSON.parse(e.data);
        let data = response.data;

        if (!Array.isArray(data)) {
            data = [data];
        }

        data.forEach(function (seatInfo) {
            const seatBtn = document.querySelector(
                `button[data-row="${seatInfo.row}"][data-seat="${seatInfo.seat}"]`
            );
            if (!seatBtn) return;

            if (seatInfo.action === 'disable') {
                seatBtn.classList.remove("btn-outline-light", "btn-info", "btn-warning");
                seatBtn.classList.add("btn-danger");
                seatBtn.dataset.bookedByMe = 'false';
                seatBtn.disabled = true;
                return;
            }

            if (seatInfo.action === "ready_to_buy") {
                seatBtn.dataset.bookedByMe = 'true';
                seatBtn.classList.remove('btn-outline-light', 'btn-info');
                seatBtn.classList.add("btn-warning");
                seatBtn.disabled = true;
            }

            if (seatInfo.action === 'cancel') {
                seatBtn.disabled = false;
                seatBtn.classList.remove('btn-info', 'btn-warning', 'btn-danger');
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
        });
    };

    document.querySelectorAll('.btn[data-row][data-seat]').forEach(function(button) {
        button.addEventListener('click', function() {
            let action = (this.dataset.bookedByMe === 'true') ? 'cancel' : 'ready_to_buy';
            
            socket.send(JSON.stringify({
                action: action,
                row: this.dataset.row,
                seat: this.dataset.seat,
                client_id: clientId,
                session_id: sessionID
            }));
        });
    });
}

function getSelectedSeats() {
    const seats = [];
    document.querySelectorAll('button[data-row][data-seat]').forEach(btn => {
        if (btn.dataset.bookedByMe === 'true') {
            seats.push({ row: btn.dataset.row, seat: btn.dataset.seat });
        }
    });
    return seats;
}

function confirmBookingOrPurchase(action) {
    const seats = getSelectedSeats();
    if (seats.length === 0 || !sessionID) {
        if (seats.length === 0) alert('Выберите места для действия');
        return;
    }

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    fetch(`/sessions/${sessionID}/confirm/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
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
    });
}

const bookingBtn = document.querySelector('button[value="booking"]');
if (bookingBtn) {
    bookingBtn.addEventListener('click', () => {
        confirmBookingOrPurchase('booking');
    });
}