<template>
  <div :style="'height:' + (getWindowHeight()-100) + 'px'">
    <div v-if="stage == 0">
      <div style="border-bottom: 1px solid grey; margin-bottom: 20px;">
        Username: <input type="text" id="username" v-model="username" />
        Table: <input type="text" id="table" v-model="table" />
        <Button style="margin-left: 20px" v-on:click="sit(-1)" :able="true" :text="'Enter'"/>
      </div>
      <div>
        <div>
        <div :key="index" v-for="(seat, index) in seats" style="display: inline-block; margin: 5px;">
          <Button v-if="seat == null" v-on:click="sit(index)" :able="true" :text="index.toString()"/>
          <div v-else>{{seat}}</div>
        </div>
        <Button v-on:click="sit(-1)" :able="true" :text="'Leave'" style="margin-left: 50px;"/>
        </div>
        <div>
          Dealer: <input type="text" id="dealer" v-model="create_dealer" />
          Level: <input type="text" id="level" v-model="create_level" />
          <Button style="margin-left: 20px" v-on:click="button()" :able="true" :text="'Start'"/>
        </div>
      </div>
    </div>
    <table width="100%" height="100%" v-else>
    <tr height="20%">
      <td width="25%">
        <card :key="index" v-for="(card_id, index) in bottom" :cardId="card_id" :visible="true" />
      </td>
      <td width="50%">
        <span style="margin-right: 10px;">{{seats[(player+2)%4] ? seats[(player+2)%4] : "Bot"}}</span>
        <span v-if="round_winner == (player+2)%4">★</span>
        <card :number="cards_count[(player+2)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+2)%4]" :cardId="card_id" :visible="true"/>
      </td>
      <td width="25%"></td>
    </tr>

    <tr height="60%">
      <td>
        <span style="margin-right: 10px;">{{seats[(player+3)%4] ? seats[(player+3)%4] : "Bot"}}</span>
        <span v-if="round_winner == (player+3)%4">★</span>
        <card :number="cards_count[(player+3)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+3)%4]" :cardId="card_id" :visible="true"/>
        </td>
      <td>
        <div>
          Level: {{levels[level]}} <br/>
          Dealer: {{dealer == -1 ? '?' : seats[dealer]}} <br/>
          Color: <span v-if="color != -1" :style="'color:' + styles[color][0]"> {{styles[color][1]}} </span> <span v-else> ? </span><br/>
          Score: {{score}} <br/>
          <br/>
          <span>{{info}}</span><br/>
          <Button :text="stages[stage]" :able="true" v-on:click="button()" style="width: 100px;" />
        </div>
      </td>
      <td>
        <span style="margin-right: 10px;">{{seats[(player+1)%4] ? seats[(player+1)%4] : "Bot"}}</span>
        <span v-if="round_winner == (player+1)%4">★</span>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+1)%4]" :cardId="card_id" :visible="true" />
        <div style="margin: 5px; display:inline-block"></div>
        <card :number="cards_count[(player+1)%4]" :visible="false"/>
      </td>
    </tr>

    <tr height="20%">
      <th colspan="3">
        <span style="margin-right: 10px;">{{username}}</span>
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
const REJECT = -1
const ACK = 0
const BOTTOM = 1
const DRAW = 2
const PLAY = 3
const SCORE = 4
const LEVEL = 5
const COLOR = 6
// const END = 7
const RECONNECT = 8

