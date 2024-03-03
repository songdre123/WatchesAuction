<!-- eslint-disable no-mixed-spaces-and-tabs -->
<!-- eslint-disable no-multiple-template-root -->
<template>
  <div>
    <v-navigation-drawer v-model="drawer" temporary color="black">
      <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
          title="John Leider"
        ></v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
          <v-list-item
            prepend-icon="mdi-account"
            title="Account"
            value="account"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-gavel"
            title="Auction"
            value="auction"
          ></v-list-item>
          <v-list-item
            prepend-icon="mdi-cash-multiple"
            title="Bids"
            value="bids"
          ></v-list-item>

          <router-link to="/">
          <v-list-item
            prepend-icon="mdi-door"
            title="Logout"
            value="logout"
          ></v-list-item>
          </router-link>
        </v-list>

    </v-navigation-drawer>
  <v-app-bar :elevation="2" :height="100">
    <v-btn @click.stop="drawer = !drawer" density="compact" icon="mdi-menu"></v-btn>
    <v-app-bar-title class="topbar">
      <h4 class="header">
        <svg-icon type="mdi" :path="path1"></svg-icon>
        Timely Watches
      </h4>
    </v-app-bar-title>
    <v-badge v-if="notifications.length > 0" :content="notifications.length">
      <v-menu :location="start">
        <template v-slot:activator="{props}">
          <v-btn density="compact" v-bind=props icon="mdi-bell-outline"></v-btn>
        </template>

        <V-list>
          <v-list-item v-for="(alert, idx) in notifications" :key="idx">
            <v-list-item-subtitle>
              {{ alert }}
            </v-list-item-subtitle>
          </v-list-item>
        </V-list>

      </v-menu>
    </v-badge>

    <v-btn v-else density="compact" icon="mdi-bell-outline"></v-btn>

  </v-app-bar>
  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiWatch } from '@mdi/js';
import { VList } from 'vuetify/lib/components/index.mjs';

export default {
	name: "my-cool-component",
	components: {
    SvgIcon,
    VList
},
	data() {
		return {
  path1: mdiWatch,
  drawer: null,
  notifications: [
    'Your bid at Auction Ref: 1593478229v has beeen replaced',
    'Your won Auction Ref: 10383902829v',
  ]
		}
	},
}
</script>


<style scoped>
.topbar {
  display: flex;
  justify-content: center;
  align-items:center;
}

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Black.otf);
}

.header {
  font-family: Riviera Nights, sans-serif;
}

</style>