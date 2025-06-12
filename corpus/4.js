let db;
const openRequest = window.indexedDB.open('str_4894')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_7428', 'str_6641');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_7031', 'str_4341');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0.indexNames
  store_0.indexNames
  store_0.name
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
const deleteRequest = indexedDB.deleteDatabase('str_4894')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
