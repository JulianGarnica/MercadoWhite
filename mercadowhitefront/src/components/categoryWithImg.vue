<template>
  <v-sheet class="mx-auto">
    <v-slide-group v-model="model" class="pa-4" center-active show-arrows>
      <v-slide-item
        v-for="n in categorias"
        :key="n.id"
        v-slot="{ active, toggle }"
      >
        <v-card
          :color="active ? 'primary' : 'grey lighten-1'"
          class="ma-4"
          height="100"
          width="200"
          @click="toggle() ;consultarProductos()"
        >
          <v-img :src="n.image" height="60" class="grey darken-4">
            <v-row class="fill-height" align="center" justify="center">
              <v-expand-transition>
                <div
                  v-if="active"
                  class="d-flex transition-fast-in-fast-out darken-2 v-card--reveal text-h2 white--text"
                  style="height: 100%"
                >
                  <v-icon
                    color="white"
                    size="48"
                    v-text="'mdi-close-circle-outline'"
                  ></v-icon>
                </div>
              </v-expand-transition>
            </v-row>
          </v-img>
          <v-card-title class="text-subtitle-1"> {{ n.name }} </v-card-title>
        </v-card>
      </v-slide-item>
    </v-slide-group>

    <v-sheet rounded="lg" v-if="!cargando">
      <v-item-group v-if="mostrarProductos">
        <v-row>
          <v-col v-for="n in productosCategoria" :key="n.id" cols="12" md="2">
            <product-vertical-card
              :nombreProducto="n.title"
              :img="n.images[0]"
              :descripcion="n.description"
              :precio="n.price"
              :id="n.id"
            ></product-vertical-card>
          </v-col>
        </v-row>
      </v-item-group>
    </v-sheet>
    <v-sheet v-else>
      <Loading></Loading>
    </v-sheet>
  </v-sheet>
</template>

<script>
import axios from "axios";
import productVerticalCard from "@/components/static/productVerticalCard.vue";
import Loading from "@/components/static/loading.vue"


export default {
  data() {
    return {
      categorias: [],
      productosCategoria: [],
      model: null,
      cargando: false,
      mostrarProductos: false
    };
  },

  components: {
    productVerticalCard,
    Loading
},

  mounted() {
    axios.get("https://api.escuelajs.co/api/v1/" + "categories").then((response) => {
      this.categorias = response.data;
    });
  },

  methods: {

    consultarProductos: function(){
      if (this.model != null){
        this.cargando = true
        let idCategory = this.model+1
        axios.get("https://api.escuelajs.co/api/v1/categories/"+idCategory+"/products").then((response) => {
          this.productosCategoria = response.data;
          if (this.productosCategoria != []){
            this.mostrarProductos = true
          }else{
            this.mostrarProductos = false
          }
          this.cargando = false
        });
      }else{
        this.mostrarProductos = false
      }
    }
  }
};
</script>

<style></style>
