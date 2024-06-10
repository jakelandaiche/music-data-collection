import { declare, update, bind, retrieve, reset } from "./state.js"
import { _data } from "./utils.js"

export function progressbar(name) {
  /* Create a state variable for the bar percentage */
  const PERCENTAGE = declare(0, `<Progress Bar ${name}>`)

  /* The filled part */
  const fg = document.createElement("div")
  /* The background part */
  const bg = document.createElement("div")

  /* Set up bg */
  bg.style.width = "100%"
  bg.classList.add('progressbar')
  bg.id = `progressbar-${name}`
  bg.appendChild(fg)
  bg[_data] = {
    percentage: PERCENTAGE,
    interval: null
  }

  /* Update fg's width whenever percentage changes */
  bind(PERCENTAGE, percentage => fg.style.width = `${Math.trunc(percentage)}%`)

  /* Return progress bar variable / DOM element */
  return [PERCENTAGE, bg]
}

export function progressbar_timer(bg, start, duration) {
  
  const length = duration*1000
  const end = start + length
  const PERCENTAGE = bg[_data].percentage

  const interval = setInterval(() => {
    const percentage = Math.trunc(100*(1 - ((Date.now() - start)/length)))
    update(PERCENTAGE, percentage, true)
    if (Date.now () >= end) clearInterval(interval)
  }, 33);

  clearInterval(bg[_data].interval)
  bg[_data].interval = interval
}
