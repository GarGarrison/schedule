import Vue from 'vue'
import axios from 'axios'

import {ru} from 'vuejs-datepicker/dist/locale'
import Datepicker from 'vuejs-datepicker';

var validation_rules = {
    holiday: {
        from: {
            msg: "Заполните дату начала"
        },
        till: {
            msg: "Заполните дату конца"
        }, 
        uid: {
            msg: "Укажите пользователя"
        }
    },
    add_user: {
        auth_id: {
            msg: "Укажите auth_id"
        },
        name: {
            msg: "Укажите имя"
        }, 
        phone: {
            msg: "Укажите телефон"
        }
    },
    edit_user: {
        id: {
            msg: "Укажите пользователя"
        },
        auth_id: {
            msg: "Укажите auth_id"
        },
        name: {
            msg: "Укажите имя"
        }, 
        phone: {
            msg: "Укажите телефон"
        }
    },
    edit_hours: {
        id: {
            msg: "Укажите пользователя"
        },
        count: {
            msg: "Количество указано неправильно",
            regexp: /[1-9]/
        }
    }
}

function responseProcess(response){
    if (response.data.status == "err") {
        alert("Error");
        console.log(response.data.msg);
    }
    else alert(response.data.msg)
}

function catchProcess(response) {
    alert("Error");
    console.log(response);
}

var app = new Vue({
    el: '#app',
    delimiters: ['[[',']]'],
    data: {
        ru: ru,
        urls: {
            add_user: "/admin/add_user",
            edit_user: "/admin/edit_user",
            holiday: "/admin/add_holiday",
            edit_hours: "/admin/edit_hours"
        },
        holiday: {
            uid: "",
            raw_from: null,
            raw_till: null,
            from: null,
            till: null,
            disabled: true,
            disabledDates: { to: null }
        },
        add_user: {
            auth_id: null,
            name: null,
            phone: null
        },
        edit_user: {
            id: "",
            auth_id: null,
            name: null,
            phone: null
        },
        edit_hours: {
            id: "",
            action: "+",
            count: null
        },
        users: []
    },
    methods: {
        submit: function(part) {
            var data = this.$data[part];
            var url = this.urls[part];
            if (!this.validor(part)) return false;
            axios.post(url, data)
                .then(responseProcess)
                .catch(catchProcess)
        },
        validor: function(key) {
            var rules = validation_rules[key];
            var vm = this;
            for (var rule in rules) {
                var value = vm.$data[key][rule];
                var regexp = rules[rule].regexp;
                var msg = rules[rule].msg;
                if ( regexp && !regexp.test(value) ){
                    alert(msg);
                    console.log("regexp")
                    return false; 
                }
                if ( !value || value == 0 || value == "") {
                    console.log("if")
                    alert(msg);
                    return false;
                }
            };
            return true;
        },
        loadUser: function(){
            var vm = this;
            if (vm.edit_user.id == 0) return false;
            axios.get("/admin/get_user/" + vm.edit_user.id)
                .then(function(response){
                    vm.edit_user = response.data;
                })
                .catch(catchProcess)
        },
        disableUser: function(id) {
            var url = `/admin/disable_user/${id}`;
            axios.get(url)
                .then(responseProcess)
                .catch(catchProcess)
        },
        pickerSelected: function(date) {
            this.holiday.disabled = false;
            this.holiday.disabledDates.to = date;
        },
        pickerCleared: function() {
            this.holiday.disabled = true;
        }
    },
    watch: {
        "holiday.raw_from": function(new_val){
            this.holiday.from = new_val.toISOString().split("T")[0];
        },
        "holiday.raw_till": function(new_val){
            this.holiday.till = new_val.toISOString().split("T")[0];
        }
    },
    mounted: function(){
        var vm = this;
        axios.get("/get_users")
                .then(function(response){
                    vm.users = response.data;
                })
                .catch(catchProcess)
    },
    components: {
        Datepicker
    }
});