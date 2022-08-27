<template>
  <v-item>
    <v-card class="d-flex align-center cardsTables">
      <div class="numberTable">
        <h2>{{ tableNumber }}</h2>
      </div>

      <div class="contentCardTable">
        <div class="text-center inside">
          <div>
            <h2>Puntaje: {{ numberTiro }}</h2>
          </div>
          <div>
            <v-btn class="botonesAcciones" @click="disminuirTiro">
              <v-icon>mdi-arrow-left-thick</v-icon>
            </v-btn>
            <v-btn class="botonesAcciones" @click="aumentarTiro">
              <v-icon>mdi-arrow-right-thick</v-icon>
            </v-btn>
          </div>
        </div>
      </div>
    </v-card>
  </v-item>
</template>

<script>
export default {
  props: ["tableNumber"],
  data: () => ({
    numberTiro: 0,
  }),
  methods: {
    aumentarTiro: function () {
      if (this.numberTiro >= 0) {
        this.numberTiro++;
      }
    },
    disminuirTiro: function () {
      if (this.numberTiro > 0) {
        this.numberTiro--;
      }
    },
  },
};
</script>

<style>
.cardsTables {
  margin: 30px;
  height: auto;
  min-height: 200px;
}

.cardsTables .contentCardTable {
  margin-left: 8%;
  height: 100%;
}

.cardsTables .contentCardTable .inside {
  margin-top: 0%;
}
.cardsTables .contentCardTable .botonesAcciones {
  width: 100px;
  min-height: 50px;
  margin: 10px;
}

.cardsTables .numberTable {
  width: 100px;
  height: auto;
  min-height: 270px;
  text-align: center;
  background: #000;
  color: #fff;
}

.cardsTables .numberTable h2 {
  margin-top: 90%;
  font-size: 50px;
}

@media only screen and (max-width: 600px) {
  .cardsTables {
    margin: 0;
    height: auto;
    min-height: 200px;
  }
  .cardsTables .contentCardTable {
    margin-left: 8%;
  }
  .cardsTables .contentCardTable .inside {
    margin-top: 0%;
  }

  .cardsTables .numberTable {
    width: 70px;
    height: 100%;
    text-align: center;
    background: #000;
    color: #fff;
  }
  .cardsTables .numberTable h2 {
    margin-top: 100%;
    font-size: 50px;
  }
}
</style>
