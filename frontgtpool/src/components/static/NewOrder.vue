<template>
  <div>
    <v-card max-width="600" class="mx-auto">
      <v-list>
        <v-subheader>Productos seleccionados</v-subheader>
        <v-subheader inset
          >Para eliminar un producto, pulsa encima de su nombre</v-subheader
        >

          <h3 v-if="itemsSelected == []">No hay productos escogidos</h3>
          <v-list-item v-for="(item,i) in itemsSelected"
          :key="i"
          >
          {{i}}
            <v-list-item-avatar>
              <v-icon v-text="item.img"></v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
              <v-list-item-subtitle v-text="item.price"></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-row align="center">
                <v-col cols="12" sm="15">
                  <div class="text-center">
                    <div class="my-2">
                      <v-btn small @click="deleteShoppingCart(i)">
                        Eliminar
                        <v-icon right dark> mdi-information</v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-list-item-action>
          </v-list-item>
      </v-list>


      <v-subheader>Lista de productos</v-subheader>
      <v-list>
        <v-subheader inset
          >Para seleccionar un producto, pulsa encima de su nombre</v-subheader
        >
        <v-list-group
          v-for="item in items"
          :key="item.title"
          v-model="item.active"
          :prepend-icon="item.action"
          no-action
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="child in item.items"
            :key="child.title"
            link
            @click="addShoppingCart(child)"
          >
            <v-list-item-avatar>
              <v-icon v-text="child.img"></v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title v-text="child.title"></v-list-item-title>
              <v-list-item-subtitle v-text="child.price"></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-row align="center">
                <v-col cols="12" sm="15">
                  <div class="text-center">
                    <div class="my-2">
                      <v-btn small>
                        Ver más
                        <v-icon right dark> mdi-information</v-icon>
                      </v-btn>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-list-item-action>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    itemsSelected: [],
    items: [
      {
        action: "mdi-ticket",
        items: [
          {
            id: 1,
            title: "Combo #1 Costillas",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 2,
            title: "Combo #2 Chuleta",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 3,
            title: "Combo #3 1/4 de Pollo",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 4,
            title: "Combo #4 Teriyaki",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 5,
            title: "Combo #5 Alitas",
            price: 20000,
            img: "mdi-clipboard-text",
          },
        ],
        title: "Combos",
      },
      {
        action: "mdi-silverware-fork-knife",
        active: false,
        items: [
          {
            id: 6,
            title: "Lomo de cerdo",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 7,
            title: "Churrasco",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 8,
            title: "Pechuga",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 9,
            title: "Mojarra",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 10,
            title: "Trucha",
            price: 20000,
            img: "mdi-clipboard-text",
          },
        ],
        title: "Platos especiales",
      },
      {
        action: "mdi-school",
        items: [
          {
            id: 11,
            title: "1 pollo frito",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 12,
            title: "1/2 pollo frito",
            price: 20000,
            img: "mdi-clipboard-text",
          },
          {
            id: 13,
            title: "1/4 pollo frito",
            price: 20000,
            img: "mdi-clipboard-text",
          },
        ],
        title: "Pollo Frito",
      },
      {
        action: "mdi-human-male-female-child",
        items: [
          {
            id: 14,
            title: "Botella de agua",
            price: 2000,
            img: "mdi-clipboard-text",
          },
          {
            id: 15,
            title: "Cerveza Poker",
            price: 2000,
            img: "mdi-clipboard-text",
          },
          {
            id: 16,
            title: "Cerveza Club Colombia",
            price: 2000,
            img: "mdi-clipboard-text",
          },
        ],
        title: "Bebidas",
      },
    ],
  }),

  methods: {
    addShoppingCart: function (newElement) {
      this.itemsSelected.push(newElement);
    },
    deleteShoppingCart: function (oldElementToDelete) {
      console.log("deleting "+oldElementToDelete)
      this.itemsSelected.splice(oldElementToDelete,1)
    }
  },
};
</script>

<style></style>
