import { socket } from "../socket.js"
import { declare, update, bind, retrieve, reset } from "../state.js"

export const STATE = declare("CONNECT", "Game State")
export const STATE_DURATION = declare(0, "State duration")

export const CODE = declare("####", "Room Code")

export const PLAYERS = declare([], "Player List")

export const ROUND_NUM = declare(0, "Round Number")

export const MATCHLIST = declare({}, "Match List")

socket.addMessageHandler("init", (message) => {
  update(STATE, "LOBBY")
  update(CODE, message.code)
})

socket.addMessageHandler("state", (message) => {
  update(STATE, message.state)
  update(STATE_DURATION, message.duration)
})

socket.addMessageHandler("players", (message) => {
  update(PLAYERS, message.players)
})

socket.addMessageHandler("round_num", (message) => {
  update(ROUND_NUM, message.round_num)
})

socket.addMessageHandler("matchlist", (message) => {
  update(MATCHLIST, message.matchlist)
})

socket.addMessageHandler("reset", () => {
  update(STATE, "LOBBY")
})

socket.onClose(() => {
  reset(STATE)
  reset(CODE)
  reset(PLAYERS)
  reset(ROUND_NUM)
})
