import { View } from "../../view.js"

import { PROGRESSBAR } from "../bar.js"

export const GAMESTART = new View({
  name: "Game Start",
  id: "div-gamestart",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})
