import { socket } from "../socket.js"
import { declare, update, bind, retrieve, reset } from "../state.js"
import { debounce, throttle } from "../utils.js"

export const STATE = declare("CONNECT", "Page State")
export const CODE = declare("####", "Room Code")
export const NAME = declare("", "Player Name")
export const COLOR = declare("#000000", "Player Color")
export const READY = declare("", "Player Is Ready")
export const SUBMITTED = declare(false, "Player Submitted Answer")

bind(COLOR, throttle((c) => {
  socket.send({
    type: "playercolor",
    name: retrieve(NAME),
    color: c,
  })
}, 100))

bind(READY, debounce((r) => {
  socket.send({
    type: "playerready",
    name: retrieve(NAME),
    ready: r,
    color: retrieve(COLOR),
  })
}, 100))

socket.addMessageHandler("state", (message) => {
  update(STATE, message.state)
  socket.send({
    type: "ack",
    ack: "state"
  })
})

socket.addMessageHandler("reset", () => {
  update(STATE, "LOBBY")
  reset(READY)
  reset(SUBMITTED)
})

socket.onClose(() => {
  reset(CODE)
  reset(NAME)
  reset(COLOR)
  reset(READY)
  reset(SUBMITTED)
})
