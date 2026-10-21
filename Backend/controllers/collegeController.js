const College = require("../models/College");

// Get all colleges
const getColleges = async (req, res) => {
  try {
    const colleges = await College.find();
    res.json(colleges);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Add new college
const addCollege = async (req, res) => {
  try {
    const college = new College(req.body);
    await college.save();
    res.status(201).json(college);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

module.exports = {
  getColleges,
  addCollege,
};