export default {
  name: 'GamePlayTable',
  props: {
  },
  data () {
    return {
      username: '',
      table: '',
      seats: [null, null, null, null],
      create_dealer: '',
      create_level: '',
      
      player: 1,
      score: 0,
      dealer: -1,
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
      bottom: [],

      stages: ['ready', 'declare', 'bottom', 'play', 'end'],
      stage: 0,
      chosen: new Set([]),
      sock: null,
      info: "",
      info_time_out: -1
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
        if (c[1] == card_info.colors[self.color])
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
    sit (seat) {
      let self = this
      self.send({
        verb: SIT,
        username: self.username,
        table: table,
        seat: seat
      })
    },
    button () {
      let self = this
      if (self.stage == 0) {  // ready
        if (!card_info.levels.includes(self.create_level))
          return
        let dealer = -1
        if (['0', '1', '2', '3'].includes(self.create_dealer))
          dealer = parseInt(self.create_dealer)
        self.send({
          verb: READY,
          username: self.username,
          level: self.create_level,
          dealer: dealer
        })
      } else if (self.stage == 1) {  // declare
        let a = Array.from(self.chosen)
        if (a.length != 1)
          return

        self.send({
          verb: COLOR,
          username: self.username,
          card: a[0]
        })
        self.chosen.clear() 
      } else if (self.stage == 2) {  // bottom
        if (self.player != self.dealer) {
          // do nothing
          return
        }
        self.send({
          verb: BOTTOM,
          username: self.username,
          cards: Array.from(self.chosen)
        })
        self.chosen.clear() 
      } else if (self.stage == 3) {  // play
        self.send({
          verb: PLAY,
          username: self.username,
          cards: Array.from(self.chosen)
        })
        self.chosen.clear() 
      } else if (self.stage == 4) {
        self.stage = 0
        self.info = ''
      }
    },
    send (obj) {
      try {
        this.sock.send(JSON.stringify(obj))
      } catch(e) {
        this.initWebSocket()
        this.sock.send(JSON.stringify(obj))
      }
    },
    receive (msg) {
      let obj = JSON.parse(msg.data)
      this.operation(obj)
    },
    display (msg, disapper=true) {
      let self = this
      if (self.info_time_out != -1) {
        clearTimeout(self.info_time_out)
        self.info_time_out = -1
      }
      self.info = msg
      if (disapper) {
        self.info_time_out = setTimeout(() => {
          self.info = ''
        }, 2000)
      }
    },
    operation (obj) {
      let self = this
      if (obj['verb'] == SIT) {
        self.seats = obj['seats']
        let i = self.seats.indexOf(self.username)
        if (i != -1) {
          self.player = i
        }
      } else if (obj['verb'] == REJECT) {
        self.display("Operation illegal.")
      } else if (obj['verb'] == RECONNECT) {
        self.stage = obj['stage']
        self.player = obj['player']
        self.level = card_info.levels.indexOf(obj['level'])
        self.dealer = obj['dealer']

        self.color = obj['color'] == null ? -1 : card_info.colors.indexOf(obj['color'])
        self.score = obj['score']

        self.round_winner = obj['round_winner']
        self.cards = obj['cards']
        self.round_cards = obj['round_cards']
        self.current_player = obj['current_player']

        self.cards_count = obj['cards_count']
      } else if (obj['verb'] == LEVEL) {
        self.level = card_info.levels.indexOf(obj['level'])
        self.dealer = obj['dealer']

        self.score = 0
        self.color = -1
        self.cards = []
        self.cards_count = [0, 0, 0, 0]
        self.bottom = []
        self.round_cards = [[], [], [], []]

        self.stage = 1
      } else if (obj['verb'] == COLOR) {
        self.color = card_info.colors.indexOf(obj['color'])
        self.dealer = obj['dealer']
      } else if (obj['verb'] == DRAW) {
        if (obj['player'] == self.player) {
          self.cards.push(obj['card'])
        }
        self.cards_count[obj['player']]++
      } else if (obj['verb'] == BOTTOM) {
        self.cards = self.cards.concat(obj['cards'])
        self.stage = 2
      } else if (obj['verb'] == ACK) {
        self.cards = self.cards.filter(e => !obj['bottom'].includes(e))
      } else if (obj['verb'] == PLAY) {
        self.stage = 3
        self.round_cards = obj['round_cards']
        self.current_player = obj['current_player']
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
        if ('winner' in obj) {
          // final score
          self.bottom = obj['bottom']
          let winner = obj['winner'] ? 'Challenger' : 'Dealer'
          self.display(winner + ' wins, level +' + obj['level'], false)
          self.stage = 4
        }
      }
    },
    cmp (a, b)  {
      return this.value_of_card(a) < this.value_of_card(b) ? 1 : -1
    },
    initWebSocket () {
      console.log("init")
      let self = this
      const socketProtocol = (window.location.protocol === 'https:' ? 'wss:' : 'ws:')
      const port = ':5000';
      const echoSocketUrl = socketProtocol + '//' + window.location.hostname + port + '/ws'
      const url = process.env.NODE_ENV === "production" ? echoSocketUrl : "ws://127.0.0.1:5000/ws";
      self.sock = new WebSocket(url)
      self.sock.onmessage = self.receive
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
