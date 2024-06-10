import { retrieve } from "../state.js"
import { sleep } from "../utils.js"

import { STATE, MATCHLIST } from "./model.js";

function getRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

const colors = [];
for (let x = 0; x < 100; x++) {
  colors.push(getRandomColor());
}

const playerlist = document.getElementById("playerlist");

export async function renderPlayer(player) {
  const div = document.createElement("div");
  playerlist.appendChild(div)
  div.classList.add("playercard");
  div.style.display = "flex";
  div.style.flexDirection = "column";
  div.style.justifyContent = "flex-start";
  div.style.alignItems = "center";
  div.style.border = `10px solid ${player.color}`;
  div.style.grid = "50%";

  const state = retrieve(STATE);
  const matchlist = retrieve(MATCHLIST)

  const entry = document.createElement("p");
  entry.innerText = player.name;
  entry.style.fontSize = "18pt";
  entry.style.fontWeight = "bold";
  entry.innerText += player.connected ? "" : " 🔌";

  const score = document.createElement("p");
  score.classList.add("score");
  score.style.fontSize = "22pt";
  score.innerText = Math.round(player.score);

  const answerDiv = document.createElement("div");

  div.appendChild(entry);
  switch (state) {
    case "LOBBY":
      entry.innerText += player.ready ? " ✅" : "";
      break;
    case "GAMESTART":
      entry.innerText += ` [${Math.round(player.total)}]`;
      break;
    case "FAKEROUNDEND":
      {
        const fullanswer = document.createElement("p");
        console.log(player.answer);
        const raw_answer = player.answer !== null ? player.answer : "";
        fullanswer.innerHTML = raw_answer
        console.log(fullanswer.innerHTML);
        div.appendChild(fullanswer);
        div.appendChild(score);
        div.style.justifyContent = "space-between";
      }
      break;
    case "FAKEROUNDSTART":
    case "ROUNDSTART":
      entry.innerText += ` [${Math.round(player.total)}]`;
      div.style.justifyContent = "space-between";
      break;
    case "FAKEROUNDCOLLECT":
    case "ROUNDCOLLECT":
      entry.innerText += ` [${Math.round(player.total)}]`;
      const hiddenanswer = document.createElement("p");
      hiddenanswer.innerText =
        player.answer !== null ? "* ".repeat(player.answer.length) : "";
      answerDiv.appendChild(hiddenanswer);
      div.appendChild(answerDiv);
      break;
    case "FAKEROUNDEND2":
    case "ROUNDEND":
      entry.innerText += ` [${Math.round(player.total)}]`;
      if (player.score_info === null) break;
      const fullanswer = document.createElement("p");
      const raw_answer = player.answer !== null ? player.answer : "";
      fullanswer.innerHTML = raw_answer
        .replace(/[a-zA-Z]+/g, word => {
          const idx = matchlist.indexOf(word.toLowerCase())
          return idx === -1 ?
            word : `<span style="color: ${colors[idx]};">${word}</span>` 
        })
      const breakdown = document.createElement("div");
      breakdown.classList.add("breakdown");

      const sim = document.createElement("div");
      const matches = document.createElement("div");
      const bonus = document.createElement("div");
      sim.classList.add("sim");
      matches.classList.add("matches");
      bonus.classList.add("bonus");

      sim.textContent = "Semantic Similarity: " + player.score_info.similarity;
      matches.textContent = "Matches: " + player.score_info.matches;
      bonus.textContent = "Multiplier from matches: " + player.score_info.bonus;

      div.appendChild(fullanswer);
      div.appendChild(breakdown);
      div.style.justifyContent = "space-between";

      breakdown.style.fontSize = "small";
      breakdown.appendChild(sim);
      breakdown.appendChild(matches);
      breakdown.appendChild(bonus);
      div.appendChild(score);
      break;
    case "GAMEEND":
      entry.innerText += ` [${Math.round(player.total)}]`;
      const stats = document.createElement("ul");
      stats.classList.add("stats")
      const len = document.createElement("li");
      stats.classList.add("len")
      const uniq = document.createElement("li");
      stats.classList.add("uniq")

      len.textContent = "Average word length: " + Math.floor(parseInt(player.avg_len));
      uniq.textContent = "Unique words written: " + parseInt(player.unique_words);

      stats.appendChild(len);
      stats.appendChild(uniq);
      div.appendChild(stats);
      break;
  }

  return div;
}

export async function reveal(div) {
  const sim = div.querySelector(".sim")
  const matches = div.querySelector(".matches")
  const bonus = div.querySelector(".bonus")
  const score = div.querySelector(".score")

  sim.style.visibility = "hidden"
  matches.style.visibility = "hidden"
  bonus.style.visibility = "hidden"
  score.style.visibility = "hidden"

  await sleep(1000)
  sim.style.visibility = "visible"
  await sleep(1000)
  matches.style.visibility = "visible"
  await sleep(1000)
  bonus.style.visibility = "visible"
  await sleep(1000)
  score.style.visibility = "visible"
}

export async function renderPlayers(players, n) {
  // Clear player list div
  while (playerlist.hasChildNodes())
    playerlist.removeChild(playerlist.firstChild);

  players.sort(roundSort);
  let lastDiv = null;

  if (n === undefined) 
    n = players.length

  for (let i = 0; i < n; i++) {
    const div = await renderPlayer(players[i])
    lastDiv = div
  }

  for (let i = 0; i < 8 - n; i++) {
    const div = document.createElement("div");
    div.classList.add("emptycard");
    div.style.grid = "50%";
    playerlist.appendChild(div);
  }
  return lastDiv
}

function roundSort(a, b) {
  if (a.score > b.score) {
    return 1;
  } else if (a.score < b.score) {
    return -1;
  } else {
    return 0;
  }
}

