const request = indexedDB.open("example_string", 1);
request.onsuccess = function(event) {
  const db = event.target.result;
  const tx = db.transaction(["store1"], "readwrite");
  tx.objectStore("store1").put("any_value");
  tx.objectStore("store1").get("any_value");
};