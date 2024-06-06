import {createApp, onMounted} from 'vue'
import App from './App.vue'
import router from './router'
import "./assets/tailwind.css";
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.use(router)

app.mount('#app')
