import ScheduleItemTime from './schedule-item-time.js'

export default {
    ScheduleItem: Vue.component('schedule-item', {
        props: ['busLine'],
        template:
            `<article :class="classObject">
                <header>
                    <h2>{{busLine.line}}</h2>
                    <h3>{{busLine.terminus}}</h3>
                </header>
                <section>
                    <schedule-item-time
                        v-for="arrival in busLine.nextArrivals.slice(0, 3)"
                        :arrival="arrival">
                    </schedule-item-time>
                    <span v-if="busLine.unavailable">&#x2620;&#xFE0F;</span>
                </section>
            </article>`,
        computed: {
            classObject() {
                return {
                    soon: this.busLine.soon,
                    imminent: this.busLine.imminent,
                    unavailable: this.busLine.unavailable,
                    loading: this.busLine.loading,
                    'real-time': this.busLine.realTime
                }
            }
        }
    })
}