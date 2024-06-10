import { View } from "../../view.js"
import { getelem } from "../../utils.js"
import { socket } from "../../socket.js"

import { ROUND_NUM } from "../model.js"
import { bind } from "../../state.js"

import { PROGRESSBAR } from "../bar.js"

const ROUNDNUMTEXT = getelem("roundstart-roundnumtext")

export const ROUNDSTART = new View({
  name: "Round Start",
  id: "div-roundstart",
  init: function() {
    bind(ROUND_NUM, (round_num) => {
      ROUNDNUMTEXT.innerText = `Round ${round_num}`;
    });
  },
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})

export const ROUNDCOLLECT = new View({
  name: "Round Collect",
  id: "div-roundcollect",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})

export const ROUNDEND = new View({
  name: "Round End",
  id: "div-roundend",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})
