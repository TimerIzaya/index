let db;
const openRequest = window.indexedDB.open('str_6848', 49)
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_2795', ['str_6170', 'str_7620']);
  index_1 = store_0.createIndex('str_6600', ['str_9112'], {'unique': false, 'multiEntry': false});
  index_2 = store_0.createIndex('str_9347', ['str_6790', 'str_5855']);
  index_3 = store_0.createIndex('str_7981', ['str_4273', 'str_7399', 'str_2675', 'str_4766']);
  index_4 = store_0.createIndex('str_519', ['str_2400', 'str_5072', 'str_872', 'str_9673']);
  index_5 = store_0.createIndex('str_5836', 'str_6943');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  store_1 = db.createObjectStore('store_1');
  index_0 = store_0.createIndex('str_5202', ['str_6430', 'str_5445', 'str_5049', 'str_2274', 'str_7031'], {'unique': true, 'multiEntry': false});
  store_1.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_7661', ['str_5017', 'str_400', 'str_1452', 'str_7827']);
  store_2 = db.createObjectStore('store_2');
  index_0 = store_0.createIndex('str_6961', ['str_3910', 'str_9337', 'str_4355'], {'unique': true, 'multiEntry': false});
  store_2.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_5380', 'str_6499', {'unique': true, 'multiEntry': true});
  store_1.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_1690', ['str_6993', 'str_2017', 'str_1230', 'str_4136'], {'unique': false, 'multiEntry': false});
  store_3 = db.createObjectStore('store_3');
  db.deleteObjectStore('store_1')
  db.deleteObjectStore('store_2')
  store_1 = db.createObjectStore('store_1');
  index_0 = store_0.createIndex('str_9692', 'str_6976');
  store_2 = db.createObjectStore('store_2');
  store_4 = db.createObjectStore('store_4');
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_0', 'readwrite')
  const store = txn.objectStore('store_0')
  const req_count_0 = store.count()
  const req_add_1 = store.add(42, 42)
  const req_get_2 = store.get(42)
  const req_clear_3 = store.clear()
  const req_put_4 = store.put(true, true)
  const req_get_5 = store.get(42)
  const req_put_6 = store.put(42, 'fallback')
  const req_put_7 = store.put('fallback', 'fallback')
  const req_add_8 = store.add(true)
  const req_getAllKeys_9 = store.getAllKeys(55)
  const req_getAllKeys_10 = store.getAllKeys('fallback')
  const req_put_11 = store.put('fallback')
  const req_get_12 = store.get('fallback')
  const req_get_13 = store.get('fallback')
  const req_openKeyCursor_14 = store.openKeyCursor(42)
  const req_put_15 = store.put(true, 'fallback')
  const req_getKey_16 = store.getKey(42)
  const req_delete_17 = store.delete('fallback')
  const req_getKey_18 = store.getKey(42)
  const req_count_19 = store.count('fallback')
  const req_count_20 = store.count('fallback')
  const req_count_21 = store.count(true)
  const req_put_22 = store.put(true)
  const req_getKey_23 = store.getKey(42)
  const req_get_24 = store.get(42)
  const req_getKey_25 = store.getKey(42)
  const req_count_26 = store.count()
  const req_delete_27 = store.delete('fallback')
  const req_getAll_28 = store.getAll(42, 79)
  const req_add_29 = store.add(true, 42)
  const req_getKey_30 = store.getKey('fallback')
  const req_getAllKeys_31 = store.getAllKeys(14)
  const req_delete_32 = store.delete(42)
  const req_getKey_33 = store.getKey(42)
  const req_getKey_34 = store.getKey(42)
  const req_put_35 = store.put('fallback')
  const req_openCursor_36 = store.openCursor('prev')
  const req_delete_37 = store.delete(true)
  const req_delete_38 = store.delete(true)
  const req_count_39 = store.count('fallback')
  const req_openKeyCursor_40 = store.openKeyCursor(true)
  const req_get_41 = store.get(42)
  const req_openCursor_42 = store.openCursor('prevunique')
  const req_put_43 = store.put(42, 42)
  const req_put_44 = store.put('fallback')
  const req_getAll_45 = store.getAll(true)
  const req_openKeyCursor_46 = store.openKeyCursor()
  const req_clear_47 = store.clear()
  const req_count_48 = store.count()
  const req_add_49 = store.add(42, true)
  const req_add_50 = store.add('fallback')
  const req_delete_51 = store.delete(42)
  const req_count_52 = store.count(42)
  const req_count_53 = store.count()
  const req_openCursor_54 = store.openCursor(42)
  const req_clear_55 = store.clear()
  const req_add_56 = store.add('fallback')
  const req_delete_57 = store.delete('fallback')
  const req_add_58 = store.add(42)
  const req_get_59 = store.get(true)
  const req_get_60 = store.get(true)
  const req_add_61 = store.add(42)
  const req_getAll_62 = store.getAll(78)
  const req_openKeyCursor_63 = store.openKeyCursor('fallback')
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
const deleteRequest = indexedDB.deleteDatabase('str_6848')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
