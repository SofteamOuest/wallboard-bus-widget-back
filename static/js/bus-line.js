export default class BusLine
{
    constructor(line, direction) {
        this.line = line
        this.direction = direction
        this.terminus = '...'
        this.next_arrivals = []
        this.isRealTime = false
    }

    get id() {
        return this.line + this.direction
    }

    get inbound() {
        if (this.next_arrivals.length == 0) return -1;
        return Math.min(...this.next_arrivals)
    }

    isSameAs(other) {
        return this.line == other.line
            && this.direction == other.direction
    }

    updateWith(schedule) {
        if (!this.isRealTime) { // real-time schedules are immutable
            this.terminus = schedule.terminus
            this.next_arrivals = schedule.next_arrivals
        }
        return this
    }

    markAsRealTime() {
        this.isRealTime = true
        return this
    }
}