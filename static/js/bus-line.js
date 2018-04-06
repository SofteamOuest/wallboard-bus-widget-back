export default class BusLine
{
    constructor(line, direction) {
        this.line = line
        this.direction = direction
        this.terminus = '...'
        this.nextArrivals = []
        this.unavailable = false
        this.isRealTime = false
    }

    get id() {
        return this.line + this.direction
    }

    get earliestArrival() {
        if (this.nextArrivals.length == 0) return -1;
        return Math.min(...this.nextArrivals)
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
        this.isRealTime = true
        return this
    }
}