import { socket } from "../socket.js";
import { update } from "../state.js";

import { NAME, STATE, CODE } from "./model.js";
import * as View from "./view.js";

console.log(
  "%cStarting MusicBox! (Player)",
  "font-size: 18px font-weight: bold;"
);

View.initViews();

console.info("Finished initializing view");

update(STATE, "CONNECT");

socket.onOpen(() => {
  update(STATE, "JOIN");
});
socket.onClose(() => {
  update(STATE, "CONNECT");
});
socket.addMessageHandler("init", (message) => {
  update(STATE, "LOBBY");
  update(CODE, message.code);
});


function init_from_query_params (socket) {
  const urlParams = new URLSearchParams(window.location.search);
  const name = urlParams.get('name')
  const code = urlParams.get('code')
  if (name !== null && code !== null) {
    update(NAME, name)
    socket.send({
      type: "join",
      name: name,
      code: code,
    })
  }
}

socket.init("wss://backend.drexel-musicbox.com:8080")
.catch(socket => socket.init("ws://localhost:8080"))
.catch(() => console.error("Unable to conect to any websocket"))
.then(init_from_query_params)
