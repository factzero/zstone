import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './styles/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import './styles/dark/dark.scss'


const app = createApp(App)
app.use(router)
app.mount('#app')
