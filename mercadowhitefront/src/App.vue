<template>
  <v-app>
    <Menu
      :infoUser="infoUser"
      ref="menuRef"
      @getInfoSesionUsuario="getInfoSesionUsuario()"
      @activarShopCar="activarShopCar()"
    ></Menu>

    <v-main>
      <router-view
        :infoUser="infoUser"
        :key="$route.fullPath"
        @getInfoSesionUsuario="getInfoSesionUsuario()"
        @activarShopCar="activarShopCar()"
      />
    </v-main>
    <v-dialog
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
      v-model="mostrarShopCar"
    >
      <v-card class="overflow-auto">
        <v-btn
          class="ma-6"
          text
          color="red"
          @click="
            mostrarShopCar = !mostrarShopCar;
            actualizarContadorCarrito();
          "
        >
          Cerrar carrito de compras
        </v-btn>
        <Shopcar v-if="mostrarShopCar"></Shopcar>
        <br />
      </v-card>
    </v-dialog>

    <Footer></Footer>
  </v-app>
</template>

<script>
import axios from "axios";
import Menu from "@/components/Menu.vue";
import Footer from "@/components/Footer.vue";
import Shopcar from "./components/static/shopcar.vue";

export default {
  name: "App",

  data: () => ({
    mostrarShopCar: false,
    infoUser: null,
  }),

  methods: {
    activarShopCar: function () {
      this.actualizarContadorCarrito;
      this.mostrarShopCar = true;
    },

    actualizarContadorCarrito: function () {
      this.$refs.menuRef.obtenerElementosCarrito();
    },

    obtenerInfoSesionUsuario: function () {
      let tokenUser = localStorage.userToken;
      if (tokenUser != null || tokenUser != undefined) {
        let headers = {
          Authorization: "Bearer " + tokenUser,
        };

        axios
          .get("https://api.escuelajs.co/api/v1/auth/profile", {
            headers: headers,
          })
          .then((response) => {
            this.infoUser = response.data;
          })
          .catch((e) => {
            this.infoUser = null;
          });
      } else {
        this.infoUser = null;
      }
    },

    getInfoSesionUsuario: function () {
      this.obtenerInfoSesionUsuario();
    },
  },

  mounted() {
    this.obtenerInfoSesionUsuario();
  },

  components: {
    Menu,
    Footer,
    Shopcar,
  },
};
</script>

<style></style>
