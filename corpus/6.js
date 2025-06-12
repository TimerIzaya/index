let db;
const openRequest = window.indexedDB.open('str_7976')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_3745', ['str_3980', 'str_8182', 'str_202', 'str_1779'], {'unique': false, 'multiEntry': false});
  store_1 = db.createObjectStore('store_1');
  index_0 = store_1.createIndex('str_2634', ['str_364', 'str_3533', 'str_4135', 'str_2557']);
  index_1 = store_1.createIndex('str_8287', ['str_8358']);
  index_2 = store_0.createIndex('str_305', ['str_5', 'str_2458', 'str_6809', 'str_799']);
  store_1.deleteIndex('index_2')
  index_2 = store_0.createIndex('str_6828', ['str_166', 'str_2639']);
  store_1.keyPath
  db.deleteObjectStore('store_0')
  index_3 = store_0.createIndex('str_9107', ['str_9933', 'str_1813']);
  db.deleteObjectStore('store_1')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_778', ['str_474', 'str_9709', 'str_2664']);
  index_3.unique
  store_1.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_7290', ['str_3032'], {'unique': true, 'multiEntry': false});
  store_0.deleteIndex('index_0')
  index_0 = store_1.createIndex('str_7591', 'str_7133');
  index_1 = store_0.createIndex('str_2210', ['str_4547', 'str_6703', 'str_8550', 'str_6872']);
  index_2 = store_1.createIndex('str_6803', ['str_8132', 'str_2123', 'str_3792']);
  index_3 = store_1.createIndex('str_9344', 'str_5835', {'unique': false, 'multiEntry': false});
  index_4 = store_0.createIndex('str_3250', 'str_9477', {'unique': true, 'multiEntry': true});
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_1.createIndex('str_1000', 'str_5109');
  index_1 = store_0.createIndex('str_1682', 'str_7372', {'unique': false, 'multiEntry': true});
  index_2 = store_1.createIndex('str_6122', ['str_1709', 'str_4285', 'str_5217'], {'unique': true, 'multiEntry': false});
  index_3 = store_0.createIndex('str_6592', 'str_3648', {'unique': true, 'multiEntry': false});
  index_4 = store_0.createIndex('str_7151', ['str_3566', 'str_1404', 'str_9846', 'str_9300']);
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_0', 'readwrite')
  const store = txn.objectStore('store_0')
  const req_getAllKeys_0 = store.getAllKeys()
  const req_getAllKeys_1 = store.getAllKeys()
  const req_openKeyCursor_2 = store.openKeyCursor('prev')
  const req_put_3 = store.put(42)
  const req_delete_4 = store.delete('fallback')
  const req_delete_5 = store.delete('fallback')
  const req_delete_6 = store.delete(true)
  const req_openKeyCursor_7 = store.openKeyCursor()
  const req_get_8 = store.get('fallback')
  const req_getKey_9 = store.getKey('fallback')
  const req_getKey_10 = store.getKey(true)
  const req_getKey_11 = store.getKey('fallback')
  const req_add_12 = store.add(true, 42)
  const req_getAllKeys_13 = store.getAllKeys(true)
  const req_getAllKeys_14 = store.getAllKeys()
  const req_add_15 = store.add(42, 42)
  const req_openKeyCursor_16 = store.openKeyCursor(None)
  const req_put_17 = store.put(true)
  const req_get_18 = store.get(42)
  const req_put_19 = store.put(42)
  const req_put_20 = store.put(true)
  const req_delete_21 = store.delete('fallback')
  const req_getKey_22 = store.getKey('fallback')
  const req_clear_23 = store.clear()
  const req_getKey_24 = store.getKey(true)
  const req_clear_25 = store.clear()
  const req_put_26 = store.put('fallback', 42)
  const req_put_27 = store.put(true)
  const req_put_28 = store.put('fallback', true)
  const req_get_29 = store.get(42)
  const req_getAll_30 = store.getAll('fallback')
  const req_delete_31 = store.delete('fallback')
  const req_delete_32 = store.delete('fallback')
  const req_add_33 = store.add(true)
  const req_openKeyCursor_34 = store.openKeyCursor('prev')
  const req_put_35 = store.put(42, 42)
  const req_openCursor_36 = store.openCursor('next')
  const req_get_37 = store.get(true)
  const req_getAll_38 = store.getAll()
  const req_getAll_39 = store.getAll()
  const req_getKey_40 = store.getKey(true)
  const req_getAllKeys_41 = store.getAllKeys()
  const req_put_42 = store.put('fallback')
  const req_delete_43 = store.delete(42)
  const req_put_44 = store.put(42, 'fallback')
  const req_openKeyCursor_45 = store.openKeyCursor(true, 'nextunique')
  const req_delete_46 = store.delete(true)
  const req_put_47 = store.put(42)
  const req_count_48 = store.count(true)
  const req_getKey_49 = store.getKey(true)
  const req_add_50 = store.add(true, 42)
  const req_getAll_51 = store.getAll('fallback')
  const req_delete_52 = store.delete('fallback')
  const req_add_53 = store.add('fallback')
  const req_getAllKeys_54 = store.getAllKeys(83)
  const req_put_55 = store.put('fallback', true)
  const req_getAllKeys_56 = store.getAllKeys('fallback', 3)
  const req_getAllKeys_57 = store.getAllKeys('fallback')
  const req_put_58 = store.put(true)
  const req_delete_59 = store.delete(true)
  const req_count_60 = store.count()
  const req_add_61 = store.add('fallback')
  const req_clear_62 = store.clear()
  const req_add_63 = store.add('fallback')
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
const deleteRequest = indexedDB.deleteDatabase('str_7976')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
