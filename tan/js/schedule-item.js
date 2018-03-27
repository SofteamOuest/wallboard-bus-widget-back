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
                    soon: 0 < this.busLine.next && this.busLine.next <= 3,
                    imminent: 0 < this.busLine.next && this.busLine.next <= 1,
                    unavailable: this.busLine.unavailable,
                    loading: this.busLine.next < 0
                }
            },
            nextScheduleFormatted() {
                if (this.busLine.next < 0)
                    return '...'
                if(this.busLine.next < 2)
                    return `${Math.floor(this.busLine.next)} min ${this.busLine.next % 1 > .5 ? 30 : ''}`
                return `${Math.floor(this.busLine.next)} min`
            }
        }
    })
}