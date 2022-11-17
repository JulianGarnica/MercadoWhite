<template>
  <div class="d-flex justify-center">
    <v-card class="mt-15 pa-5" max-width="450px">
      <v-form ref="form" @submit.prevent="submit">
        <v-container fluid>
          <v-row>
            <v-col cols="12" sm="12">
              <v-img
                alt="Vuetify Logo"
                contain
                class="mx-auto"
                src="@/assets/logo-MercadoWhite2.png"
                transition="scale-transition"
                width="150"
              />
            </v-col>

            <v-col cols="12" sm="12">
              <h2 class="text-center ma-3">Registrarse</h2>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="form.name"
                :rules="rules.name"
                color="purple darken-2"
                label="Nombre"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="form.email"
                :rules="rules.email"
                color="purple darken-2"
                label="Correo"
                required
              ></v-text-field>
            </v-col>

            <v-col cols="12" sm="12">
              <v-text-field
                v-model="form.password"
                :rules="rules.password"
                color="purple darken-2"
                label="Contraseña"
                type="password"
                required
              ></v-text-field>
            </v-col>
          </v-row>

          <v-card-actions>
            <v-btn
              :disabled="!formIsValid"
              color="primary"
              type="submit"
              class="botonComprar"
              large
            >
              Regístrate
            </v-btn>
          </v-card-actions>
          <div class="text-center">
            ¿Ya tienes una cuenta?
            <router-link to="/login"> ¡Inicia sesión! </router-link>
          </div>
        </v-container>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    infoUser: Object,
  },

  data() {
    const formRegister = Object.freeze({
      name: "",
      email: "",
      password: "",
    });

    return {
      rules: {
        name: [(val) => (val || "").length > 0 || "Este campo es requerido"],
        email: [(val) => (val || "").length > 0 || "Este campo es requerido"],
        password: [
          (val) => (val || "").length > 0 || "Este campo es requerido",
        ],
      },
      form: Object.assign({}, formRegister),
      formRegister,
    };
  },

  computed: {
    formIsValid() {
      return this.form.name && this.form.email && this.form.password;
    },
  },

  methods: {
    resetForm() {
      this.form = Object.assign({}, this.formRegister);
      this.$refs.form.reset();
    },
    submit() {
      this.snackbar = true;
      this.register();
      //this.resetForm()
    },

    register() {
      console.log(this.form);
      //https://api.escuelajs.co/api/v1/auth/login
      axios
        .post("https://api.escuelajs.co/api/v1/users/", this.form)
        .then((response) => {
          //localStorage.userToken = response.data.access_token
          console.log(response);
          //this.$router.go("/login")
          this.resetForm();
        });
    },

    ejecutarConsultaUsuario: function () {
      this.$emit("getInfoSesionUsuario");
      if (this.infoUser != {} || this.infoUser != undefined) {
        //this.$router.push("/")
      }
    },

    // getSesionUsuario () {
    //   let infoSesionUsuario = this.$emit("getInfoSesionUsuario");
    //   console.log(infoSesionUsuario)
    // }
  },

  watch: {
    infoUser: function (newValue) {
      if (newValue != null) {
        this.$router.push("/");
      }
    },
  },

  mounted() {
    this.ejecutarConsultaUsuario();
  },
};
</script>

<style scoped>
.botonComprar {
  width: 100%;
}
</style>
