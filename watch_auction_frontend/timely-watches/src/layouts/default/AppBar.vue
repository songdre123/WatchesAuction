<!-- eslint-disable no-mixed-spaces-and-tabs -->
<!-- eslint-disable no-multiple-template-root -->
<template>
  <div>
    <v-navigation-drawer v-model="drawer" temporary color="amber-lighten-4">
      <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
          :title="getUserName()"
        ></v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <router-link class="router-link" to="/home">
          <v-list-item
          prepend-icon="mdi-home"
          title="All Auctions"
          value="home">
          </v-list-item>
        </router-link>

        <router-link class="router-link" to="/home/bids">
          <v-list-item
            prepend-icon="mdi-cash-multiple"
            title="My Bids"
            value="bids"
          ></v-list-item>
        </router-link>

          <router-link class="router-link" to="/home/account">
            <v-list-item
              prepend-icon="mdi-account"
              title="Account"
              value="account"
            ></v-list-item>
          </router-link>

          <router-link class="router-link" to="/">
          <v-list-item
            prepend-icon="mdi-door"
            title="Logout"
            value="logout"
            @click="removeUserStore"
          ></v-list-item>
          </router-link>
        </v-list>

    </v-navigation-drawer>
  <v-app-bar :elevation="2" :height="100" color="amber-lighten-5">
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
import { useUserStore } from '@/store/userStore'
import axios from 'axios'

const userStore = useUserStore()

export default {
	data() {
		return {
      drawer: null,
      notifications: [
        
      ],
		}
	},
  computed: {
    getUserName() {
      return userStore.getUserName
    }
  },
  methods: {
    removeUserStore() {
      userStore.removeUser
    }
  },
  async mounted() {
    try {
      const userID = userStore.getUserId()
      const notificationResponse = await axios.get(`http://127.0.0.1:5004/notification/${userID}`)
      const notificationData = notificationResponse.data.data.notifications
      this.notifications = notificationData
      console.log(notificationResponse)
    }
    catch (error) {
      console.error('Error getting user:', error.message);
      console.log(error.status)
      console.log(error)
      throw error; // Re-throw the error to propagate it further
    }
  }
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

.router-link {
  text-decoration: none;
  color: black;
}

</style>