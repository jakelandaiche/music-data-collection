import { socket } from "../socket.js";
import { sleep } from "../utils.js";
import { bind, retrieve, update } from "../state.js";
import { STATE, STATE_DURATION, CODE, PLAYERS, ROUND_NUM, MATCHLIST } from "./model.js";

import { CONNECT } from "./views/connect.js"
import { LOBBY } from "./views/lobby.js"
import { GAMESTART } from "./views/gamestart.js"
import { GAMEEND } from "./views/gameend.js"
import { FAKEROUNDSTART, FAKEROUNDCOLLECT, FAKEROUNDEND, FAKEROUNDEND2 } from "./views/tutorial.js"
import { ROUNDSTART, ROUNDCOLLECT, ROUNDEND } from "./views/round.js"

import { renderPlayer, renderPlayers, reveal } from "./playerlist.js"

const stateViewMap = {
  CONNECT: CONNECT,
  LOBBY: LOBBY,
  GAMESTART: GAMESTART,
  GAMEEND: GAMEEND,

  ROUNDSTART: ROUNDSTART,
  ROUNDCOLLECT: ROUNDCOLLECT,
  ROUNDEND: ROUNDEND,

  FAKEROUNDSTART: FAKEROUNDSTART,
  FAKEROUNDCOLLECT: FAKEROUNDCOLLECT,
  FAKEROUNDEND: FAKEROUNDEND,
  FAKEROUNDEND2: FAKEROUNDEND2,
}

bind(STATE, (s) => {
  for (const [state, view] of Object.entries(stateViewMap)) {
    if (s == state) {
      view.show()
    } else {
      view.hide()
    }
  }
});

bind(STATE, async (s) => {
  if (s != "CONNECT") {
    document.getElementById("playerdiv").style.display = "flex";
  } else {
    document.getElementById("playerdiv").style.display = "none";
  }
  const players = retrieve(PLAYERS);
  if (s === "ROUNDEND") {
    for (let i = 0; i < players.length; i++) {
      await sleep(1000)
      const div = await renderPlayers(players, i+1);
      if (div !== null)
        await reveal(div);
    }
  } else if (s === "GAMEEND") {
    for (let i = 0; i < players.length; i++) {
      await sleep(1000)
      await renderPlayers(players, i+1);
    }
  } else {
    await renderPlayers(players)
  }

});

bind(PLAYERS, async (players) => {
  await renderPlayers(players);
});

export function initViews() {
  Object.values(stateViewMap).forEach(view => view.init())
}

export function initVideoPlayer() {
  socket.addMessageHandler("video", (message) => {
    play_video(message.id, message.start_time, message.start_time + 10);
  });
}
