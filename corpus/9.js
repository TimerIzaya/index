let db;
const openRequest = window.indexedDB.open('str_4124')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_489', ['str_4266', 'str_8111', 'str_9981', 'str_6002', 'str_5235'], {'unique': false, 'multiEntry': false});
  store_0.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_8167', 'str_256', {'unique': false, 'multiEntry': false});
  store_1 = db.createObjectStore('store_1');
  store_0.autoIncrement
  index_0 = store_0.createIndex('str_9599', ['str_5271'], {'unique': true, 'multiEntry': false});
  store_1.deleteIndex('index_0')
  index_0 = store_1.createIndex('str_4568', 'str_899');
  store_1.autoIncrement
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_1.createIndex('str_6279', ['str_2680', 'str_897', 'str_4987']);
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  store_2 = db.createObjectStore('store_2');
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  db.deleteObjectStore('store_1')
  store_1.autoIncrement
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_2', 'readwrite')
  const store = txn.objectStore('store_2')
  txn.oncomplete = (event) => {
  console.log('Transaction completed successfully');
};
  txn.onabort = (event) => {
  console.log('Transaction was aborted');
};
  txn.onerror = (event) => {
  console.log('Transaction error occurred');
};
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
const deleteRequest = indexedDB.deleteDatabase('str_4124')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
