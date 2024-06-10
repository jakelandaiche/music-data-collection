/**
 *   Helper functions
 *   @module
 */

export const _data = Symbol("DOM Element Data")
export const getelem = id => document.getElementById(id)
export const sleep = (ms = 0) => new Promise(resolve => setTimeout(resolve, ms))

export function debounce(callback, delay=1000) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      callback(...args);
    }, delay);
  };
}

export function throttle(callback, delay=1000) {
  let wait = false;

  return (...args) => {
    if (wait) return;

    callback(...args);
    wait = true;

    setTimeout(() => {
      wait = false;
    }, delay);
  };
}
