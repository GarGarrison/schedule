import Vue from 'vue'
import axios from 'axios'
import moment from 'moment'

import Cell from './components/Cell.vue'
import Day from './components/Day.vue'
import MonthPicker from './components/MonthPicker.vue'
import TimePicker from './components/TimePicker.vue'
import { VueContext } from 'vue-context'

function responseProcess(response){
    if (response.data.status == "err") {
        alert("Error");
        console.log(response.data.msg);
    }
}

function catchProcess(response) {
    alert("Error");
    console.log(response);
}

var app = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data: {
        users: [],
        weeks: [],
        currentMonth: (new Date()).getMonth()+1,
        currentYear: (new Date()).getFullYear(),
        stat: [],
        statMonth: {},
        dutyUser: "",
        endOfDay: null,
        str_months: {
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
    },
    methods: {
        createDay: function(date, uid, weekend){
            var vm = this;
            axios.post("/admin/create_day", {"date": date, "uid": uid, "weekend": weekend})
                .then(function(response){
                    if (response.data.status == "err") {
                        alert("Error");
                        console.log(response.data.msg);
                        return;
                    }
                    vm.updateStat(vm.currentYear, vm.currentMonth);
                })
                .catch(catchProcess)
        },
        updateDay: function(date, uid, weekend){
            var vm = this;
            axios.post("/admin/update_day", {"date": date, "uid": uid, "weekend": weekend})
                .then(function(response){
                    if (response.data.status == "err") {
                        alert("Error");
                        console.log(response.data.msg);
                        return;
                    }
                    vm.updateStat(vm.currentYear, vm.currentMonth);
                })
                .catch(catchProcess)
        },
        updateStat: function(y, m){
            var vm = this;
            axios.get(`/update_stat/${y}/${m}`)
                .then(function(response){
                    console.log(response.data)
                    vm.stat = response.data.stat;
                    vm.statMonth = response.data.statMonth;
                })
                .catch(catchProcess)
        },
        toggleWeekend: function(date, val) {
            axios.post("/admin/toggle_weekend", {"date": date, "weekend": val})
                .then(responseProcess)
                .catch(catchProcess)
        },
        addHoliday: function(){
            console.log("add_holiday");
        },
        delHoliday: function(data){
            data.day.holiday = 0;
            axios.post("/admin/del_holiday", {"date": data.day.date, "uid": data.uid})
                .then(responseProcess)
                .catch(catchProcess)
        },
        getToday: function(){
            var d = new Date();
            return d.toISOString().split("T")[0];
        },
        parseDate: function(d){
            var l = d.split("-");
            return l[2] + "." + l[1] + "." + l[0].slice(2);
        },
        chooseMonth: function(y,m) {
            var vm = this;
            axios.get(`/update_month/${y}/${m}`)
                .then(function(response){
                    vm.updateStat(y, m);
                    vm.weeks = response.data.weeks;
                    vm.currentMonth = m;
                    vm.currentYear = y;
                })
                .catch(catchProcess)
        },
        changeLashHour: function(h){
            this.last_hour = h;
        },
        goHome: function(){
            var minutes = (moment(new Date()) - moment(this.endOfDay))/60000;
            minutes = Math.round(minutes);
            var hours = Math.round(minutes * 100/60) / 100;
            var q = confirm(`На счет поступит ${minutes} минут (${hours} часов)`);
            if (!q) return;
            axios.get(`/go_home/${this.dutyUser.id}/${minutes}`)
                .then(responseProcess)
                .catch(catchProcess)
        }
    },
    computed: {
        today: function(){
            return this.parseDate(this.getToday());
        },
        nowDate: function() {
            return new Date();
        }

    },
    created: function(){
        var vm = this;
        axios.get("/get_index_data")
                .then(function(response){
                    var du = response.data.dutyUser;
                    vm.users = response.data.users;
                    vm.weeks = response.data.weeks;
                    vm.stat = response.data.stat;
                    vm.statMonth = response.data.statMonth;
                    vm.endOfDay = moment(response.data.endOfDay);
                    vm.dutyUser = du ? vm.users[du] : {"name": "Никого", "phone": ""};
                })
                .catch(catchProcess)
    },
    components: {
        Cell,
        Day,
        MonthPicker,
        TimePicker,
        VueContext
    }
});