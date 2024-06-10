import { View } from "../../view.js"

import { PROGRESSBAR } from "../bar.js"

export const FAKEROUNDSTART = new View({
  name: "Fake Round Start",
  id: "div-fakeroundstart",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})

export const FAKEROUNDCOLLECT = new View({
  name: "Fake Round Collect",
  id: "div-fakeroundcollect",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})

export const FAKEROUNDEND = new View({
  name: "Fake Round End",
  id: "div-fakeroundend",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})

export const FAKEROUNDEND2 = new View({
  name: "Fake Round End2",
  id: "div-fakeroundend2",
  enter: function () {
    this.div.appendChild(PROGRESSBAR)
  },
})
