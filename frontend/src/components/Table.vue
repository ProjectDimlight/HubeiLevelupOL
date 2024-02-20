<template>
  <div :style="'height:' + (getWindowHeight()-100) + 'px'">
    <div v-if="stage == 0">
      <div style="border-bottom: 1px solid grey; margin-bottom: 20px;">
        用户名: <input type="text" id="username" v-model="username" />
        桌号： <input type="text" id="table" v-model="table" />
        <Button style="margin-left: 20px" v-on:click="sit(-1)" :able="true" :text="'上桌'"/>
      </div>
      <div v-if="owner != ''">
        <div> 桌主: {{owner}} </div>
        <div :key="index" v-for="(seat, index) in seats" style="display: inline-block; margin: 5px;">
          <Button v-if="seat == null" v-on:click="sit(index)" :able="true" :text="index.toString()"/>
          <Button v-else-if="seat == username || owner == username" v-on:click="kick(index)" color="rgb(230, 180, 70)" :able="true" :text="seat"/>
          <div v-else>{{seat}}</div>
        </div>
        <div v-if="owner == username">
          庄家:
          <select id="dealer" v-model="create_dealer">
            <option :value="-1">抢叫</option>
            <option :key="index" v-for="(seat, index) in seats" :value="index">
              {{seat ? seat : "Bot" + index}}
            </option>
          </select>
          级牌:
          <select id="level" v-model="create_level">
            <option :key="index" v-for="(level, index) in levels" :value="level">
              {{level}}
            </option>
          </select>
          <Button style="margin-left: 20px" v-on:click="button()" :able="true" :text="'开局'"/>
        </div>
      </div>
      <div v-else>
        <img :src="image" /><br/>
        欢迎来到升级大战OL！<br/>
        点击侧边问号查看说明。<br/>
        开源链接：<a href="https://github.com/ProjectDimlight/HubeiLevelupOL">HubeiLevelupOL</a>
      </div>
      <div style="margin-top: 30px;">
        <span>{{info}}</span>
      </div>
    </div>
    <table width="100%" height="100%" v-else>
    <tr height="20%">
      <td width="25%">
        <card :key="index" v-for="(card_id, index) in bottom" :cardId="card_id" :visible="true" />
      </td>
      <td width="50%">
        <span style="margin-right: 10px;">{{seats[(player+2)%4] ? seats[(player+2)%4] : "Bot" + (player+2)%4}}</span>
        <span v-if="round_winner == (player+2)%4">★</span>
        <card :number="cards_count[(player+2)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+2)%4]" :cardId="card_id" :visible="true"/>
      </td>
      <td width="25%"></td>
    </tr>

    <tr height="60%">
      <td>
        <span style="margin-right: 10px;">{{seats[(player+3)%4] ? seats[(player+3)%4] : "Bot" + (player+3)%4}}</span>
        <span v-if="round_winner == (player+3)%4">★</span>
        <card :number="cards_count[(player+3)%4]" :visible="false"/>
        <div style="margin: 5px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+3)%4]" :cardId="card_id" :visible="true"/>
        </td>
      <td>
        <div>
          级牌: {{levels[level]}} <br/>
          庄家: {{dealer == -1 ? '?' : seats[dealer] ? seats[dealer] : 'Bot' + dealer}} <br/>
          花色: <span v-if="color != -1" :style="'color:' + styles[color][0]"> {{styles[color][1]}} </span> <span v-else> ? </span><br/>
          散家分数: {{score}} <br/>
          <br/>
          <br/>
          <span>{{info}}</span><br/>
          <span v-if="time > 0">倒计时: {{time}}<br/></span>
          <Button :text="stages[stage]" :able="true" v-on:click="button()" style="width: 100px;" />
        </div>
      </td>
      <td>
        <span style="margin-right: 10px;">{{seats[(player+1)%4] ? seats[(player+1)%4] : "Bot" + (player+1)%4}}</span>
        <span v-if="round_winner == (player+1)%4">★</span>
        <card :key="index" v-for="(card_id, index) in round_cards[(player+1)%4]" :cardId="card_id" :visible="true" />
        <div style="margin: 5px; display:inline-block"></div>
        <card :number="cards_count[(player+1)%4]" :visible="false"/>
      </td>
    </tr>

    <tr height="20%">
      <th colspan="3">
        <span style="margin-right: 10px;">{{seats[player] ? seats[player] : "Bot" + player}}</span>
        <span v-if="round_winner == player">★</span>
        <div v-if="seats[player] == username" style="display:inline-block">
          <card :key="index" v-for="(card_id, index) in sorted_cards" :cardId="card_id" :visible="true" v-on:click="toggle_choose(card_id)" :style="'top:' + (chosen.has(card_id) ? -10 : 0) + 'px;'"/>
        </div>
        <div v-else style="display:inline-block">
          <card :number="cards_count[player]" :visible="false"/>
        </div>
        <div style="margin: 20px; display:inline-block"></div>
        <card :key="index" v-for="(card_id, index) in round_cards[player]" :cardId="card_id" :visible="true"/>
      </th>
    </tr>
    </table>
  </div>

  <Button v-on:click="readme_hidden = !readme_hidden" :able="true" text="？" style="position: fixed; right: 10px; top: 50px;"></Button>
  <Button v-on:click="leave()" :able="true" text="退" style="position: fixed; right: 10px; top: 80px;"></Button>
  <ReadMe :hidden="readme_hidden"> </ReadMe>
