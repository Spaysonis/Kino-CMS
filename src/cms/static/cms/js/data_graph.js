
console.log(typeof $.fn.vectorMap);



$('#vmap').vectorMap({ map: 'ukraine_ua' });

console.log(window.chartLabels)
console.log(window.scheduleData)
console.log(window.visitorData)
console.log(window.desktopTabletData)
console.log(window.MobileDesktopData)
console.log(window.MobileData)

let ctx = document.getElementById('line-chart').getContext('2d');
const lineChart = new Chart(ctx, {
    type: 'line', // именно линейный график
    data: {
        labels: window.chartLabels, // подписи по оси X
        datasets: [{
            label: 'Сеансы',               // подпись линии
            data: window.scheduleData, // данные
            borderColor: '#ffffff',         // цвет линии
            backgroundColor: 'rgba(255,255,255,0.2)', // цвет заливки под линией
            fill: true                      // включить заливку
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true, labels: { color: '#fff' } }
        },
        scales: {
            x: {
                ticks: {
            color: '#fff',
            autoSkip: true,
            maxTicksLimit: 7
        }
            },

            y: { ticks: { color: '#fff' } }
        }
    }
});



let ctxVisitors = document.getElementById('visitors-chart').getContext('2d');

const Visitor = new Chart(ctxVisitors, {
     type: 'line', // именно линейный график
    data: {
        labels: window.chartLabels, // подписи по оси X
        datasets: [{
            label: 'Все пользователи',
            data: window.visitorData, // данные
            borderColor: '#063778',         // цвет линии
            backgroundColor: 'rgba(255,255,255,0.2)', // цвет заливки под линией
            fill: true                      // включить заливку
        }, {
            label: 'Планшеты и обычные ПК',
            data: window.desktopTabletData, // данные
            borderColor: '#f36532',         // цвет линии
            backgroundColor: 'rgba(255,255,255,0.2)', // цвет заливки под линией
            fill: true                      // включить заливку
        }, {
            label: 'Мобильные устройства',
            data: window.MobileData, // данные
            borderColor: '#22b83e',         // цвет линии
            backgroundColor: 'rgba(255,255,255,0.2)', // цвет заливки под линией
            fill: true                      // включить заливку
            }, {
            label: 'Смартфоны и ПК',
            data: window.MobileDesktopData, // данные
            borderColor: '#981ac1',         // цвет линии
            backgroundColor: 'rgba(255,255,255,0.2)', // цвет заливки под линией
            fill: true                      // включить заливку

            }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true, labels: { color: '#000000' } }
        },
        scales: {
            x: { ticks: { color: '#fff' },
            display:false
            },
            y: { ticks: { color: '#000000' },
            display:false}
        }
    }
});