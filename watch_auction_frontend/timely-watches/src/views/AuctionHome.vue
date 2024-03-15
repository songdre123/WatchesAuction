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
            :referenceNo="index"
            :watch="watch"
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
      'Rolex': {
        "126610LN" :
        {
          'title': 'Rolex Submariner',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 8000,
          'imageURL': "https://cdn.watchbase.com/watch/lg/origin:png/rolex/datejust-31/278341rbr-0023-f.webp",
        },
        '126234':
        {
          'title': 'Rolex Datejust',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 10000,
          'imageURL': "https://cdn.watchbase.com/watch/lg/origin:jpg/rolex/datejust/116333-0004-a3.webp",
        },
        '116500LN':
        {
          'title': 'Rolex Daytona',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 12000,
          'imageURL' : 'https://cdn.watchbase.com/watch/lg/origin:jpg/rolex/daytona/116576tbr-7b.webp'
        },
        '126710BLRO':
        {
          'title': 'Rolex GMT-Master II',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 15000,
          'imageURL' : 'https://cdn.watchbase.com/watch/lg/origin:png/rolex/gmt-master/116718ln-0001-fc.webp'
        },
        '128238':
        {
          'title': 'Rolex Day-Date',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 20000,
          'imageURL' : 'https://cdn.watchbase.com/watch/lg/origin:jpg/rolex/day-date/6611-8d.webp'
        },
        '214270':
        {
          'title': 'Rolex Explorer',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 18000,
          'imageURL' : 'https://cdn.watchbase.com/watch/lg/origin:jpg/rolex/explorer-2/16570-43.webp'
        }
      },
      'Patek Phillipe': {
        '5711/1A-010':
        {
          'title': 'Patek Philippe Nautilus',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 20000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/nautilus/5980-1r-001-6d.webp'
        },
        // Add more Patek Philippe watches here
        '5296R-010':
        {
          'title': 'Patek Philippe Calatrava',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 25000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/calatrava/6000r-001-1d.webp'
        },
        '5167A-001':
        {
          'title': 'Patek Philippe Aquanaut',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 22000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/aquanaut/tropic-style-rubber-strap-f8.webp'
        },
        '5327J-001':
        {
          'title': 'Patek Philippe Grand Complications',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 30000, 
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/grand-complications/5140r-001-ba.webp'
        },
        '5124J-001':
        {
          'title': 'Patek Philippe Gondolo',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 28000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/175th-commemorative-watches/5200g-010-19.webp'
        },
        '4910/10A-012':
        {
          'title': 'Patek Philippe Twenty~4',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 18000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/patek-philippe/twenty-4/4908-11r-010-1c.webp'
        }
      },
      'Audemars Piguet': {
        '15500ST.OO.1220ST.01':
        {
          'title': 'Audemars Piguet Royal Oak',
          'Date': '2022-03-24 16:00 GMT',
          'MinBid': 15000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/audemars-piguet/royal-oak/15400or-oo-d002cr-01-8e.webp'
        },
        // Add more Audemars Piguet watches here
        '26400SO.OO.A002CA.01':
        {
          'title': 'Audemars Piguet Royal Oak Offshore',
          'Date': '2022-03-25 17:00 GMT',
          'MinBid': 18000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:jpg/audemars-piguet/royal-oak-offshore/26473bc-zz-8043bc-01-ca.webp'
        },
        '26589IO.OO.D030CA.01':
        {
          'title': 'Audemars Piguet Royal Oak Concept',
          'Date': '2022-03-26 18:00 GMT',
          'MinBid': 22000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:jpg/audemars-piguet/concept/26265-fo-oo-d002-ca-94-e3.webp'
        },
        '26331ST.OO.1220ST.01':
        {
          'title': 'Audemars Piguet Royal Oak Chronograph',
          'Date': '2022-03-27 19:00 GMT',
          'MinBid': 20000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/audemars-piguet/royal-oak-offshore/26402cb-oo-a010ca-01-ea.webp'
        },
        '26388PO.OO.D027CA.01':
        {
          'title': 'Audemars Piguet Royal Oak Tourbillon',
          'Date': '2022-03-28 20:00 GMT',
          'MinBid': 30000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/audemars-piguet/royal-oak-offshore/26170or-oo-1000or-01-35.webp'
        },
        '15450ST.OO.1256ST.01':
        {
          'title': 'Audemars Piguet Royal Oak Selfwinding',
          'Date': '2022-03-29 21:00 GMT',
          'MinBid': 25000,
          'imageURL': 'https://cdn.watchbase.com/watch/lg/origin:png/audemars-piguet/royal-oak-offshore/26703st-oo-a027ca-01-ef.webp'
        }
      }
    }
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

