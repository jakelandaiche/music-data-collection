import { bind } from "../state.js"
import { progressbar, progressbar_timer } from "../progressbar.js"

import { STATE_DURATION } from "./model.js"

export const [PERCENTAGE, PROGRESSBAR] = progressbar("mainbar")
bind(STATE_DURATION, duration => progressbar_timer(PERCENTAGE, Date.now(), duration))
