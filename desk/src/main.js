import * as lodash from "lodash";
import { createApp } from "vue";
import { createPinia } from "pinia";
import {
  dontmanageRequest,
  resourcesPlugin,
  setConfig,
  Badge,
  Button,
  Dialog,
  ErrorMessage,
  FeatherIcon,
  FormControl,
  Input,
  Tooltip,
} from "dontmanage-ui";
import App from "./App.vue";
import "./index.css";
import { router } from "./router";
import { socket } from "./socket";
import { createToast } from "@/utils";

const globalComponents = {
  Badge,
  Button,
  Dialog,
  ErrorMessage,
  FeatherIcon,
  FormControl,
  Input,
  Tooltip,
};

setConfig("resourceFetcher", dontmanageRequest);

const pinia = createPinia();
const app = createApp(App);

app.use(resourcesPlugin);
app.use(pinia);
app.use(router);

for (const c in globalComponents) {
  app.component(c, globalComponents[c]);
}

app.config.unwrapInjectedRef = true;
app.config.globalProperties.$_ = lodash;
app.config.globalProperties.$socket = socket;
app.config.globalProperties.$toast = createToast;

app.mount("#app");
