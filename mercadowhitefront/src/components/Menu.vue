<template>
  <v-app-bar app color="primary" dark>
    <v-spacer></v-spacer>
    <router-link to="/" class="">
      <v-img
        alt="Vuetify Logo"
        class="shrink mr-2"
        contain
        src="@/assets/logo-MercadoWhite2.png"
        transition="scale-transition"
        width="55"
      />
    </router-link>
    <v-toolbar-title class="titulo"
      >MercadoWhite
      <p class="subtitulo">
        Compra, sé feliz
      </p></v-toolbar-title
    >

    <v-spacer></v-spacer>
    <v-text-field
      placeholder="Buscar producto..."
      outlined
      class="campoBusqueda"
      prepend-inner-icon="mdi-magnify"
      filled
      rounded
    >
    </v-text-field>
    <v-spacer></v-spacer>

    <v-badge
      class="mr-4"
      color="secondary"
      overlap
      :content="conteoProdsCarrito"
    >
      <v-btn text elevation="2" fab @click="activarShopCarEvent()">
        <v-icon>mdi-cart</v-icon>
      </v-btn>
    </v-badge>

    <v-menu open-on-hover offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn text elevation="2" fab v-bind="attrs" v-on="on">
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item v-for="(item, index) in items" :key="index">
          <router-link :to="item.url" class="" v-if="!item.hasFunction && item.url != ''">
            <v-list-item-title >{{ item.title }}</v-list-item-title>
          </router-link>
          <div v-else-if="item.hasFunction">
            <v-btn
              color="primary"
              type="submit"
              class="botonComprar"
              large
              @click="cerrarSesion()"

            >
              {{item.title}}
            </v-btn>
          </div>

          <div v-else>
            <v-list-item-title >{{ item.title }}</v-list-item-title>
          </div>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-spacer></v-spacer>
  </v-app-bar>
</template>

<script>
export default {
  props: {
    infoUser: Object,
  },

  data() {
    return {
      conteoProdsCarrito: 0,
      items: [
        { title: "Iniciar Sesión", url: "/login", hasFunction: false },
        { title: "Registrarse", url: "/register", hasFunction: false },
      ],
    }
  },

  mounted() {
    this.obtenerElementosCarrito();
    this.ejecutarConsultaUsuario();
  },

  watch: {
    infoUser: function(newValue) {
      if (newValue != null) {
        this.items = [
          { title: newValue.name, url: ""},
          { title: "Mi perfil", url: "/profile" },
          { title: "Cerrar Sesión", url: "", hasFunction: true },
        ];
      }
    }
  },

  methods: {
    activarShopCarEvent: function () {
      this.$emit("activarShopCar");
    },

    ejecutarConsultaUsuario:  function () {
      this.$emit("getInfoSesionUsuario");
      if (this.infoUser != {} || this.infoUser != undefined) {
        //this.$router.push("/")
      }
    },

    cerrarSesion: function(){

      localStorage.removeItem('userToken');
      this.$router.go()
    },

    obtenerElementosCarrito: function () {
      this.conteoProdsCarrito = 0;
      if(localStorage.productos != undefined || localStorage.productos != null){
        for (const product of JSON.parse(localStorage.productos)) {
          this.conteoProdsCarrito += product.size;
        }
      }
    },
  },
};
</script>

<style>
.campoBusqueda {
  transform: scale(0.8);
  margin-top: 20px !important;
}

.titulo {
  margin-top: 5px;
}

.titulo .subtitulo {
  font-size: 10px;
  margin-top: -6px;
}

.v-badge__badge {
  inset: auto auto calc(100% - 20px) calc(100% - 20px) !important;
}
</style>
