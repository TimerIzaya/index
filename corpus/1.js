let db;
const openRequest = window.indexedDB.open('str_463')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_7669', ['str_1691', 'str_20', 'str_9494']);
  index_1 = store_0.createIndex('str_6872', 'str_8907', {'unique': false, 'multiEntry': false});
  store_0.deleteIndex('index_1')
  index_1 = store_0.createIndex('str_5243', 'str_4852', {'unique': false, 'multiEntry': true});
  index_1.unique
  store_1 = db.createObjectStore('store_1');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_191', ['str_5294', 'str_1307', 'str_7585', 'str_6884'], {'unique': false, 'multiEntry': false});
  store_2 = db.createObjectStore('store_2');
  db.deleteObjectStore('store_2')
  db.deleteObjectStore('store_1')
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_9285', 'str_9625');
  index_1 = store_1.createIndex('str_6287', ['str_6143', 'str_7988', 'str_4783']);
  index_2 = store_0.createIndex('str_1402', 'str_2597', {'unique': false, 'multiEntry': false});
  index_3 = store_0.createIndex('str_7970', 'str_3560', {'unique': true, 'multiEntry': true});
  index_4 = store_0.createIndex('str_9005', 'str_6756');
  index_5 = store_2.createIndex('str_4601', ['str_9527'], {'unique': true, 'multiEntry': false});
  db.deleteObjectStore('store_0')
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  db.onversionchange = (event) => {
  console.log('The version of this database has changed, release this connection');
  db.close()
};
  db.onclose = (event) => {
  console.log('The database connection is unexpectedly closed');
};
};
openRequest.onblocked = (event) => {
  console.log('open db blocked triggered')
};
openRequest.onerror = (event) => {
  console.log('open db onerror triggered')
};
const deleteRequest = indexedDB.deleteDatabase('str_463')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
