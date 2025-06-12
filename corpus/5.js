let db;
const openRequest = window.indexedDB.open('str_5343')
openRequest.onupgradeneeded = (event) => {
  console.log('db onupgraded trigered');
  db = event.target.result;
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_9455', ['str_6388', 'str_4805', 'str_5584', 'str_4411']);
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  store_1 = db.createObjectStore('store_1');
  index_0 = store_0.createIndex('str_8510', ['str_7508', 'str_9217', 'str_5077', 'str_5383', 'str_3062']);
  index_0.name
  store_0.keyPath
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  index_0 = store_1.createIndex('str_7361', ['str_8043', 'str_4166'], {'unique': false, 'multiEntry': false});
  store_1.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_4704', 'str_175', {'unique': false, 'multiEntry': true});
  db.deleteObjectStore('store_0')
  store_0 = db.createObjectStore('store_0');
  index_0 = store_0.createIndex('str_8804', ['str_6516', 'str_6047', 'str_4544', 'str_7175', 'str_7560']);
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  index_0 = store_1.createIndex('str_5315', 'str_9975');
  index_1 = store_1.createIndex('str_5731', 'str_255', {'unique': true, 'multiEntry': true});
  index_2 = store_1.createIndex('str_1915', ['str_1235', 'str_891', 'str_4840']);
  index_3 = store_0.createIndex('str_7848', ['str_9669', 'str_5044', 'str_7507', 'str_621'], {'unique': true, 'multiEntry': false});
  index_4 = store_0.createIndex('str_5427', ['str_1466', 'str_7488', 'str_8970', 'str_9044']);
  index_5 = store_1.createIndex('str_9954', ['str_6173']);
  db.deleteObjectStore('store_1')
  store_1 = db.createObjectStore('store_1');
  index_0 = store_1.createIndex('str_9162', ['str_5613', 'str_9860', 'str_3636', 'str_8419']);
  store_1.deleteIndex('index_0')
  index_0 = store_1.createIndex('str_4032', ['str_3186', 'str_4446', 'str_5636', 'str_2456'], {'unique': true, 'multiEntry': false});
  store_1.deleteIndex('index_0')
  index_0 = store_1.createIndex('str_6088', ['str_8482', 'str_9213', 'str_4511', 'str_6995', 'str_5564'], {'unique': true, 'multiEntry': false});
  store_1.autoIncrement
  store_0.deleteIndex('index_0')
  index_0 = store_0.createIndex('str_7351', 'str_4063');
};
openRequest.onsuccess = (event) => {
  console.log('db onsuccess triggered')
  db = openRequest.result;
  const txn = db.transaction('store_1', 'readwrite')
  const store = txn.objectStore('store_1')
  const req_getAll_0 = store.getAll()
  const req_count_1 = store.count()
  const req_openKeyCursor_2 = store.openKeyCursor(None, 'prev')
  const req_openKeyCursor_3 = store.openKeyCursor()
  const req_put_4 = store.put('fallback', 42)
  const req_delete_5 = store.delete(42)
  const req_openKeyCursor_6 = store.openKeyCursor()
  const req_put_7 = store.put(42, 'fallback')
  const req_getAll_8 = store.getAll(true, 13)
  const req_getAll_9 = store.getAll()
  const req_add_10 = store.add(true, 42)
  const req_add_11 = store.add(42, true)
  const req_add_12 = store.add(42, 'fallback')
  const req_get_13 = store.get(true)
  const req_count_14 = store.count(42)
  const req_getKey_15 = store.getKey(42)
  const req_delete_16 = store.delete(true)
  const req_getKey_17 = store.getKey(42)
  const req_getKey_18 = store.getKey(true)
  const req_getAllKeys_19 = store.getAllKeys()
  const req_getAllKeys_20 = store.getAllKeys(true, 73)
  const req_getAllKeys_21 = store.getAllKeys()
  const req_openCursor_22 = store.openCursor()
  const req_getAll_23 = store.getAll('fallback')
  const req_put_24 = store.put(true)
  const req_add_25 = store.add(42)
  const req_getKey_26 = store.getKey(42)
  const req_count_27 = store.count()
  const req_delete_28 = store.delete(42)
  const req_delete_29 = store.delete(true)
  const req_count_30 = store.count()
  const req_openKeyCursor_31 = store.openKeyCursor('nextunique')
  const req_getAllKeys_32 = store.getAllKeys()
  const req_getAllKeys_33 = store.getAllKeys()
  const req_put_34 = store.put(true, true)
  const req_openCursor_35 = store.openCursor(None)
  const req_openCursor_36 = store.openCursor(true)
  const req_put_37 = store.put(42)
  const req_count_38 = store.count(true)
  const req_clear_39 = store.clear()
  const req_getAllKeys_40 = store.getAllKeys(true)
  const req_count_41 = store.count()
  const req_count_42 = store.count()
  const req_getAllKeys_43 = store.getAllKeys(true, 39)
  const req_add_44 = store.add(true)
  const req_delete_45 = store.delete(42)
  const req_count_46 = store.count()
  const req_count_47 = store.count()
  const req_add_48 = store.add(true)
  const req_get_49 = store.get(42)
  const req_getAllKeys_50 = store.getAllKeys()
  const req_put_51 = store.put(true)
  const req_openCursor_52 = store.openCursor(None, 'nextunique')
  const req_put_53 = store.put(42, 42)
  const req_delete_54 = store.delete(true)
  const req_count_55 = store.count()
  const req_delete_56 = store.delete(true)
  const req_clear_57 = store.clear()
  const req_clear_58 = store.clear()
  const req_add_59 = store.add('fallback')
  const req_get_60 = store.get('fallback')
  const req_openCursor_61 = store.openCursor()
  const req_openCursor_62 = store.openCursor('fallback')
  const req_put_63 = store.put(42, 42)
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
const deleteRequest = indexedDB.deleteDatabase('str_5343')
deleteRequest.onblocked = (event) => {
  console.log('delete db onblocked triggered')
};
deleteRequest.onsuccess = (event) => {
  console.log('delete db onsuccess triggered')
};
deleteRequest.onerror = (event) => {
  console.log('delete db onerror triggered')
};
