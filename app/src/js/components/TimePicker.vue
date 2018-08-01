<template>
    <div class="time_picker">
        <div class="clock" v-show="show" @click="toggle">
            <div class="hour clock_item_wrapper">
                <div class="clock_item" v-wheel="scroll" type="hours" delta="1">
                    {{ parsedHour }}
                </div>
            </div>
            <div class="clock_item_middle">
                <div class="clock_item">
                    :
                </div>
            </div>
            <div class="minute clock_item_wrapper">
                <div class="clock_item" v-wheel="scroll" type="minutes" delta="5">
                    {{ parsedMinute }}
                </div>
            </div>
        </div>
        <input type="text" class="time_picker_head" @click="toggle" @blur="toggle" :value="parsedVal" />
    </div>
</template>
<script>
    import moment from 'moment'

    export default {
        props: ["init-val"],
        data: function() {
            return {
                show: false,
                currentVal: this.initVal,
            }
        },
        computed: {
            parsedVal: function(){
                if (this.currentVal) return this.currentVal.format("HH:mm");
            },
            parsedHour: function(){
                if (this.currentVal) return this.currentVal.format("HH");
            },
            parsedMinute: function(){
                if (this.currentVal) return this.currentVal.format("mm");
            }
        },
        watch: {
            initVal: function(v) {
                this.currentVal = v;
            },
            currentVal: function(v) {
                this.$emit("input", v);
            }
        },
        methods: {
            change: function(event) {
                var v = event.target.value;
                this.currentVal = v;
                this.$emit("input", v);
            },
            scroll: function(event){
                var direction = event.deltaY;
                var type = event.target.getAttribute('type');
                var delta = event.target.getAttribute('delta');
                if (direction < 0) this.currentVal = moment(this.currentVal).add(delta, type);
                else this.currentVal = moment(this.currentVal).subtract(delta, type);
            },
            toggle: function(){
                this.show = !this.show;
            }
        },
        directives: {
            wheel: {
                bind: function(el, binding){
                    var action = binding.value;
                    if (el.addEventListener) {
                        if ('onwheel' in document) {
                        // IE9+, FF17+, Ch31+
                            el.addEventListener("wheel", action);
                        } else if ('onmousewheel' in document) {
                        // устаревший вариант события
                            el.addEventListener("mousewheel", action);
                        } else {
                        // Firefox < 17
                            el.addEventListener("MozMousePixelScroll", action);
                        }
                    } else { // IE8-
                        el.attachEvent("onmousewheel", action);
                    }

                },
                unbind: function(el, binding) {
                    el.removeEventListener('wheelevent', binding.value);
                }
            }
        }
    }
</script>
<style>
    input[type="text"] {
        border: none;
        margin: 0px;
        padding: 0px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }
    input.time_picker_head:focus:not([readonly]) {
        border-bottom: none;
        box-shadow: none;
    }
    .time_picker {
        display: inline-block;
    }
    .clock {
        width:100%;
        position: absolute;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
        border-radius: 10px;
        top: 0;
        background: white;
        overflow: hidden;
    }
    .clock_item_wrapper {
        float: left;
        width: 48%;
        height: 100%;
    }
    .clock_item_middle {
        float: left;
        width: 4%;
        height: 100%;
    }
    .clock_item {
        padding: 10px;
        font-size: 36px;
        font-weight: bold;
    }
    .clock_item_middle .clock_item {
        padding: 8px 0px;
    }
</style>