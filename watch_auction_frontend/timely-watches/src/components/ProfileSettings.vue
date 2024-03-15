<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="6" align="center" justify="center">
        <h2 class="text">Account Settings</h2>
        <v-form>
          <v-row class="mt-4">
            <v-col cols="6">
              <v-text-field label="First Name" v-model="firstName" required></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field label="Last Name" v-model="lastName" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Password" v-model="password" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn @click="makeChanges" color="amber">Save</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useUserStore } from '@/store/userStore'
import axios from 'axios'
const userStore = useUserStore()

export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      password: '',
    }
  },
  methods: {
    async makeChanges() {
      userStore.editFirstName(this.firstName)
      userStore.editLastName(this.lastName)
      userStore.editPassword(this.password)

      const params = {
        password : this.password,
        first_name: this.firstName,
        last_name: this.lastName,
      }
      try {
        await axios.put(`http://127.0.0.1:5000//user/${this.email}`, params);
      } catch (error) {
        console.error('Error creating user:', error);
        throw error; // Re-throw the error to propagate it further
      }
      
    }
  }
}
</script>

<style scoped>
/* Component-specific styles here */
</style>