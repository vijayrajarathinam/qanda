const express = require("express");
const cors = require("cors");
const fileUpload = require("express-fileupload");
const cookieParser = require("cookie-parser");

const app = express();

// Enable dotenv
require("dotenv").config();

// handle application/json
app.use(express.json());

// handle application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// read cookie values
app.use(cookieParser());

// enable cors
app.use(cors());

// handle file upload and validate
app.use(fileUpload({ safeFileNames: true, preserveExtension: true }));

// set public directory
app.use(express.static(__dirname + "/public"));

// start the server
const server = app.listen(process.env.PORT || 8000, () => {
  console.log(`Listening at port ${server.address().port}`);
});
