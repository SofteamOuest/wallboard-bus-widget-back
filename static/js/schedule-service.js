function getSchedule(endPoint) {
    return new Promise((resolve, reject) => {
            fetch(endPoint)
                .then(response => response.json())
                .then(response => resolve(response))
                .catch(error => reject(error))
        })
}

function getTheoreticalSchedule(busLines) {
    let endPoint = getTheoreticalScheduleEndpoint(busLines)
    return getSchedule(endPoint)
}

function getRealTimeSchedule(busLines) {
    let endPoint = getRealTimeScheduleEndpoint()
    return getSchedule(endPoint)
}

const STOP = 'IDNA'
// const API = 'http://127.0.0.1:5000'
// const API = '/tan/theoretical.json#'
const API = ''

function getTheoreticalScheduleEndpoint(busLines) {
    let lines = new Set(busLines.map(b => `line=${b.line}`))
    let q = [...lines].join('&')
    return `${API}/theoretical?stop=${STOP}&${q}`
}

function getRealTimeScheduleEndpoint() {
    return `${API}/real_time?stop=${STOP}`
}

export default { 
    getTheoreticalSchedule,
    getRealTimeSchedule
}