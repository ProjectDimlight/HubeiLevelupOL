<template>
  <div v-if="visible" class="card" :style="'color:' + deck[cardId][0]" v-html="deck[cardId][2] + deck[cardId][1]">
  </div>
  <div v-else class="card" style="background-color:rgb(160, 160, 160)" v-html="'x' + number">
  </div>
</template>

<script>
import card_info from './card.js'

export default {
  name: 'GameCard',
  data () {
    return {
      deck: card_info.deck
    }
  },
  props: {
    cardId: Number,
    visible: Boolean,
    number: Number
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.card {
  width: 30px;
  height: 40px;
  border: 2px grey solid;
  display: inline-block;
  position: relative;
}
</style>
