<template>
  <v-card max-width="1000" class="mx-auto">
    <v-container>
      <div class="text-h4 text-center ma-5">Carrito de compras</div>
      <v-row no-gutters>
        <v-col
          cols="12"
          sm="12"
          md="8"
          v-if="!loadingCarrito && !noHayProductos"
        >
          <v-card v-for="(item, i) in infoProductos" :key="i" elevation="0">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title
                  class="text-h6"
                  v-text="item.title"
                ></v-card-title>

                <v-card-subtitle>
                  <span class="text-h7"
                    >Precio por unidad: $ {{ item.price }}</span
                  >
                  <br />
                  <span class="text-h6 font-weight-light"
                    >Precio total: $ {{ item.price * item.size }}</span
                  >
                </v-card-subtitle>
                <v-card-actions>
                  <v-btn @click="reducirCant(item.id)">
                    <v-icon>mdi-arrow-left</v-icon>
                  </v-btn>

                  <v-text-field
                    label="Cantidad"
                    class="inputCantidad"
                    :value="item.size"
                    type="number"
                    outlined
                    dense
                    disabled
                  ></v-text-field>
                  <v-btn @click="aumentarCant(item.id)">
                    <v-icon>mdi-arrow-right</v-icon>
                  </v-btn>

                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        color="primary"
                        dark
                        v-bind="attrs"
                        v-on="on"
                        class="ml-3"
                        outlined
                        @click="eliminarCarrito(item.id)"
                      >
                        <v-icon>mdi-close-circle</v-icon>
                      </v-btn>
                    </template>
                    <span>Eliminar producto del carrito</span>
                  </v-tooltip>
                </v-card-actions>
              </div>

              <v-avatar class="ma-3" size="125" tile>
                <v-img :src="item.images[0]"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>

        <v-col
          class="d-flex justify-center"
          cols="12"
          sm="12"
          md="12"
          v-if="noHayProductos"
        >
          <v-sheet class="text-center" max-width="720px" width="100%">
            <div>{{ this.textoCarrito }}</div>
            <br />
            <v-img
              class="mx-auto rounded align-center"
              src="@/assets/sadcart.jpeg"
              max-width="300"
            ></v-img>
            <a
              href="https://www.freepik.com/free-photo/lonely-sad-tired-woman-rests-shopping-trolley-fatigue-noise-loud-music-needs-rest-has-gloomy-facial-expression-wears-dress-sneakers-carries-bunch-air-balloons-disappointed_11579423.htm#query=sad%20cart&position=0&from_view=search&track=sph"
              >Image by wayhomestudio</a
            >
            on Freepik
          </v-sheet>
        </v-col>

        <v-col cols="12" sm="12" md="12" v-if="loadingCarrito">
          <br />
          <Loading></Loading>
        </v-col>

        <v-col
          cols="12"
          md="4"
          sm="12"
          v-if="!loadingCarrito && !noHayProductos"
        >
          <v-card elevation="1" class="pa-6">
            <div class="text-h5 text-center">Resumen de pedido</div>
            <br />

            <v-row no-gutters>
              <v-col cols="6">
                <b>Nombre prod.</b>
              </v-col>
              <v-col cols="2"><b>Ud</b></v-col>
              <v-col cols="4"><b>Total</b></v-col>
            </v-row>

            <v-divider></v-divider>
            <br />

            <div v-for="(item, i) in infoProductos" :key="i" class="pb-4">
              <v-row no-gutters>
                <v-col cols="6">
                  {{ item.title }}
                </v-col>
                <v-col cols="2">x{{ item.size }}</v-col>
                <v-col cols="4"> $ {{ item.price * item.size }} </v-col>
              </v-row>
              <v-divider></v-divider>
            </div>

            <div class="pb-4">
              <v-row no-gutters>
                <v-col class="text-h5 text-center" cols="6"> Subtotal </v-col>
                <v-col class="text-h5 text-center" cols="6">
                  $ {{ subtotal }}</v-col
                >
              </v-row>
            </div>

            <v-row justify="space-around">
              <v-col cols="auto">
                <v-dialog transition="dialog-bottom-transition" max-width="600">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      class="ma-2 botonComprar"
                      color="info"
                      v-bind="attrs"
                      v-on="on"
                      large
                    >
                      Pagar
                      <template v-slot:loader>
                        <span class="custom-loader">
                          <v-icon light>mdi-cached</v-icon>
                        </span>
                      </template>
                    </v-btn>
                  </template>
                  <template v-slot:default="dialog">
                    <v-card>
                      <v-toolbar color="primary" dark
                        >Tarjeta de pago</v-toolbar
                      >
                      <v-card-text>
                        <div class="text-h2 pa-12">
                          <v-text-field
                            label="Número de tarjeta"
                          ></v-text-field>
                          <v-text-field
                            label="CSV"
                          ></v-text-field>
                          <v-text-field
                            label="Fecha expiración"
                          ></v-text-field>
                          <v-text-field
                            label="Ciudad"
                          ></v-text-field>
                          <v-text-field
                            label="Dirección"
                          ></v-text-field>
                          <v-text-field
                            label="Nombre del que recibe"
                          ></v-text-field>
                        </div>
                      </v-card-text>
                      <v-card-actions class="justify-end">
                        <v-btn text @click="completarPago()">Pagar</v-btn>
                        <v-btn text @click="dialog.value = false">Close</v-btn>
                      </v-card-actions>

                      <v-snackbar
                        v-model="snackbar"
                        :timeout="timeout"
                      >
                        {{ text }}

                        <template v-slot:action="{ attrs }">
                          <v-btn
                            color="blue"
                            text
                            v-bind="attrs"
                            @click="snackbar = false"
                          >
                            Close
                          </v-btn>
                        </template>
                      </v-snackbar>
                    </v-card>
                  </template>
                </v-dialog>
              </v-col>
            </v-row>
          </v-card></v-col
        >
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";
import Loading from "@/components/static/loading.vue";

