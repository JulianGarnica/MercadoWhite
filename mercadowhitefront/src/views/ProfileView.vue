<template>
  <div class="d-flex justify-center">
    <v-card class="mt-15 pa-5" max-width="450px">
        <v-container fluid>
          <v-row>
            <v-col cols="12" sm="12">
              <v-img
                alt="Vuetify Logo"
                contain
                class="mx-auto"
                src="https://upload.wikimedia.org/wikipedia/commons/9/96/User_icon-cp.png"
                transition="scale-transition"
                width="150"
              />
            </v-col>

            <v-col cols="12" sm="12">
              <h2 class="text-center ma-3">{{infoUser.name}}</h2>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="infoUser.name"
                color="purple darken-2"
                label="Nombre"
                disabled
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="infoUser.email"
                color="purple darken-2"
                label="Correo"
                disabled
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="infoUser.role"
                color="purple darken-2"
                label="Rol"
                disabled
                required
              ></v-text-field>
            </v-col>
          </v-row>


        </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  props: {
    infoUser: Object,
  },


  methods: {
    ejecutarConsultaUsuario: function () {
      this.$emit("getInfoSesionUsuario");
    },

    // getSesionUsuario () {
    //   let infoSesionUsuario = this.$emit("getInfoSesionUsuario");
    //   console.log(infoSesionUsuario)
    // }
  },

  watch: {
    infoUser: function (newValue) {
      console.log(this.infoUser)
      if (newValue == null) {
        this.$router.push("/login");
      }
    },
  },

  mounted() {
    this.ejecutarConsultaUsuario();
  },
};
</script>

<style></style>
