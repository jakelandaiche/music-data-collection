/**
 * Wrapper around WebSocket that can hold
 * multiple persistent handlers and also
 * preprocesses messages sent and received
 */
class MusicBoxSocket {

  constructor() {
    this.socket = null;

    this.onopen = [];
    this.onclose = [];
    this.message_handlers = {};
  }

  // Init
  init(ws_host) {
    // initialize socket
    if (this.socket !== null && this.socket.readyState !== 3) return;

    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(ws_host);
      console.info(`Attempting to connect to ${ws_host}`)

      // Open and Close handlers 
      this.socket.addEventListener("open", (event) => {
        resolve(this);

        console.info(`Connected to ${ws_host} successfully`)
        this.onopen.forEach(_ => _(event))
      });

      this.socket.addEventListener("error", (event) => {
        console.error("WebSocket error: ", event);
      });

      // Message handler
      this.socket.addEventListener("message", (event) => {
        console.group("Received WebSocket Message")
        console.log("Raw:", event.data);

        // Try to parse data
        let data;
        try {
          data = JSON.parse(event.data);
          console.log("Parsed:", data);
        } catch (error) {
          console.error("Unable to parse message:", error)
        }

        // Check if message has type
        if ("type" in data) {
          console.log("Type:", data.type);

          // Run handler if message type has a handler
          if (data.type in this.message_handlers) {
            console.log("Executing handler...");
            console.group("Handler logs");
            this.message_handlers[data.type](data);
            console.groupEnd();
          }

        } else {
          console.error("Message has no type");
        }

        // Done
        console.groupEnd();
      });

      this.socket.addEventListener("close", (event) => {
        console.info(`Connection to ${ws_host} closed. Reason:` , event.reason);
        this.onclose.forEach(f => f(event))

        // Null socket when closed
        this.socket = null;

        // Reject promise;
        reject(this);
      });

    });
  }

  onOpen(handler) {
    this.onopen.push(handler)
  }

  onClose(handler) {
    this.onclose.push(handler)
  }

  send(data) {
    if (this.socket === null || this.socket.readyState != 1) return;
    
    console.group("Sent WebSocket Message")
    console.log("Payload", data)
    this.socket.send(JSON.stringify(data))
    console.groupEnd()
  }

  addMessageHandler(type, handler) {
    this.message_handlers[type] = handler;
  }

}

// Global socket
export const socket = new MusicBoxSocket();
