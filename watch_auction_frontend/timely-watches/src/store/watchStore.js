// Utilities
import { defineStore } from "pinia";

export const useWatchStore = defineStore("watch", {
  state: () => ({
    watch: null,
  }),
  actions: {
    setWatch(watch) {
      this.watch = watch
    },
    getWatch() {
      return this.watch
    },
    updateWatchPrice() {
      this.watch.CurrentPrice += 500;
    }
  },
});
