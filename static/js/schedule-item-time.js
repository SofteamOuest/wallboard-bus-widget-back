export default {
    ScheduleItemTime: Vue.component('schedule-item-time', {
        props: ['arrival'],
        template:
            `<p>{{nextScheduleFormatted}}</p>`,
        computed: {
            nextScheduleFormatted() {
                if (this.arrival < 0)
                    return '...'
                if (this.arrival < 1)
                    return '<1 min'
                return `${Math.floor(this.arrival)} min`
            }
        }
    })
}