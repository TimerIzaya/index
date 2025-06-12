let db;
const openRequest = window.indexedDB.open('str_4329')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_8786', 'str_4594', {'unique': true, 'multiEntry': true});
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_1742', 'str_7853', {'unique': true, 'multiEntry': true});
  index_1 = store_0.createIndex('str_9788', ['str_3259'], {'unique': false, 'multiEntry': false});
  index_2 = store_0.createIndex('str_7325', ['str_5989', 'str_9745', 'str_807', 'str_2913']);
  index_3 = store_0.createIndex('str_7413', ['str_3110', 'str_1928'], {'unique': false, 'multiEntry': false});
  index_4 = store_0.createIndex('str_5110', ['str_3075', 'str_6582'], {'unique': true, 'multiEntry': false});
  store_1 = db.createObjectStore('store_1');
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  index_0 = store_0.createIndex('str_9014', 'str_388', {'unique': true, 'multiEntry': true});
  store_0.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_2313', ['str_2940', 'str_6700', 'str_9825', 'str_8212'], {'unique': false, 'multiEntry': false});
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  store_2 = db.createObjectStore('store_2');
  store_0.keyPath
  index_0 = store_1.createIndex('str_9022', ['str_2099', 'str_6052'], {'unique': true, 'multiEntry': false});
  index_0.keyPath
  db.deleteObjectStore('store_2')
  store_2 = db.createObjectStore('store_2');
  db.deleteObjectStore('store_1')
  index_0.keyPath
  db.deleteObjectStore('store_2')
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_5419', ['str_8357', 'str_9880', 'str_7876', 'str_9359', 'str_1263']);
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_0', 'readwrite')
  const store = txn.objectStore('store_0')
  const req_get_0 = store.get(42)
  const req_getAllKeys_1 = store.getAllKeys('fallback')
  const req_getAllKeys_2 = store.getAllKeys(1)
  const req_getAllKeys_3 = store.getAllKeys('fallback', 68)
  const req_getAllKeys_4 = store.getAllKeys(42)
  const req_delete_5 = store.delete(42)
  const req_getAllKeys_6 = store.getAllKeys(true, 76)
  const req_getAllKeys_7 = store.getAllKeys(42)
  const req_openKeyCursor_8 = store.openKeyCursor()
  const req_getAllKeys_9 = store.getAllKeys()
  const req_count_10 = store.count(true)
  const req_openKeyCursor_11 = store.openKeyCursor()
  const req_put_12 = store.put(true, 42)
  const req_get_13 = store.get(true)
  const req_getAll_14 = store.getAll()
  const req_openCursor_15 = store.openCursor(None, 'nextunique')
  const req_get_16 = store.get('fallback')
  const req_count_17 = store.count()
  const req_count_18 = store.count('fallback')
  const req_count_19 = store.count()
  const req_put_20 = store.put(42, true)
  const req_delete_21 = store.delete('fallback')
  const req_clear_22 = store.clear()
  const req_add_23 = store.add(true)
  const req_put_24 = store.put(42)
  const req_getKey_25 = store.getKey(42)
  const req_getAllKeys_26 = store.getAllKeys('fallback')
  const req_clear_27 = store.clear()
  const req_put_28 = store.put('fallback', 'fallback')
  const req_get_29 = store.get(42)
  const req_count_30 = store.count(true)
  const req_getAllKeys_31 = store.getAllKeys()
  const req_openKeyCursor_32 = store.openKeyCursor(None, 'nextunique')
  const req_openKeyCursor_33 = store.openKeyCursor()
  const req_get_34 = store.get('fallback')
  const req_add_35 = store.add(42)
  const req_getKey_36 = store.getKey(true)
  const req_getKey_37 = store.getKey(42)
  const req_add_38 = store.add(42)
  const req_get_39 = store.get(true)
  const req_openCursor_40 = store.openCursor('fallback', 'next')
  const req_openCursor_41 = store.openCursor(None, 'prevunique')
  const req_put_42 = store.put('fallback')
  const req_getAllKeys_43 = store.getAllKeys(true)
  const req_openCursor_44 = store.openCursor(42)
  const req_getKey_45 = store.getKey(42)
  const req_getAllKeys_46 = store.getAllKeys()
  const req_getAllKeys_47 = store.getAllKeys()
  const req_openCursor_48 = store.openCursor()
  const req_count_49 = store.count('fallback')
  const req_clear_50 = store.clear()
  const req_add_51 = store.add(42)
  const req_add_52 = store.add('fallback')
  const req_delete_53 = store.delete('fallback')
  const req_count_54 = store.count(42)
  const req_openKeyCursor_55 = store.openKeyCursor()
  const req_clear_56 = store.clear()
  const req_count_57 = store.count()
  const req_openKeyCursor_58 = store.openKeyCursor()
  const req_openKeyCursor_59 = store.openKeyCursor('prevunique')
  const req_openKeyCursor_60 = store.openKeyCursor(42)
  const req_getAll_61 = store.getAll()
  const req_clear_62 = store.clear()
  const req_get_63 = store.get('fallback')
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
const deleteRequest = indexedDB.deleteDatabase('str_4329')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
