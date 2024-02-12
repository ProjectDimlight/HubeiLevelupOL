<template>
  <div :class="'button ' + (able ? 'able' : '') " v-html="text">
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
    text: String,
    able: Boolean
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.button {
    padding: 3px 10px;
    background-color: rgb(90, 90, 90);
    color: white;
    display: inline-block;
}

.able {
    background-color: green;
    transition: 0.7s;
}

.able:hover {
    background-color: rgb(190, 255, 190);
    color: black;
    transition: 0.7s;
}
</style>
