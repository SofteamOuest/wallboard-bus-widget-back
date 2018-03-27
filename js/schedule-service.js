function getSchedule(busLines) {
    return new Promise((resolve, _) => {
            let endPoint = getTheoreticalScheduleEndpoint(busLines)
            fetch(endPoint)
                .then(response => response.json())
                .then(response => resolve(response))
        })
}

const STOP = 'IDNA'
const API = 'http://localhost:5000'
// const API = '/tan/theoretical.json#'

function getTheoreticalScheduleEndpoint(busLines) {
    let lines = new Set(busLines.map(b => `line=${b.line}`))
    let q = [...lines].join('&')
    return `${API}/theoretical?stop=${STOP}&${q}`
}

export default { 
    getSchedule
}