<template>
    <div class="day" :class="{weekend: day.weekend, past: checkPast}">
        <div class="cell head" 
                @dblclick="changeWeekend"
                :class="{today: checkToday}">{{ parsedVal }}
        </div>
        <cell v-for="user, index in dataUsers"
            @updateduty="updateDuty"
            :day="day"
            :uid="user.id"
            :past="checkPast"
            :key="index"
            >
        </cell>
    </div>
</template>
<script>
    import Cell from './Cell.vue'
    export default {
        props: ["data-users", "data-day"],
        data: function() {
            return {
                day: this.dataDay
            }
        },
        methods: {
            updateDuty: function(new_uid){
                if (this.day.uid == 0) this.$root.createDay(this.day.date, new_uid, this.day.weekend);
                else this.$root.updateDay(this.day.date, new_uid, this.day.weekend);
                this.day.uid = new_uid;
            },
            changeWeekend: function(){
                this.day.weekend = !this.day.weekend;
                this.$root.toggleWeekend(this.day.date, this.day.weekend);
            }
        },
        computed: {
            parsedVal: function(){
                return this.$root.parseDate(this.day.date);
            },
            checkPast: function(){
                var d = new Date();
                var today = d.toISOString().split("T")[0];
                return this.day.date < today;
            },
            checkToday: function(){
                var today = this.$root.getToday();
                return this.day.date == today;
            },
        },
        watch: {
            dataDay: function(newDataDay) {
                this.day = newDataDay;
            }
        },
        components: {
            Cell
        }
    }
</script>