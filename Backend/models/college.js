const mongoose = require("mongoose");

const collegeSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  course: {
    type: String,
    required: true,
  },
  city: {
    type: String,
    required: true,
  },
  fees: {
    type: String,
    required: true,
  },
  placement: {
    type: String,
    required: true,
  },
  highestPackage: {
    type: String,
  },
  averagePackage: {
    type: String,
  },
  rating: {
    type: String,
  },
  image: {
    type: String,
  },
  website: {
    type: String,
  },
  description: {
    type: String,
  },
});

module.exports = mongoose.model("College", collegeSchema);