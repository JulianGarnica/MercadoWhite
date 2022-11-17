<template>
  <v-container >
    <br /><br />
    <v-row  no-gutters>
      <v-col class="d-flex justify-center" cols="12"  sm="12" md="8" >
        <v-sheet  class="align-center" max-width="720px" width="100%">
          <v-img
            :src="infoProducto.images[imagenSeleccionada]"
            width="720"
            class="mx-auto rounded align-center"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular
                  indeterminate
                  color="grey lighten-5"
                ></v-progress-circular>
              </v-row>
            </template>
          </v-img>
          <v-sheet class="" >
            <v-slide-group
              v-model="imagenSeleccionada"
              class="pa-1 "
              prev-icon="mdi-minus"
              next-icon="mdi-plus"
              show-arrows
              mandatory
            >
              <v-slide-item
                v-for="n in infoProducto.images"
                :key="n"
                v-slot="{ active, toggle }"

              >
                <v-card width="100" class="ma-1 rounded-xl" @click="toggle">
                  <v-img :src="n" class="rounded-xl">
                    <v-row class="fill-height" align="center" justify="center">
                      <v-scale-transition>
                        <v-card
                          v-if="active"
                          class="imageSelect"
                          height="150%"
                          width="100%"
                        >
                        </v-card>
                      </v-scale-transition>
                    </v-row>
                  </v-img>
                </v-card>
              </v-slide-item>
            </v-slide-group>
          </v-sheet>
        </v-sheet>

      </v-col>
      <v-col cols="12" sm="12" md="4" class="d-flex justify-center">
        <v-card
          class="pa-5  text-left rounded-lg"
          outlined
          max-width="400"
          width="100%"
        >
          <div class="grey--text">Nuevo | 18 vendidos</div>
          <div class="text-h4">{{ infoProducto.title }}</div>
          <br />
          <div class="text-h4 font-weight-light">
            $ {{ infoProducto.price }}
          </div>
          <br />
          <div>
            <v-icon>mdi-tag</v-icon>
            {{ infoProducto.category.name }}
          </div>
          <div>
            <v-icon>mdi-truck</v-icon>
            Envío gratis
          </div>
          <br />
          <br />
          <v-btn class="ma-2 botonComprar" color="info" large>
            Comprar ahora
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon light>mdi-cached</v-icon>
              </span>
            </template>
          </v-btn>

          <v-btn
            class="ma-2 botonComprar"
            color="info"
            large
            outlined
            @click="agregarCarrito()"
          >
            Agregar al carrito
            <template v-slot:loader>
              <span class="custom-loader">
                <v-icon light>mdi-cached</v-icon>
              </span>
            </template>
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
    <br><br>

    <v-row  no-gutters>
      <v-col class="d-flex justify-center" cols="12"  sm="12" md="8" >
        <v-card
          class="pa-5  text-left rounded-lg"
          width="100%"
          elevation="0"
        >
        <div class="text-h4">Descripción</div>
        <br>
        <v-divider></v-divider>
        <br>
        {{infoProducto.description}}
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="4" class="d-flex justify-center">
        <v-card
          class="pa-5  text-left rounded-lg"
          outlined
          max-width="400"
          width="100%"
        >
        <v-item-group>
        <v-row>
          <v-col v-for="n in productosCategoria" :key="n.id" cols="12" md="12">
            <product-vertical-card
              :nombreProducto="n.title"
              :img="n.images[0]"
              :descripcion="n.description"
              :precio="n.price"
              :id="n.id"
              class="productosVertical"
              v-if="infoProducto.id != n.id"
            ></product-vertical-card>
          </v-col>
        </v-row>
      </v-item-group>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import productVerticalCard from "@/components/static/productVerticalCard.vue";

export default {
  data() {
    return {
      infoProducto: {},
      productosCategoria: [],
      imagenSeleccionada: 0,
    };
  },

  components: {
    productVerticalCard
},

  mounted() {
    axios
      .get("https://api.escuelajs.co/api/v1/products/" + this.$route.params.id)
      .then((response) => {
        this.infoProducto = response.data;
        let idCategory = this.infoProducto.category.id
        axios.get("https://api.escuelajs.co/api/v1/categories/"+idCategory+"/products?offset=0&limit=4").then((response) => {
          this.productosCategoria = response.data;
          if (this.productosCategoria != []){
            this.mostrarProductos = true
          }else{
            this.mostrarProductos = false
          }
          this.cargando = false
        });
      });


  },

  methods: {

    agregarCarrito: function () {
      let prodAgregar = {
        id: this.infoProducto.id,
        size: 1,
      };
      if (localStorage.productos == null) {
        localStorage.productos = JSON.stringify([prodAgregar]);
      } else {
        let productosInStorage = JSON.parse(localStorage.productos);
        let posProducto = productosInStorage.findIndex(
          (producto) => producto.id === this.infoProducto.id
        );
        if (posProducto != -1) {
          prodAgregar.size = productosInStorage[posProducto].size + 1;
          productosInStorage[posProducto] = prodAgregar;
        } else {
          productosInStorage.push(prodAgregar);
        }

        localStorage.productos = JSON.stringify(productosInStorage);
      }

      this.$emit("activarShopCar");
    },
  },
};
</script>

<style>
.botonComprar {
  width: 95%;
}

.imageSelect {
  background: rgba(41, 41, 41, 0.531) !important;
}

.productosVertical{
  margin: 0 !important;
}
</style>
