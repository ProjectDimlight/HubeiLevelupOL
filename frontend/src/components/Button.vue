<template>
  <div :class="'button ' + (able ? 'able' : '') " :style="color ? 'background-color: ' + color : '' " v-html="text">
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
    color: String,
    able: Boolean
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.button {
    padding: 3px 10px;
    color: white;
    display: inline-block;
}

.able {
    background-color: green;
    transition: 0.7s;
}

.able:hover {
    background-color: rgb(210, 210, 210);
    color: black;
    transition: 0.7s;
}
</style>
