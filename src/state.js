/**
 *   Basic reactive state
 *   @module
 */

/** Array that keeps track of *all* states */
const states = []
/** Keeps track of current value for each state */
const state = {}
/** Keeps track of initial values for each state */
const inits = {}
/** Keeps track of change handlers for each state */
const handlers = {}

/** 
 * Creates a new state variable with a given name and initial value */
export function declare(init, name) {
  const sym = name === undefined ? Symbol() : Symbol(name)
  inits[sym] = init
  state[sym] = init
  handlers[sym] = []
  states.push(sym)
  return sym
}

/** 
 * Updates a state variable's value, calling all bound handlers */
export function update(sym, value, quiet=false) {
  if (!quiet) {
    console.debug(`[STATE UPDATE] ${sym.description}: ${state[sym]} -> ${value}`)
  }
  state[sym] = value
  handlers[sym].forEach(h => h(value))
}

/** 
 * Gets the current value of a state variable */
export function retrieve(sym) {
  return state[sym]
}

/** 
 * Adds a new callback to a state variable's handler list */
export function bind(sym, handler) {
  handlers[sym].push(handler)
}

/** 
 * Resets a state variable to its original value */
export function reset(sym) {
  state[sym] = inits[sym]
  handlers[sym].forEach(h => h(inits[sym]))
}

/**
 * Allows for binding to multiple states at once.
 * Handler arguments have to be in the same order as symbol list
 */
export function bindmultiple(syms, handler) {
  syms.forEach(sym => bind(sym, () => handler(...syms.map(retrieve))))
}

/**
 * Creates a state with a value derived from another state
 * (DO NOT modify this state manually)
 */
export function derived(sym, f, name) {
  const s = declare(f(sym), name ?? sym.toString()) 
  bind(sym, v => update(s, f(v)))
  return s
}

/*
 * Sets state B to update to A's value whenever A updates
 */
export function mirror(a, b) {
  bind(a, val => update(b, val))
}

/**
 * Convenience function 
 */
export function elembind(sym, elem, f) {
  bind(sym, val => f(val, elem))
}

/**
 * Prints every state variable at once to the console
 */
export function statedump() {
  console.group(
    "%cSTATE DUMP:",
    "font-size: 18px font-weight: bold;"
  )
  states.forEach(sym => console.log(`${sym.description}: ${retrieve(sym)}`))
  console.groupEnd()
}


