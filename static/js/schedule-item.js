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
                    soon: 0 <= this.busLine.inbound && this.busLine.inbound <= 3,
                    imminent: 0 <= this.busLine.inbound && this.busLine.inbound <= 1,
                    unavailable: this.busLine.unavailable,
                    loading: this.busLine.inbound < 0,
                    'real-time': this.busLine.isRealTime
                }
            },
            nextScheduleFormatted() {
                if (this.busLine.inbound < 0)
                    return '...'
                if (this.busLine.inbound < 1)
                    return '<1 min'
                return `${Math.floor(this.busLine.inbound)} min`
            }
        }
    })
}