export default {
  props: {},
  data: () => ({
    infoProductos: [],
    subtotal: 0,
    loadingCarrito: true,
    noHayProductos: true,
    textoCarrito: "",
    snackbar: false,
    text: 'Pago realizado con éxito! :D',
    timeout: 2000,

  }),

  components: {
    Loading,
  },

  methods: {
    sortedArray: function () {
      function compare(a, b) {
        if (a.id < b.id) return -1;
        if (a.id > b.id) return 1;
        return 0;
      }

      return this.infoProductos.sort(compare);
    },

    validarConteo: function (cont, productosInStorage) {
      if (cont == 0) {
        this.infoProductos = [];
        this.loadingCarrito = false;
        this.noHayProductos = true;
        this.textoCarrito = "No hay productos en el carrito :(";
      } else if (productosInStorage.length == cont) {
        this.noHayProductos = false;
        this.loadingCarrito = false;
        this.textoCarrito = "";
        this.infoProductos = this.sortedArray();
      }
    },

    completarPago: function(){
      this.snackbar = true
      localStorage.removeItem('productos');
      this.obtenerInfoProds();
    },

    obtenerInfoProds: async function () {
      this.infoProductos = [];
      this.subtotal = 0;
      this.loadingCarrito = true;

      let cont = 0;

      if (localStorage.productos != null || localStorage.productos != undefined){
        let productosInStorage = JSON.parse(localStorage.productos);
        for (const product of productosInStorage) {
          await axios
            .get("https://api.escuelajs.co/api/v1/products/" + product.id)
            .then((response) => {
              response.data.size = product.size;
              this.subtotal += response.data.price * product.size;
              this.infoProductos.push(response.data);
            })
            .catch((e) => {
              this.eliminarCarrito(product.id);
            });
          cont++;
        }

        if (productosInStorage.length == cont) {
          this.validarConteo(cont, productosInStorage);
        }
      }else{
        this.infoProductos = [];
        this.loadingCarrito = false;
        this.noHayProductos = true;
        this.textoCarrito = "No hay productos en el carrito :(";
      }
    },

    aumentarCant(id) {
      this.loadingCarrito = true;
      let prodAgregar = {
        id: id,
        size: 1,
      };
      if (localStorage.productos != null) {
        let productosInStorage = JSON.parse(localStorage.productos);
        let posProducto = productosInStorage.findIndex(
          (producto) => producto.id === id
        );
        if (posProducto != -1) {
          prodAgregar.size = productosInStorage[posProducto].size + 1;
          productosInStorage[posProducto] = prodAgregar;
          localStorage.productos = JSON.stringify(productosInStorage);
        } else {
          console.log("producto no encontrado");
        }

        this.obtenerInfoProds();
      }
    },

    reducirCant(id) {
      this.loadingCarrito = true;
      let prodAgregar = {
        id: id,
        size: 1,
      };
      if (localStorage.productos != null) {
        let productosInStorage = JSON.parse(localStorage.productos);
        let posProducto = productosInStorage.findIndex(
          (producto) => producto.id === id
        );
        if (posProducto != -1) {
          prodAgregar.size = productosInStorage[posProducto].size - 1;
          productosInStorage[posProducto] = prodAgregar;
          localStorage.productos = JSON.stringify(productosInStorage);
        } else {
          console.log("producto no encontrado");
        }

        this.obtenerInfoProds();
      }
    },

    eliminarCarrito: function (id) {
      this.loadingCarrito = true;
      let prodAgregar = {
        id: id,
        size: 1,
      };
      if (localStorage.productos != null) {
        let productosInStorage = JSON.parse(localStorage.productos);
        let posProducto = productosInStorage.findIndex(
          (producto) => producto.id === id
        );
        if (posProducto != -1) {
          productosInStorage.splice(posProducto, 1);
          localStorage.productos = JSON.stringify(productosInStorage);
        }
        this.obtenerInfoProds();
      }
    },
  },

  mounted() {
    this.obtenerInfoProds();
  },
};
</script>

<style>
.inputCantidad {
  margin-top: 25px !important;
  max-width: 60px !important;
}
</style>
