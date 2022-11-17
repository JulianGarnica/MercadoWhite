<template>
  <div>
    <v-carousel
    cycle
    height="400"
    hide-delimiter-background
    show-arrows-on-hover
  >
    <v-carousel-item
    v-for="(item,i) in items"
      :key="i"
      :src="item.src"
    >

    </v-carousel-item>
  </v-carousel>
  </div>
</template>

<script>
export default {
  data (){
    return{
      items: [
          {
            src: 'https://http2.mlstatic.com/D_NQ_792184-MLA51668992169_092022-OO.webp',
          },
          {
            src: 'https://http2.mlstatic.com/D_NQ_675136-MLA51653453221_092022-OO.webp',
          }
        ],
    }
  }
}
</script>

<style>
</style>
