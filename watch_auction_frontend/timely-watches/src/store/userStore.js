// Utilities
import { defineStore } from "pinia";



export const useUserStore = defineStore("user", {
  state: () => ({
    user: "",
    userID: "",
  }),
  actions: {
    async setUser(user) {
      this.user = user;
      return new Promise((resolve) => {
        // Simulate asynchronous operation to set user data
        setTimeout(() => {
          resolve(); // Resolve the promise once user data is set
        }, 100); // Adjust the delay as needed
      });
    },
    setUserId(id) {
      this.userID = id;
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve();
        }, 100);
      });
    },
    getUser() {
      return this.user;
    },
    getUserId() {
      return this.userID;
    },
    getUserName() {
      return this.user.first_name + " " + this.user.last_name;
    },
    getUserEmail() {
      return this.user.email;
    },
    removeUser() {
      this.user = "";
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
      this.user.password = password;
    },
  },
  persist: {
    enabled: true,
  },
});
