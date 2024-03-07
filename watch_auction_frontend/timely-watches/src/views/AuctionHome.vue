<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-container>
    <v-tabs v-model="tab" align-tabs="center" color="amber-lighten-2">
      <v-tab v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</v-tab>
    </v-tabs>
      <v-row align="center" justify="center">
        <v-col v-for="(watch, index) in watches[tab]" :key="index" cols="4">
          <WatchCard
            v-if="watch"
            :title="watch['title']"
            :referenceNo="watch['Ref']"
            :date="watch['Date']"
            :minBid="watch['MinBid']"
          />
        </v-col>
      </v-row>
    </v-container>
</template>

<script setup>
  import WatchCard from '@/components/WatchCard.vue'
</script>

<script>
  export default {
    data() {
      return {
        categories: ['Rolex', 'Patek Phillipe', 'Audemars Piguet'],
        tab: null,
        watches: {
      'Rolex': [
        {
          'title': 'Rolex Submariner',
          'Ref': '126610LN',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 8000,
        },
        {
          'title': 'Rolex Datejust',
          'Ref': '126234',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 10000,
        },
        // Add more Rolex watches here
        {
          'title': 'Rolex Daytona',
          'Ref': '116500LN',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 12000,
        },
        {
          'title': 'Rolex GMT-Master II',
          'Ref': '126710BLRO',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 15000,
        },
        {
          'title': 'Rolex Day-Date',
          'Ref': '128238',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 20000,
        },
        {
          'title': 'Rolex Explorer',
          'Ref': '214270',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 18000,
        }
      ],
      'Patek Phillipe': [
        {
          'title': 'Patek Philippe Nautilus',
          'Ref': '5711/1A-010',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 20000,
        },
        // Add more Patek Philippe watches here
        {
          'title': 'Patek Philippe Calatrava',
          'Ref': '5296R-010',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 25000,
        },
        {
          'title': 'Patek Philippe Aquanaut',
          'Ref': '5167A-001',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 22000,
        },
        {
          'title': 'Patek Philippe Grand Complications',
          'Ref': '5327J-001',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 30000,
        },
        {
          'title': 'Patek Philippe Gondolo',
          'Ref': '5124J-001',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 28000,
        },
        {
          'title': 'Patek Philippe Twenty~4',
          'Ref': '4910/10A-012',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 18000,
        }
      ],
      'Audemars Piguet': [
        {
          'title': 'Audemars Piguet Royal Oak',
          'Ref': '15500ST.OO.1220ST.01',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 15000,
        },
        // Add more Audemars Piguet watches here
        {
          'title': 'Audemars Piguet Royal Oak Offshore',
          'Ref': '26400SO.OO.A002CA.01',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 18000,
        },
        {
          'title': 'Audemars Piguet Royal Oak Concept',
          'Ref': '26589IO.OO.D030CA.01',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 22000,
        },
        {
          'title': 'Audemars Piguet Royal Oak Chronograph',
          'Ref': '26331ST.OO.1220ST.01',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 20000,
        },
        {
          'title': 'Audemars Piguet Royal Oak Tourbillon',
          'Ref': '26388PO.OO.D027CA.01',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 30000,
        },
        {
          'title': 'Audemars Piguet Royal Oak Selfwinding',
          'Ref': '15450ST.OO.1256ST.01',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 25000,
        }
      ]
    }
      }
    },
    methods: {
      handleTabChange(tab) {
      this.tab = tab;
      setTimeout(() => {
        window.dispatchEvent(new Event('resize')); // Trigger resize event to update Vuetify layout
      }, 300);
    }
    },
    computed: {
    watchLength() {
      return this.watches[this.tab] ? this.watches[this.tab].length : 0
    },
  },
   mounted() {
      this.tab = this.categories[0]; // Initialize tab to the first category
    },
}
</script>

