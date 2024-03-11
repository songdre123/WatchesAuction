// Composables
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/home",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "", // Empty path for the Home route
        name: "Home",
        component: () =>
          import(/* webpackChunkName: "home" */ "@/views/AuctionHome.vue"),
      },
      {
        path: ":id",
        name: "AuctionDetails",
        component: () => import("@/views/AuctionDetails.vue"),
        meta: {
          auth: true,
        },
      },
      {
        path: "account", // Removed the leading slash
        name: "Account",
        component: () => import("@/views/Account.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
