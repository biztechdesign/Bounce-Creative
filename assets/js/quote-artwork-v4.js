/* Local preview artwork persistence. Production quotes need stored attachment URLs. */
(function () {
  'use strict';
  function database() {
    return new Promise(function (resolve, reject) {
      var request = indexedDB.open('bounce-quote-artwork', 1);
      request.onupgradeneeded = function () { request.result.createObjectStore('artwork'); };
      request.onsuccess = function () { resolve(request.result); };
      request.onerror = function () { reject(request.error); };
    });
  }
  window.BounceQuoteArtwork = {
    save: async function (file) {
      var db = await database(), id = crypto.randomUUID();
      return new Promise(function (resolve, reject) {
        var tx = db.transaction('artwork', 'readwrite');
        tx.objectStore('artwork').put(file, id);
        tx.oncomplete = function () { db.close(); resolve({ id: id, name: file.name, type: file.type }); };
        tx.onerror = function () { db.close(); reject(tx.error); };
        tx.onabort = tx.onerror;
      });
    },
    load: async function (id) {
      var db = await database();
      return new Promise(function (resolve, reject) {
        var request = db.transaction('artwork').objectStore('artwork').get(id);
        request.onsuccess = function () { db.close(); resolve(request.result); };
        request.onerror = function () { db.close(); reject(request.error); };
      });
    }
  };
})();
