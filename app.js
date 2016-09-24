var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var router = express.Router();
var path = require('path');
var fs = require('fs');
var multer = require('multer');
var upload = multer({dest: 'uploads/'});

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// parse application/json
app.use(bodyParser.json());

app.get('/', function(req, res){
  res.sendFile(__dirname + '/form.html');
})

app.post("/upload", upload.single('uploadedFile'), function(req, res){
  var file = req.file;
  // fs.createReadStream(file.path).pipe(csv).on('data', function(data){
  //   res.json(data);
  // })
  var readStream = fs.createReadStream(file.path);
  readStream.on('open', function(){
    
    readStream.pipe(res);
  });

  // rename the uploaded file
  fs.rename(file.path, '/uploads'+path.extname(file), (err) =>{
    if(err) throw err;
    console.log("Renaming complete");
  })

  // console.log(file.originalname);
   readStream.on('error', function(err) {
    res.end(err);
  });
});



// start the server
app.listen(3000, () =>{
  console.log("Listening on port 3000");
})
