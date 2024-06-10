import { getelem } from "../../utils.js"
import { socket } from "../../socket.js"
import { View } from "../../view.js"

const CONNECTFORM = getelem("connectform")

export const CONNECT = new View({
  name: "Connection Form",
  id: "div-connect",
  init: function() {
    CONNECTFORM.addEventListener("submit", (event) => {
      event.preventDefault(); // prevent browser from reloading (default behavior)

      // init socket
      const formData = new FormData(connectform);
      const ws_host = formData.get("ws-host");
      socket.init(ws_host);
    });
  },
  reset: function() {
    const hostinput = document.getElementById("connectform-hostinput");
    hostinput.innerText = "wss://backend.drexel-musicbox.com:8080";
  }
})

