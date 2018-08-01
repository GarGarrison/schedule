<template>
    <div class="date_picker">
        <input class="menu_item" @click="toggle()" @blur="toggle()" :value="`${m} ${currentYear}`">
        <div class="calendar" v-show="show">
            <div class="year_picker">
                <i class="material-icons" @mousedown.prevent="minus">keyboard_arrow_left</i>
                {{ currentYear }}
                <i class="material-icons" @mousedown.prevent="plus">keyboard_arrow_right</i>
            </div>
            <div class="month_picker">
                <div class="month_row">
                    <div class="month" :class="{active: currentMonth==1}" @mousedown="choose(1)">Янв</div>
                    <div class="month" :class="{active: currentMonth==2}" @mousedown="choose(2)">Фев</div>
                    <div class="month" :class="{active: currentMonth==3}" @mousedown="choose(3)">Мар</div>
                    <div class="month" :class="{active: currentMonth==4}" @mousedown="choose(4)">Апр</div>
                </div>
                <div class="month_row">
                    <div class="month" :class="{active: currentMonth==5}" @mousedown="choose(5)">Май</div>
                    <div class="month" :class="{active: currentMonth==6}" @mousedown="choose(6)">Июн</div>
                    <div class="month" :class="{active: currentMonth==7}" @mousedown="choose(7)">Июл</div>
                    <div class="month" :class="{active: currentMonth==8}" @mousedown="choose(8)">Авг</div>
                </div>
                <div class="month_row">
                    <div class="month" :class="{active: currentMonth==9}" @mousedown="choose(9)">Сен</div>
                    <div class="month" :class="{active: currentMonth==10}" @mousedown="choose(10)">Окт</div>
                    <div class="month" :class="{active: currentMonth==11}" @mousedown="choose(11)">Ноя</div>
                    <div class="month" :class="{active: currentMonth==12}" @mousedown="choose(12)">Дек</div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        data: function() {
            return {
                show: false,
                currentYear: 0,
                currentMonth: 0,
                months: {
                    1: "Январь",
                    2: "Февраль",
                    3: "Март",
                    4: "Апрель",
                    5: "Май",
                    6: "Июнь",
                    7: "Июль",
                    8: "Август",
                    9: "Сентябрь",
                    10: "Октябрь",
                    11: "Ноябрь",
                    12: "Декабрь"
                }
            }
        },
        computed: {
            m: function(){
                return this.months[this.currentMonth];
            }
        },
        mounted: function(){
            var d = new Date();
            this.currentYear = d.getFullYear();
            this.currentMonth = d.getMonth()+1;
        },
        methods: {
            plus: function(){
                this.currentYear ++;
            },
            minus: function(){
                this.currentYear --;
            },
            choose: function(i) {
                this.currentMonth = i;
                this.$root.chooseMonth(this.currentYear, i);
            },
            toggle: function(){
                this.show = !this.show;
            }
        }
    }
</script>
<style>
    .date_picker {
        position: relative;
    }
    .year_picker {
        text-align: center;
        padding: 10px 0px;
        font-weight: bold;
        font-size: 20px;
        background: #eb6767;
    }
    .year_picker i:first-child {
        float: left;
        cursor: pointer;
    }
    .year_picker i:last-child {
        float: right;
        cursor: pointer;
    }
    .month_row {
        display: inline-block;
    }
    .month {
        width: 25%;
        cursor: pointer;
    }
    .month:hover {
        background: #e5e5e5;
    }
    .calendar {
        position: absolute;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
        border-radius: 10px;
        top: 0;
        background: white;
        overflow: hidden;
        z-index: 10;
    }
    .month {
        padding: 10px;
        float: left;
    }
    .month.active {
        background: #dff0d8;
    }
</style>