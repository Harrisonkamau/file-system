// import the required modules
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var multer = require('multer');

// define the destination of the uploaded file
var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname); // retain the original name after upload
  }
});
var upload = multer({ storage: storage });

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// parse application/json
app.use(bodyParser.json());


// load the home page
app.get('/', function(req, res){
  res.sendFile(__dirname + '/form.html');
});

// create upload route
 app.post('/upload', upload.single('uploadedFile'), function(req, res, next) {
    if(req.file){
        console.dir(req.file); // log out the file's directory
        return "Upload successful";
    }
    return "Missing file!";
    });

// start the server
app.listen(3000, () =>{
  console.log("Listening on port 3000");
})