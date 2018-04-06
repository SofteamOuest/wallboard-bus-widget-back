export default class BusLine
{
    constructor(line, direction) {
        this.line = line
        this.direction = direction
        this.terminus = '...'
        this.nextArrivals = []
        this.unavailable = false
        this.realTime = false
    }

    get id() {
        return this.line + this.direction
    }

    get earliestArrival() {
        if (this.nextArrivals.length == 0) return -1
        return Math.min(...this.nextArrivals)
    }

    get soon() {
        return 0 <= this.earliestArrival && this.earliestArrival <= 3
    }

    get imminent() {
        return 0 <= this.earliestArrival && this.earliestArrival <= 1
    }

    get loading() {
        return this.earliestArrival < 0 && !this.unavailable
    }

    isSameAs(other) {
        return this.line == other.line
            && this.direction == other.direction
    }

    updateWith(schedule) {
        if (!this.isRealTime) { // real-time schedules are immutable
            this.unavailable = schedule.unavailable
            if (!schedule.unavailable) {
                this.terminus = schedule.terminus
                this.nextArrivals = schedule.next_arrivals
            }
        }
        return this
    }

    markAsRealTime() {
        this.realTime = true
        return this
    }
}