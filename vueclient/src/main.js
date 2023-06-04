import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'

// // NEW
// if (process.env.NODE_ENV === 'development') {
//     const { worker } = require('./mocks/browser')
//     worker.start()
// }

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
