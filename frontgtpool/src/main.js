import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import socketio from 'socket.io-client';
import VueSocketIO from 'vue-socket.io';

Vue.config.productionTip = false
Vue.use(new VueSocketIO({
  debug: true,
  connection: 'ws://localhost:5000/socket.io/?EIO=3&transport=websocket',
  vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
  },
}))

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
