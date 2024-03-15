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
    }
  },
});
