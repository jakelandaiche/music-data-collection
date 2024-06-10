import { getelem } from "../../utils.js"
import { socket } from "../../socket.js"
import { View } from "../../view.js"

const RESTARTBTN = document.getElementById("gameend-restartbtn");

export const GAMEEND = new View({
  name: "Game End",
  id: "div-gameend",
  init: function() {
    RESTARTBTN.addEventListener("click", (event) => {
      socket.send({
        type: "restart",
      });
    });
  }
})

