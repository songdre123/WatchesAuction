<template>

    <div class="wrapper">
        <ejs-calendar :selectedDate="date" :change="change" :showTodayButton="false">
        </ejs-calendar>
        <button @click="submitschedule" class="btn btn-primary" >Submit</button>
    </div>
    <div v-if="submitted">
        <h1>Success</h1>
        <p>Your collection date has been placed successfully.</p>
    </div>



</template>
<script>
import { CalendarComponent } from '@syncfusion/ej2-vue-calendars';
export default{
    name: 'Schedule',
    data(){
        return{
            date: new Date()
            submitted: false

        }
    },
    components: {
        'ejs-calendar': CalendarComponent
    },
}
</script>
<style>
@import "@syncfusion/ej2-base/styles/material.css";
@import "@syncfusion/ej2-buttons/styles/material.css";
@import "@syncfusion/ej2-calendars/styles/material.css";
@import "bootstrap/dist/css/bootstrap.css"; /* Add this line */
.wrapper{
    max-width: 200px;
    margin: 0 auto;
}
</style>