import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Form from "../components/Form.vue";
import Schedule from "../components/Schedule.vue";
import Assignment1 from "../components/Assignment.vue";
import Note from "../components/Note.vue";
import Visualization from "../components/Visualization.vue";

export const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/form",
    name: "form",
    component: Form,
    props: {
      poll_id: 2,
    },
  },
  {
    path: "/about",
    name: "about",
    components: { about: () => import("../views/AboutView.vue") },
  },
  {
    path: "/helloworld",
    name: "helloworld",
    component: Assignment1,
  },
  {
    path: "/note",
    name: "note",
    component: Note,
  },
  {
    path: "/visualization",
    name: "visualization",
    component: Visualization,
  },
  // {
  //     path: '/schedule',
  //     name: 'schedule',
  //     component: Schedule
  // },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
