<template>
 <!--make a site for people to book a day to collect their watch  -->
    <v-container>
        <v-row>
        <v-col>
            <v-sheet>
            <h3 class="mb-3">Schedule a Day to Collect Your Watch</h3>
            <v-divider class="mb-3"></v-divider>
            <v-row>
                <v-col>
                <v-text-field
                    label="Date"
                    type="date"
                    v-model="date"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    label="Time"
                    type="time"
                    v-model="time"
                ></v-text-field>
                </v-col>
            </v-row>
            <v-btn
                @click="schedule"
            >Schedule</v-btn>
            </v-sheet>
        </v-col>
        </v-row>
    </v-container>
</template>
<script>
export default {
    data() {
        return {
            date: '',
            time: ''
        }
    },
    methods: {
        schedule() {
            console.log('Scheduled')
        }
    }
}

</script>