let db;
const openRequest = window.indexedDB.open('str_5503')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_3203', 'str_2897', {'unique': true, 'multiEntry': false});
  store_0.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_8718', 'str_5517');
  index_1 = store_0.createIndex('str_6596', ['str_9134', 'str_882'], {'unique': true, 'multiEntry': false});
  index_2 = store_0.createIndex('str_5170', ['str_7906', 'str_1273', 'str_9155', 'str_3912']);
  index_3 = store_0.createIndex('str_3470', ['str_7847', 'str_9272', 'str_4890', 'str_9961']);
  index_4 = store_0.createIndex('str_7710', ['str_4284', 'str_4648', 'str_243'], {'unique': false, 'multiEntry': false});
  store_1 = db.createObjectStore('store_1');
  index_1.multiEntry
  index_3.unique
  index_0 = store_1.createIndex('str_1584', ['str_3851', 'str_7454', 'str_7086', 'str_5022'], {'unique': true, 'multiEntry': false});
  index_1 = store_1.createIndex('str_5716', ['str_782', 'str_6266', 'str_4447', 'str_9505']);
  store_1.deleteIndex('index_1')
  index_1 = store_1.createIndex('str_6181', ['str_6953'], {'unique': true, 'multiEntry': false});
  store_0.deleteIndex('index_0')
  index_0 = store_1.createIndex('str_7536', 'str_6927');
  store_1.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_7640', 'str_9975');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  store_0.name
  db.deleteObjectStore('store_0')
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_1', 'readwrite')
  const store = txn.objectStore('store_1')
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
const deleteRequest = indexedDB.deleteDatabase('str_5503')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
