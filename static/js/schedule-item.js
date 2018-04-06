export default {
    ScheduleItem: Vue.component('schedule-item', {
        props: ['busLine'],
        template:
            `<section :class="classObject">
                <header>
                    <h2>{{busLine.line}}</h2>
                    <h3>{{busLine.terminus}}</h3>
                </header>
                <p>{{nextScheduleFormatted}}</p>
            </section>`,
        computed: {
            classObject() {
                return {
                    soon: 0 <= this.busLine.earliestArrival && this.busLine.earliestArrival <= 3,
                    imminent: 0 <= this.busLine.earliestArrival && this.busLine.earliestArrival <= 1,
                    unavailable: this.busLine.unavailable,
                    loading: this.busLine.earliestArrival < 0,
                    'real-time': this.busLine.isRealTime
                }
            },
            nextScheduleFormatted() {
                if (this.busLine.earliestArrival < 0)
                    return '...'
                if (this.busLine.earliestArrival < 1)
                    return '<1 min'
                return `${Math.floor(this.busLine.earliestArrival)} min`
            }
        }
    })
}