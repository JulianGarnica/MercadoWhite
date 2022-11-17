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
              <h2 class="text-center ma-3"> Iniciar sesión</h2>
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
            Iniciar sesión
          </v-btn>


          </v-card-actions>
          <div class="text-center">
            ¿No tienes una cuenta?
            <router-link to="/register"> ¡Regístrate! </router-link>
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
    infoUser: Object
  },

  data() {
    const formLogin = Object.freeze({
        email: '',
        password: ''
      })

    return {
      rules: {

        email: [(val) => (val || "").length > 0 || "Este campo es requerido"],
        password: [(val) => (val || "").length > 0 || "Este campo es requerido"],
      },
      form: Object.assign({}, formLogin),
      formLogin

    };

  },

  computed: {
      formIsValid () {
        return (
          this.form.email &&
          this.form.password
        )
      },
    },



    methods: {
      resetForm () {
        this.form = Object.assign({}, this.formLogin)
        this.$refs.form.reset()
      },
      submit () {
        this.snackbar = true
        this.login()
        //this.resetForm()
      },

      login () {
        //https://api.escuelajs.co/api/v1/auth/login
        axios.post("https://api.escuelajs.co/api/v1/auth/login", this.form)
        .then(response => {
          localStorage.userToken = response.data.access_token
          this.$router.go("/")
          this.resetForm()
        });
      },

      ejecutarConsultaUsuario: function() {
        this.$emit("getInfoSesionUsuario");
        if(this.infoUser != {} || this.infoUser != undefined) {
          //this.$router.push("/")
        }
      }

      // getSesionUsuario () {
      //   let infoSesionUsuario = this.$emit("getInfoSesionUsuario");
      //   console.log(infoSesionUsuario)
      // }
    },

    watch: {
      infoUser: function(newValue) {
        if (newValue != null) {
          this.$router.push("/")
        }
      }
    },

    mounted() {
      this.ejecutarConsultaUsuario()
    },
};
</script>

<style scoped>
.botonComprar {
  width: 100%;
}
</style>
