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
          <v-list-item
            prepend-icon="mdi-door"
            title="Logout"
            value="logout"
          ></v-list-item>
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
    <v-badge v-if="notificationCount > 0" :content="notificationCount">
      <v-btn density="compact" icon="mdi-bell-outline"></v-btn>
    </v-badge>

    <v-btn v-else density="compact" icon="mdi-bell-outline"></v-btn>

  </v-app-bar>
  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiWatch } from '@mdi/js';

export default {
	name: "my-cool-component",
	components: {
		SvgIcon
	},
	data() {
		return {
  path1: mdiWatch,
  drawer: null,
  notificationCount: 2,
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