</template>

<script>
import image from "../../public/icon.jpg"
import Card from './Card.vue'
import Button from './Button.vue'
import ReadMe from './Readme.vue'
import card_info from './card.js'

const SIT = 100
const READY = 101
const KICK = 102
const LEAVE = 103
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
      image: image,
      readme_hidden: true,
      time: 0,
      timer_time_out: -1,

      username: '',
      table: '',
      owner: '',
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

      stages: ['准备', '叫牌', '扣牌', '出牌', '退出'],
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
        table: self.table,
        seat: seat
      })
    },
    kick (seat) {
      let self = this
      self.send({
        verb: KICK,
        username: self.username,
        seat: seat
      })
    },
    leave () {
      let self = this
      self.send({
        verb: LEAVE,
        username: self.username
      })
    },
    button () {
      let self = this
      if (self.stage == 0) {  // ready
        if (!card_info.levels.includes(self.create_level))
          return
        let dealer = self.create_dealer
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
    timer (t) {
      this.cancel_timer()
      if (t <= 0)
        return
      this.count_down(t)
    },
    count_down (t) {
      let self = this
      self.time = t
      self.timer_time_out = setTimeout(() => {
          self.count_down(t - 1)
      }, 1000)
    },
    cancel_timer () {
      this.time = 0
      clearTimeout(this.timer_time_out)
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
        self.owner = obj['owner']
        let i = self.seats.indexOf(self.username)
        if (i != -1) {
          self.player = i
        } else {
          self.player = 0
        }
      } else if (obj['verb'] == LEAVE) {
        self.owner = ''
        self.stage = 0
      } else if (obj['verb'] == REJECT) {
        if (obj['reason']) {
          self.display(obj['reason'])
        } else 
          self.display("违规操作。")
      } else if (obj['verb'] == RECONNECT) {
        self.stage = obj['stage']
        self.player = obj['player']
        self.level = card_info.levels.indexOf(obj['level'])
        self.dealer = obj['dealer']

        self.color = obj['color'] == null ? -1 : card_info.colors.indexOf(obj['color'])
        self.score = obj['score']

        self.round_winner = obj['round_winner']
        self.cards = obj['cards']
        self.chosen.clear() 
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
        if ('card' in obj) {
          self.cards.push(obj['card'])
        } else {
          self.cards_count[obj['player']]++
        }
      } else if (obj['verb'] == BOTTOM) {
        self.cards = self.cards.concat(obj['cards'])
        self.display("请庄家扣牌。")
        self.timer(obj['time'])
        self.stage = 2
      } else if (obj['verb'] == ACK) {
        self.cards = self.cards.filter(e => !obj['bottom'].includes(e))
        self.bottom = obj['bottom']
      } else if (obj['verb'] == PLAY) {
        self.stage = 3
        self.round_cards = obj['round_cards']
        self.current_player = obj['current_player']
        if (self.current_player == self.player && !obj['round_cards'][self.player]) {
          self.display("轮到你了。")
          self.timer(obj['time'])
        } else
          self.cancel_timer()

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
          let winner = obj['winner'] ? '散家' : '庄家'
          self.display(winner + ' 获胜，等级 +' + obj['level'], false)
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
    Button,
    ReadMe
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input {
  width: 50px;
}
</style>
