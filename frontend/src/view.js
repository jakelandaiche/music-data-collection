/**
 */

export class View {

  _init() {}
  _reset() {}
  _enter() {}
  _exit() {}

  constructor ({
    name,
    id,
    init, 
    reset, 
    enter,
    exit 
  }) {
    this.name = name
    this.id = id
    this.div = null

    this._init = init ?? this._init
    this._reset = reset ?? this._reset
    this._enter = enter ?? this._enter
    this._exit = exit ?? this._exit
  }

  init() {
    console.group(`Initializing `, this.name)
    const div = document.getElementById(this.id)
    if (div == null) {
      console.error(`Unable to find div for view "${this.name}"!`)
    } else {
      this.div = div
      this._init()
    }
    console.groupEnd()
  }

  reset() {
    if (this.div == null) {
      console.error (`Attempted to reset view "${this.name}" which has no div!`)
    } else {
      console.log(`Resetting view ${this.name}`)
      this._reset()
    }
  }

  show() {
    if (this.div == null) {
      console.error (`Attempted to show view "${this.name}" which has no div!`)
    } else {
      this.div.style.display = "block"
      this._enter()
    }
  }

  hide() {
    if (this.div == null) {
      console.error (`Attempted to show view "${this.name}" which has no div!`)
    } else {
      this.div.style.display = "none"
      this._exit()
    }
  }
}

