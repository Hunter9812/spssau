import axios from "axios";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/reset.css";
import router from "./router";

const app = createApp(App);

app.use(router).use(ElementPlus);

app.mount("#app");
