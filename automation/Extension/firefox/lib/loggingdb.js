const fileIO            = require("sdk/io/file");
const system            = require("sdk/system");
const {Cc, Ci, CC, Cu, components} = require("chrome");

var socket              = require("./socket.js");

var crawlId= null;
var siteID = null;
var linkID = null
var requestID = null
var responseID = null 
var cookieID = null
var debugging = false;
var sqliteAggregator = null;
var ldbAggregator = null;
var aFile = null;
var dataDirectrory = null;
//var logAggregator = null;
var listeningSocket = null;
var noFile=null;



exports.open = function(sqliteAddress, ldbAddress, dataDir, crawlID) {
    if (sqliteAddress == null && ldbAddress == null && crawlID == '') {
        console.log("Debugging, everything will output to console");
        debugging = true;
        return;
    }
    
    crawlId = crawlID;
    dataDirectory = dataDir;
    console.log("Data dir ", dataDir);
    // Connect to databases for saving data
    console.log("Opening socket connections...");
    if (sqliteAddress != null) {
        sqliteAggregator = new socket.SendingSocket();
        var rv = sqliteAggregator.connect(sqliteAddress[0], sqliteAddress[1]);
        console.log("sqliteSocket started?",rv);
    }
    if (ldbAddress != null) {
        ldbAggregator = new socket.SendingSocket();
        var rv = ldbAggregator.connect(ldbAddress[0], ldbAddress[1]);
        console.log("ldbSocket started?",rv);
    }

    aFile = Cc["@mozilla.org/file/local;1"].createInstance(Ci.nsILocalFile);
    console.log("aFile: ",aFile);
    console.log ('noFile', noFile);
    noFile=0;
    console.log ('noFile', noFile);
 /*   // Connect to loggingServerJS for logging information and debugging data
    if (logAddress != null) {
        logAggregator = new socket.SendingSocket();
        var rv = logAggregator.connect(logAddress[0], logAddress[1]);
        console.log("sqliteSocket started?",rv);
    } */
   
  

    // Listen for incomming urls as visit ids
    listeningSocket = new socket.ListeningSocket();
    var path = system.pathFor("ProfD") + '/extension_port.txt';
    console.log("Writing listening socket port to disk at:", path);
    var file = fileIO.open(path, 'w');
    if (!file.closed) {
        file.write(listeningSocket.port);
        file.close();
        console.log("Port",listeningSocket.port,"written to disk.");
    }
    console.log("Starting socket listening for incomming connections.");
    listeningSocket.startListening();

    
};

exports.close = function() {
    if (sqliteAggregator != null) {
        sqliteAggregator.close();
    }
    if (ldbAggregator != null) {
        ldbAggregator.close();
    }
};

exports.executeSQL = function(statement, async) {
    // send to console if debugging
    // TODO remove async argument
    if (debugging) {
        if (typeof statement == 'string'){
            console.log("SQLite",statement);
        }else{  // log the table name and values to be inserted
            var table_name = statement[0].replace("INSERT INTO ", "").split(" ")[0];
            console.log("SQLite", table_name, statement[1]);
        }
        return;
    }
    // catch statements without arguments
    if (typeof statement == "string") {
        var statement = [statement, []];
    }
    sqliteAggregator.send(statement);
};

exports.saveContent = function(content, contentHash) {
  // send content to levelDBAggregator which stores content
  // deduplicated by contentHash in a levelDB database
  if (debugging) {
    console.log("LDB contentHash:",contentHash,"with length",content.length);
    return;
  }
  ldbAggregator.send([content, contentHash]);
}

function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

exports.escapeString = function(string) {
    // Convert to string if necessary
    if(typeof string != "string")
        string = "" + string;

    return encode_utf8(string);
};



exports.boolToInt = function(bool) {
    return bool ? 1 : 0;
};

exports.createInsert2 = function(table, update) {
    // Add top url visit id if changed
    while (!debugging && listeningSocket.queue.length != 0) {
        siteID = listeningSocket.queue.shift();        
    }

    update["site_id"] = siteID;

    var statement = "INSERT INTO " + table + " (";
    var value_str = "VALUES (";
        var values = [];
    var first = true;
    for(var field in update) {
        statement += (first ? "" : ", ") + field;
        value_str += (first ? "?" : ",?");
                values.push(update[field]);
        first = false;
    }
    statement = statement + ") " + value_str + ")";
    return [statement, values];
}


exports.createInsert = function(table, update) {
    // Add top url visit id if changed
    while (!debugging && listeningSocket.queue.length != 0) {
        visit = listeningSocket.queue.shift();      
        siteID = visit["site_id"];
        linkID  = visit["link_id"];
        requestID = 0; responseID = 0; cookieID = 0;
        noFile = 0;
        
    }

    if (table == 'http_requests'){ 
       requestID += 1; 
       update["request_id"] = requestID;
       path = dataDirectory + "/../log/req-" + siteID + "-" + linkID + "-" + requestID;
    }
    if (table == 'http_responses'){ 
       responseID += 1; 
       update["response_id"] = responseID;
       path = dataDirectory + "/../log/res-" + siteID + "-" + linkID + "-" + responseID;
    } 
    if (table == 'cookies'){ 
       cookieID += 1; 
       update["cookie_id"] = cookieID;
       path = dataDirectory + "/../log/coo-" + siteID + "-" + linkID + "-" + cookieID;
    }
    update["site_id"] = siteID;
    update["link_id"] = linkID;
  /*   
    var file = fileIO.open(path, 'w');
    if (!file.closed) {
        file.write("nesto");
        file.close()
    }
*/
    var statement = "INSERT INTO " + table + " (";
    var value_str = "VALUES (";
        var values = [];
    var first = true;
    for(var field in update) {
        statement += (first ? "" : ", ") + field;
        value_str += (first ? "?" : ",?");
                values.push(update[field]);
        first = false;
    }
    statement = statement + ") " + value_str + ")";
    return [statement, values];
}


exports.writeRespBodyIntoFile = function(respBody,type) {

  while (!debugging && listeningSocket.queue.length != 0) {
    visit = listeningSocket.queue.shift();      
    noFile = 0;
    siteID = visit["site_id"];
    linkID  = visit["link_id"]; 
    requestID = 0; responseID = 0; cookieID = 0;
    noFile = 0;
     
  }; 

    noFile = noFile + 1;
    var name = "file-" + siteID + "-" + linkID + "-" + (responseID + 1)//noFile;
    if (type == "html") {
	name = name + ".html";
    } else if (type == "image") {
        name = name + ".image";
    };
  var fileName = dataDirectory + "/httpResp/" + "site-" + siteID + "/" + name; 
  console.log("fileName logg",fileName); 
  aFile.initWithPath(fileName);
  //console.log("initialize file",fileName);
  aFile.createUnique(Ci.nsIFile.NORMAL_FILE_TYPE, 0600);
  var stream = Cc["@mozilla.org/network/safe-file-output-stream;1"].createInstance(Ci.nsIFileOutputStream);
  stream.init(aFile, 0x04 | 0x08 | 0x20, 0600, 0); // readwrite, create, truncate           
  stream.write(respBody, respBody.length);    
  if (stream instanceof Ci.nsISafeOutputStream) {
    stream.finish();
  } else {
    stream.close();
  };
  return name
}



/*
exports.logging = function(text){
    loggingAggregator.send(text)
}*/
