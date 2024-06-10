import { socket } from "../socket.js"
import { update, bind, retrieve } from "../state.js"
import { STATE, NAME, COLOR, READY } from "./model.js"


export const stateViews = {
  CONNECT: {
    div: "div-connect",
    init: () => {
      const connectform = document.getElementById("connectform")
      connectform.addEventListener("submit", (event) => {
        event.preventDefault() // prevent browser from reloading (default behavior)

        // init socket
        const formData = new FormData(connectform)
        const ws_host = formData.get("ws-host")
        socket.init(ws_host)
      })
    },
    reset: () => {},
  },

  JOIN: {
    div: "div-join",
    init: () => {
      const joinform = document.getElementById("joinform")

      joinform.addEventListener("submit", (event) => {
        event.preventDefault() // prevent browser from reloading (default behavior)

        // init socket
        const formData = new FormData(joinform)
        const name = formData.get("name")
        const code = formData.get("code")

        update(NAME, name)
        socket.send({
          type: "join",
          name: name,
          code: code,
        })
      })
    },
    reset: () => {
      const codeinput = document.getElementById("join-codeinput")
      const nameinput = document.getElementById("join-nameinput")

      codeinput.value = ""
      nameinput.value = ""
    },
  },

  LOBBY: {
    div: "div-lobby",
    init: () => {
      const nametext = document.getElementById("lobby-nametext")
      const colorinput = document.getElementById("lobby-colorinput")
      const readyinput = document.getElementById("lobby-readyinput")

      colorinput.addEventListener("change", (event) => {
        update(COLOR, colorinput.value)
      })
      readyinput.addEventListener("change", (event) => {
        update(READY, readyinput.checked)
      })

      bind(NAME, (n) => {
        nametext.innerText = n
      })
    },
    reset: () => {
      const nametext = document.getElementById("lobby-nametext")
      const colorinput = document.getElementById("lobby-colorinput")
      const readyinput = document.getElementById("lobby-readyinput")

      nametext.innerText = ""
      colorinput.value = "#000000"
      readyinput.checked = false
    },
  },

  GAMESTART: {
    div: "div-gamestart",
    init: () => {},
    reset: () => {},
  },

  FAKEROUNDSTART: {
    div: "div-gamestart",
    init: () => {},
    reset: () => {},
  },
  FAKEROUNDCOLLECT: {
    div: "div-gamestart",
    init: () => {},
    reset: () => {},
  },
  FAKEROUNDEND: {
    div: "div-gamestart",
    init: () => {},
    reset: () => {},
  },
  FAKEROUNDEND2: {
    div: "div-gamestart",
    init: () => {},
    reset: () => {},
  },


  ROUNDSTART: {
    div: "div-roundstart",
    init: () => {},
    reset: () => {},
  },

  ROUNDCOLLECT: {
    div: "div-roundstart",
    init: () => {
      const answerform = document.getElementById("answerform")
      const answerinput = document.getElementById("answerinput")
      const postsubmit = document.getElementById("roundcollect-postsubmit")

      answerform.addEventListener("submit", (event) => {
        event.preventDefault() // prevent browser from reloading (default behavior)

        const formData = new FormData(answerform)
        const answer = formData.get("answer")

        socket.send({
          type: "answer",
          name: retrieve(NAME),
          answer: answer,
        })

        answerform.style.display = "none"
        postsubmit.style.display = "block"
      })
    },
    reset: () => {
      const answerform = document.getElementById("answerform")
      const answerinput = document.getElementById("answerinput")
      const postsubmit = document.getElementById("roundcollect-postsubmit")

      answerform.style.display = "block"
      postsubmit.style.display = "none"
      answerinput.value = ""
    },
  },

  ROUNDEND: {
    div: "div-roundend",
    init: () => {},
    reset: () => {},
  },

  GAMEEND: {
    div: "div-gameend",
    init: () => {},
    reset: () => {},
  },
}

const divs = {
  CONNECT: "div-connect",
  JOIN: "div-join",
  LOBBY: "div-lobby",
  GAMESTART: "div-gamestart",
  ROUNDSTART: "div-roundstart",
  ROUNDCOLLECT: "div-roundcollect",
  ROUNDEND: "div-roundend",
  GAMEEND: "div-gameend",
}

bind(STATE, (s) => {
  Object.keys(stateViews)
    .filter((k) => k != s)
    .forEach((k) => {
      document.getElementById(stateViews[k].div).style.display = "none"
    })
  Object.keys(stateViews)
    .filter((k) => k != s)
    .forEach((k) => stateViews[k].reset())
  document.getElementById(stateViews[s].div).style.display = "block"

  document.getElementById("answersubmit").disabled = (s === "ROUNDSTART")

  if (s === "ROUNDCOLLECT") {
    setTimeout(() => {
      const answerform = document.getElementById("answerform")
      const formData = new FormData(answerform)
      const answer = formData.get("answer")
      socket.send({
        type: "answer",
        name: retrieve(NAME),
        answer: answer,
      })
    }, 29000)
  }
})

export function initViews() {
  Object.keys(stateViews).forEach((k) => stateViews[k].init())
}
