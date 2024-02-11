<template>
  <div :style="'height:' + (getWindowHeight()-100) + 'px'">
    <table width="100%" height="100%">
    <tr>
      <td width="20%"></td>
      <td width="60%">
        <span v-if="round_winner == (player+2)%4">★</span>
        <card :number="cards_count[(player+2)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+2)%4]" :cardId="card_id" :visible="true"/>
      </td>
      <td width="20%"></td>
    </tr>

    <tr height="70%">
      <td>
        <span v-if="round_winner == (player+3)%4">★</span>
        <card :number="cards_count[(player+3)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+3)%4]" :cardId="card_id" :visible="true"/>
        </td>
      <td>
        <div>
          Level: {{levels[level]}} <br/>
          Color: <span v-if="color != -1" :style="'color:' + styles[color][0]"> {{styles[color][1]}} </span> <span v-else> ? </span><br/>
          Score: {{score}} <br/>

          <Button :text="stages[stage]" :able="true" v-on:click="button()" />
        </div>
      </td>
      <td>
        <span v-if="round_winner == (player+1)%4">★</span>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+1)%4]" :cardId="card_id" :visible="true" />
        <div style="margin: 5px; display:inline-block"></div>
        <card :number="cards_count[(player+1)%4]" :visible="false"/>
      </td>
    </tr>

    <tr>
      <th colspan="3">
        <span v-if="round_winner == player">★</span>
        <card :key="index" v-for="(card_id, index) in sorted_cards" :cardId="card_id" :visible="true" v-on:click="toggle_choose(card_id)" :style="'top:' + (chosen.has(card_id) ? -10 : 0) + 'px;'"/>
        <div style="margin: 20px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[player]" :cardId="card_id" :visible="true"/>
      </th>
    </tr>
    </table>
  </div>
</template>

<script>
import Card from './Card.vue'
import Button from './Button.vue'
import card_info from './card.js'

const SIT = 100
const READY = 101
// const REJECT = -1
// const ACK = 0
// const BOTTOM = 1
const DRAW = 2
const PLAY = 3
const SCORE = 4
// const LEVEL = 5
const COLOR = 6
// const END = 7

export default {
  name: 'GamePlayTable',
  props: {
  },
  data () {
    return {
      username: 'sol',
      score: 0,
      player: 1,
      dealer: 0, 
      current_player: -1,
      round_winner: -1,
      color: -1,
      level: 0,
      styles: card_info.styles,
      colors: card_info.colors,
      levels: card_info.levels,
      cards_count: [0, 0, 0, 0],
      cards: [],
      round_cards: [[], [], [], []],
      stages: ['ready', 'declare', 'bottom', 'play'],
      stage: 0,
      chosen: new Set([]),
      sock: null
    }
  },
  computed: {
    sorted_cards () {
      return this.cards.toSorted(this.cmp)
    }
  },
  methods: {
    value_of_card (card) {
        let self = this
        let c = card_info.deck[card]
        if (c[1] == 'J')
            card += 100000
        else if (c[2] == card_info.levels[self.level])
            card += 10000
        else if (c[2] == '2')
            card += 1000
        if (c[0] == card_info.colors[self.color])
            card += 100
        return card
    },
    getWindowHeight () {
      return window.innerHeight
    },
    toggle_choose (card_id) {
      let self = this
      if (self.chosen.has(card_id)) {
        self.chosen.delete(card_id)
      } else {
        self.chosen.add(card_id)
      }
    },
    button () {
      let self = this
      if (self.stage == 0) {  // ready
        self.send({
          verb: SIT,
          username: self.username,
          table: 1,
          seat: self.player
        })
        self.send({
          verb: READY,
          username: self.username
        })
      } else if (self.stage == 1) {  // declare
        if (self.player != self.dealer) {
          // do nothing
          return
        }
      } else if (self.stage == 2) {  // bottom

      } else {  // play

      }
    },
    send (obj) {
      this.sock.send(JSON.stringify(obj))
    },
    receive (msg) {
      let obj = JSON.parse(msg.data)
      console.log(obj)
      this.operation(obj)
    },
    operation (obj) {
      let self = this
      if (obj['verb'] == DRAW) {
        if (obj['player'] == self.player) {
          self.cards.push(obj['card'])
        }
        self.cards_count[obj['player']]++
      } else if (obj['verb'] == COLOR) {
        self.color = card_info.colors.indexOf(obj['color'])
        console.log(self.color)
      } else if (obj['verb'] == PLAY) {
        self.round_cards = obj['round_cards']
        for (let i of self.round_cards)
          if (i)
            i.sort(self.cmp)
        let lp = (obj['current_player'] + 3) % 4
        if (self.round_cards[lp]) {
          self.cards_count[lp] -= self.round_cards[lp].length
          if (lp == self.player) {
            self.cards = self.cards.filter(e => !self.round_cards[lp].includes(e))
          }
        }
      } else if (obj['verb'] == SCORE) {
        self.round_winner = obj['round_winner']
        self.score = obj['total_score']
      }
    },
    cmp (a, b)  {
      return this.value_of_card(a) < this.value_of_card(b) ? 1 : -1
    },
    initWebSocket () {
      const url = process.env.NODE_ENV === "production" ? undefined : "ws://127.0.0.1:5000/echo";
      this.sock = new WebSocket(url)
      this.sock.onmessage = this.receive
    }
  },
  created() {
    this.initWebSocket()
  },
  components: {
    Card,
    Button
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
