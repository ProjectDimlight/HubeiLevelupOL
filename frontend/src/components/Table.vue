<template>
  <table width="100%" height="100%">
  <tr>
    <td width="20%"></td>
    <td width="60%">
      <card :number="cards.length" :visible="false"/>
      <div style="margin: 20px; display:inline-block"></div>
      <card :key="index" v-for="(card_id, index) in round_cards[(player+2)%4]" :cardId="card_id" :visible="true"/>
    </td>
    <td width="20%"></td>
  </tr>

  <tr height="70%">
    <td>
      <card :number="cards.length" :visible="false"/>
      <div style="margin: 20px; display:inline-block"></div>
      <card :key="index" v-for="(card_id, index) in round_cards[(player+3)%4]" :cardId="card_id" :visible="true"/>
      </td>
    <td></td>
    <td>
      <card :key="index" v-for="(card_id, index) in round_cards[(player+1)%4]" :cardId="card_id" :visible="true"/>
      <div style="margin: 20px; display:inline-block"></div>
      <card :number="cards.length" :visible="false"/>
    </td>
  </tr>

  <tr>
    <td></td>
    <td>
      <card :key="index" v-for="(card_id, index) in cards" :cardId="card_id" :visible="true"/>
      <div style="margin: 20px; display:inline-block"></div>
      <card :key="index" v-for="(card_id, index) in round_cards[player]" :cardId="card_id" :visible="true"/>
    </td>
    <td>Score: {{score}}</td>
  </tr>
  </table>
</template>

<script>
import Card from './Card.vue'

export default {
  name: 'GamePlayTable',
  props: {
  },
  data () {
    return {
      score: 0,
      player: 0,
      cards: [1, 5, 7, 12, 50, 51, 52, 53],
      round_cards: [[2, 8], null, [3, 6], [0, 4]]
    }
  },
  components: {
    Card
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
