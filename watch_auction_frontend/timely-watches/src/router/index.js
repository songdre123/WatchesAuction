// Composables
import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/store/userStore";

const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("@/views/Login.vue"),
  },
  {
    path: "/schedule/:id",
    name: "Schedule",
    component: () => import("@/views/Schedule.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    component: () => import("@/layouts/admin/AdminDefault.vue"),
    children: [
      {
        path: "create",
        name: "Create",
        component: () => import("@/views/seller/CreateListing.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "account",
        name: "AdminAccount",
        component: () => import("@/views/Account.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "listing",
        name: "Listing",
        component: () => import("@/views/seller/Listing.vue"),
        meta: { requiresAuth: true },
      },
    ],
    meta: { requiresAuth: true },
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
        meta: { requiresAuth: true },
      },
      {
        path: "bids",
        name: "Bids",
        component: () => import("@/views/BidsView.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: ":id",
        name: "AuctionDetails",
        component: () => import("@/views/AuctionDetails.vue"),
        meta: {
          auth: true,
          requiresAuth: true,
        },
      },
      {
        path: "account", // Removed the leading slash
        name: "Account",
        component: () => import("@/views/Account.vue"),
        meta: { requiresAuth: true },
      },
    ],
    meta: { requiresAuth: true },
  },
  {
    path: "/checkout/:id",
    name: "Checkout",
    component: () => import("@/views/Checkout.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/Success",
    name: "Success",
    component: () => import("@/views/Success.vue"), // Fixed the casing of the file name
    meta: { requiresAuth: true },
  },
  {
    path: "/Cancel",
    name: "Cancel",
    component: () => import("@/views/Cancel.vue"),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// eslint-disable-next-line no-unused-vars
router.beforeEach((to, from) => {
  const userStore = useUserStore();
  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !userStore.$state.isLoggedIn
  ) {
    return {
      path: "/",
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    };
  } 
});

export default router;
