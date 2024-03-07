<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="6" align="center" justify="center">
        <h2 class="text">Account Settings</h2>
        <v-form>
          <v-row class="mt-4">
            <v-col cols="6">
              <v-text-field label="First Name" required></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field label="Last Name" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Email" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Password" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn color="amber">Save</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  // Component logic here
}
</script>

<style scoped>
/* Component-specific styles here */
</style>