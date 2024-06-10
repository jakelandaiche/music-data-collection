import { socket } from "../socket.js";
import { update, statedump } from "../state.js";

import { STATE, CODE } from "./model.js";
import * as View from "./view.js";

console.log("%cStarting MusicBox!", "font-size: 18px font-weight: bold;");

View.initVideoPlayer();
View.initViews();

console.info("Finished initializing view");

// Let's go !
update(STATE, "CONNECT");

socket.onOpen(() => {
  socket.send({
    type: "init",
  });
});

socket.init("wss://backend.drexel-musicbox.com:8080")
.catch(socket => socket.init("ws://localhost:8080"))
.catch(() => console.error("Unable to conect to any websocket"));

const urlParams = new URLSearchParams(window.location.search);
const myParam = urlParams.get('myParam');
console.log("myParam", myParam)

