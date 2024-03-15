// Utilities
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: '',
  }),
  actions: {
    setUser(user) {
      this.user = user;
    },
    getUser() {
      return this.user;
    },
    getUserName() {
      return this.user["first_name"] + " " + this.user["last_name"];
    },
    removeUser() {
      this.user = null;
    },
    editImage(photo_link) {
      this.user.profile_picture = photo_link;
    },
    editFirstName(firstName) {
      this.user.first_name = firstName;
    },
    editLastName(lastName) {
      this.user.last_name = lastName;
    },
    editPassword(password) {
        this.user.password = password
    }
  },
});