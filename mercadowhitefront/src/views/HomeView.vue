<template>
  <div>
    <v-parallax
    dark
    height="350"
    src="https://cdn.pixabay.com/photo/2018/07/18/13/05/ecommerce-3546296_960_720.jpg"
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        class="text-center mb-15 mt-15"
        cols="12"
      >
          <v-img
            alt="Vuetify Logo"
            contain
            class="mx-auto"
            src="@/assets/logo-MercadoWhite.png"
            transition="scale-transition"
            width="200"
          />
          <br>
        <h2 class="subheading">
          MercadoWhite
        </h2>

        <h4 class="subheading">
          Dale, gástate tu capricho ;)
        </h4>
      </v-col>
    </v-row>
  </v-parallax>

    <v-sheet min-height="70vh" rounded="lg">
      <v-item-group>
        <v-container>
          <home-carousel />
          <br>
          <v-app-bar color="secondary" dense dark >
            <v-spacer></v-spacer>
            <v-toolbar-title>Productos destacados</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-app-bar>
          <v-row align="center"
      justify="center">
            <v-col v-for="n in productosDestacados" :key="n.id" cols="12" md="4" lg="3">
              <product-vertical-card
                :nombreProducto="n.title"
                :img="n.images[0]"
                :descripcion="n.description"
                :precio="n.price"
                :id="n.id"
              ></product-vertical-card>
            </v-col>
          </v-row>

          <v-app-bar color="secondary" dense dark>
            <v-spacer></v-spacer>
            <v-toolbar-title>Categorías</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-app-bar>

          <category-with-img></category-with-img>
        </v-container>
      </v-item-group>
    </v-sheet>
  </div>
</template>

<script>
import HomeCarousel from "../components/HomeCarousel.vue";
import productVerticalCard from "@/components/static/productVerticalCard.vue";
import axios from "axios";
import CategoryWithImg from '@/components/categoryWithImg.vue';

export default {
  name: "Home",

  data() {
    return {
      info: null,
      productosDestacados: [],
    };
  },

  components: {
    HomeCarousel,
    productVerticalCard,
    CategoryWithImg,
  },

  mounted() {
    axios
      .get("https://api.escuelajs.co/api/v1/products?offset=0&limit=6")
      .then((response) => {
        this.productosDestacados = response.data;
      });

  },


};
</script>
