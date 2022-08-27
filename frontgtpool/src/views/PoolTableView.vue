<template>
  <v-app id="inspire">

    <!-- Menu -->

    <v-app-bar app color="white" flat>
      <v-container class="py-0 fill-height">
        <v-avatar class="mr-10" color="grey darken-1" size="32"></v-avatar>

        <v-btn v-for="link in links" :key="link" text>
          {{ link }}
        </v-btn>

        <v-spacer></v-spacer>

        <v-responsive max-width="260">
          <v-text-field
            dense
            flat
            hide-details
            rounded
            solo-inverted
          ></v-text-field>
        </v-responsive>
      </v-container>
    </v-app-bar>

    <!-- Dialogs templates -->
    emp: {{emp}}
    id: {{id}}
    <v-dialog
      v-model="dialogNewOrder"
      persistent
      width="500"
    >
      <v-card>
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="dialogNewOrder = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Hacer nuevo pedido</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn
              dark
              text
              @click="dialogNewOrder = false"
            >
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <NewOrder v-if="dialogNewOrder"></NewOrder>

      </v-card>
    </v-dialog>

    <!-- Main -->
    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col class="colLeft" cols="2">
            <div class="my-2" rounded="lg">
              <v-btn color="" class="botonHacerNuevoPedido" outlined large @click="dialogNewOrder = true">
                Hacer nuevo pedido
              </v-btn>
            </div>
            <v-sheet rounded="lg">
              <v-list color="transparent">
                <v-list-item v-for="(value, key) in datosMesaIzq" :key="key">
                  <v-list-item-content>
                    <v-list-item-title>
                      <ul>
                        <li v-if="value.tituloVisible">
                          <b>{{ value.titulo }}:</b>
                        </li>
                        <li>{{ value.value }}</li>
                      </ul>
                      <v-divider class="my-2" v-if="value.divisor"></v-divider>
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-sheet>
          </v-col>

          <v-col class="colRight">
            <v-sheet min-height="70vh" rounded="lg">
              <v-item-group>
                <v-container>
                  <h1 class="text-center">PUNTAJES</h1>
                  <v-row>

                    <v-col v-for="n in 8" :key="n" cols="12" md="4">
                      <Cards :tableNumber="n"></Cards>
                    </v-col>
                  </v-row>
                </v-container>
              </v-item-group>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <button @click="clickButton()">Enviar puntaje</button>
  </v-app>
</template>

<script>
import NewOrder from "../components/static/NewOrder.vue"
import Cards from "../components/static/cards.vue";
import axios from 'axios'
export default {
  components: {
    Cards,
    NewOrder
  },
  data: () => ({
    isConnected: false,
    socketMessage: '',
    emp: "",
    id: "",
    links: ["Dashboard", "Messages", "Profile", "Updates"],
    dialogNewOrder: false,
    socket: null,
    datosMesaIzq: [
      {
        titulo: "Mesa",
        value: "01",
        tituloVisible: true,
        divisor: false,
      },
      {
        titulo: "HoraAct",
        value: "",
        tituloVisible: false,
        divisor: true,
      },
      {
        titulo: "Inicio",
        value: "06/03/2022 11:42:06 AM",
        tituloVisible: true,
        divisor: false,
      },
      {
        titulo: "Vr. tiempo",
        value: "$266.66",
        tituloVisible: true,
        divisor: false,
      },
      {
        titulo: "Vr. consumo",
        value: "$5,000.00",
        tituloVisible: true,
        divisor: false,
      },
      {
        titulo: "Vr. total",
        value: "$5,266.66",
        tituloVisible: true,
        divisor: false,
      },
    ],
  }),

  created() {
    this.emp = this.$route.query.emp
    this.id = this.$route.query.id

    axios.get('http://127.0.0.1:5000/appPool/get/mesas_activas/'+this.emp+'/'+this.id,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(result => {
        let resultQuery = result.data.result[0]
        console.log(resultQuery)
        this.datosMesaIzq[0].value = resultQuery.mesa
        this.datosMesaIzq[2].value = resultQuery.fecha_hora
        this.datosMesaIzq[3].value = resultQuery.vr_minuto
      }).catch(error => {

        console.log(error)
      })
  },

sockets: {
        connect: function () {
            console.log('socket connected')
        },
        customEmit: function (data) {
            console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
        }
    },

  methods:{
        date_function: function () {
            this.datosMesaIzq[1].value = new Date().toLocaleString();
        },
        getPuntaje: function(message) {
          console.log(this.connection);
          this.connection.send(message);
        },
          // Send the "pingServer" event to the server.
         clickButton: function (data) {
            // $socket is socket.io-client instance
            let msgEMIT = this.$socket.emit('my_event', data)
            console.log(msgEMIT)
            console.log(data)
        }

    },
    mounted () {
      setInterval(this.date_function,1000)
    },

    created: function() {
    console.log("Starting connection to WebSocket Server")
    // this.socket = io.connect();

    // socket.on('connect', function() {
    //       console.log('Connect')
    //   });
    // socket.on('getEvent', function(msg){
    //   console.log(msg)
    // })

  }
};
</script>

<style>
ul li {
  list-style: none;
}

.botonHacerNuevoPedido {
  width: 100%;
}

.colLeft {
  min-width: auto;
}

@media only screen and (max-width: 1900px) {
  .colLeft {
    min-width: 25%;
  }
}

@media only screen and (max-width: 1250px) {
  .colLeft {
    min-width: 100%;
  }
  .colRight {
    min-width: 100%;
  }
}
</style>
