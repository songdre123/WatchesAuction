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
        <router-link class="router-link" to="/admin">
          <v-list-item
          prepend-icon="mdi-cash"
          title="Home"
          value="home">
          </v-list-item>
        </router-link>

          <v-list-item
            prepend-icon="mdi-gavel"
            title="My Created Auctions"
            value="auction"
          ></v-list-item>

          <router-link class="router-link" to="/admin/create">
            <v-list-item
              prepend-icon="mdi-watch"
              title="List Watch"
              value="list"
            ></v-list-item>
          </router-link>

          <router-link class="router-link" to="/admin/account">
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
  </v-app-bar>
  </div>
</template>

<script>
import { useUserStore } from '@/store/userStore'
const userStore = useUserStore()

export default {
	data() {
		return {
      drawer: null,
		}
	},
  computed: {
    getUserName() {
      return userStore.getUserName
    }
  },
  methods: {
    removeUserStore() {
      userStore.removeUser()
      userStore.logout()
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

.router-link {
  text-decoration: none;
  color: black;
}

</style>