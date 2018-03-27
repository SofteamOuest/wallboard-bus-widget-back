export default class BusLine
{
    constructor(line, direction) {
        this.id = line + direction
        this.line = line
        this.direction = direction
        this.terminus = '...'
        this.next = -1
    }

    sameAs(other) {
        return this.line == other.line
            && this.direction == other.direction
    }

    updateWith(schedule) {
        this.terminus = schedule.terminus
        this.next = schedule.next
    }
}