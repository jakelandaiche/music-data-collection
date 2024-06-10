import { getelem } from "../../utils.js"
import { socket } from "../../socket.js"
import { View } from "../../view.js"
import { bind, update } from "../../state.js"

import { CODE, PLAYERS } from "../model.js"

export const CODETEXT = getelem("lobby-codetext")
export const STARTBTN = getelem("lobby-startbtn")
export const DATASETSELECT = getelem("lobby-datasetselect")
export const NROUNDSINPUT = getelem("lobby-nroundsinput")
export const TUTORIALINPUT = getelem("lobby-tutorialinput")

export const LOBBY = new View({
  name: "Lobby",
  id: "div-lobby",
  init: function() {
    DATASETSELECT.addEventListener("change", (event) => {
      socket.send({
        type: "dataset",
        dataset: event.target.value,
      });
    });

    NROUNDSINPUT.addEventListener("change", (event) => {
      socket.send({
        type: "nrounds",
        nrounds: event.target.value,
      });
    });

    STARTBTN.addEventListener("click", (event) => {
      socket.send({
        type: "start",
        tutorial: TUTORIALINPUT.checked
      });
    });
    bind(CODE, (c) => {
      CODETEXT.innerText = c;
    });
    bind(PLAYERS, (players) => {
      // startbtn.disabled = players.length < 3
    });
    update(PLAYERS, []);
  },
  exit: function() {
    const nroundsinput = document.getElementById("lobby-nroundsinput");
    nroundsinput.value = "5";
  },
})
