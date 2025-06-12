let db;
const openRequest = window.indexedDB.open('str_289', 39)
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_9801', 'str_55', {'unique': false, 'multiEntry': true});
  index_1 = store_0.createIndex('str_9886', ['str_5551', 'str_3255', 'str_2930'], {'unique': true, 'multiEntry': false});
  index_2 = store_0.createIndex('str_3554', ['str_7390'], {'unique': false, 'multiEntry': false});
  index_3 = store_0.createIndex('str_3426', 'str_3047');
  index_4 = store_0.createIndex('str_1146', 'str_2143');
  index_5 = store_0.createIndex('str_6217', ['str_4961', 'str_3321', 'str_2539', 'str_1093']);
  index_0.name
  index_6 = store_0.createIndex('str_1156', ['str_6266', 'str_5085', 'str_2376', 'str_2880']);
  index_7 = store_0.createIndex('str_9172', 'str_1914', {'unique': true, 'multiEntry': false});
  index_8 = store_0.createIndex('str_7593', 'str_7151');
  index_9 = store_0.createIndex('str_3729', ['str_156', 'str_403', 'str_7444', 'str_2666'], {'unique': false, 'multiEntry': false});
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  store_0.autoIncrement
  index_0 = store_0.createIndex('str_6204', ['str_8784', 'str_828', 'str_2133', 'str_2522'], {'unique': true, 'multiEntry': false});
  index_1 = store_0.createIndex('str_6498', ['str_7597'], {'unique': false, 'multiEntry': false});
  index_2 = store_0.createIndex('str_8923', ['str_481', 'str_1636', 'str_5092', 'str_220', 'str_2674']);
  index_3 = store_0.createIndex('str_3217', 'str_136', {'unique': true, 'multiEntry': true});
  index_4 = store_0.createIndex('str_1574', ['str_6444']);
  store_0.indexNames
  store_0.name
  index_4.multiEntry
  store_0.autoIncrement
  index_5 = store_0.createIndex('str_8150', 'str_3317', {'unique': true, 'multiEntry': false});
  index_6 = store_0.createIndex('str_9867', 'str_1719');
  index_7 = store_0.createIndex('str_1268', 'str_8217', {'unique': true, 'multiEntry': false});
  db.deleteObjectStore('store_0')
  store_0.keyPath
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
const deleteRequest = indexedDB.deleteDatabase('str_289')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
