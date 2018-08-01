<template>
    <div>
        <div class="cell"
            @click="setDuty"
            @contextmenu.prevent="context"
            :class="{pointer: !past, holiday: holiday}">
            {{ value }}
        </div>
        
    </div>
</template>
<script>
    export default {
        props: ["day", "uid", "past"],
        data: function() {
            return {
            }
        },
        methods: {
            setDuty: function(){
                if (this.value == "1" || this.past) return;
                this.$emit("updateduty", this.uid);
            },
            context: function(event){
                if (this.holiday) this.$root.$refs.menu.open(event, { uid: this.uid, day: this.day});
            }
        },
        computed: {
            value: function(){
                return this.uid == this.day.uid ? '1': '';
            },
            holiday: function(){
                return this.uid == this.day.holiday ? true: false;
            }
        }
    }
</script>