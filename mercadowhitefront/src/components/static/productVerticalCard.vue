<template>
  <div>
    <v-hover v-slot="{ hover }">
      <router-link :to="'/producto/' + id">
        <v-card
          :loading="cargando"
          class="mx-auto  rounded-t-xl mt-5 mb-5"

          max-width="374"
        >
          <div :class="{ 'on-hover-border-up': hover }">
            <template slot="progress">
              <v-progress-linear
                color="deep-purple"
                height="10"
                indeterminate
              ></v-progress-linear>
            </template>

            <v-img height="250" :src="img" aspect-ratio="1" contain>
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
              <v-expand-transition>
                <div
                  v-if="hover"
                  class="rounded-t-xl d-flex transition-fast-in-fast-out darken-2 v-card--reveal text-h2 white--text"
                  style="height: 100%"
                >
                  Precio: ${{ precio }}
                </div>
              </v-expand-transition>
            </v-img>

            <v-card-title>{{ nombreProducto }}</v-card-title>
          </div>
          <div>
            <v-card-text
              class="hover-card rounded-b-xl"
              :class="{ 'on-hover-border-down': hover }"
              v-if="hover"
            >
              <v-expand-transition class="" rounded>
                <div
                  class="pa-4 my-4 text-subtitle-1 d-flex transition-fast-in-fast-out"
                >
                  {{ descripcion }}
                </div>
              </v-expand-transition>
            </v-card-text>
          </div>
        </v-card>
      </router-link>
    </v-hover>
  </div>
</template>

<script>
export default {
  props: {
    cargando: Boolean,
    nombreProducto: String,
    img: String,
    descripcion: String,
    precio: Number,
    id: Number,
  },

  data() {
    return {};
  },
};
</script>

<style>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  text-align: center;
  opacity: 0.9;
  position: absolute;
  width: 100%;
  background: #0e5066;
}

.hover-card {
  position: absolute !important;
  display: inline-block !important;
  z-index: 2;
  background: #fff;
  padding: 0;
  margin: 0;
}

.on-hover-border-up {
  border-top: 1px solid #1a8bb2;
  border-left: 1px solid #1a8bb2;
  border-right: 1px solid #1a8bb2;
  -webkit-box-shadow: 0px 0px 47px 21px rgba(0, 0, 0, 0.19);
  -moz-box-shadow: 0px 0px 47px 21px rgba(0, 0, 0, 0.19);
  box-shadow: 0px 0px 47px 21px rgba(0, 0, 0, 0.19);
}

.on-hover-border-down {
  border-left: 1px solid #1a8bb2;
  border-right: 1px solid #1a8bb2;
  border-bottom: 1px solid #1a8bb2;
}
</style>
