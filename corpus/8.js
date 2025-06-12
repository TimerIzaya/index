let db;
const openRequest = window.indexedDB.open('str_2620')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_9221', ['str_4163', 'str_1494'], {'unique': true, 'multiEntry': false});
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_3678', ['str_7627', 'str_6424', 'str_8212']);
  store_0.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_1640', 'str_4960');
  index_1 = store_0.createIndex('str_615', 'str_4888');
  db.deleteObjectStore('store_0')
  index_1.name
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
const deleteRequest = indexedDB.deleteDatabase('str_2620')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
