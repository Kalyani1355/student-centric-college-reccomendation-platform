const express = require("express");
const router = express.Router();

const College = require("../models/College");

const {
  getColleges,
  addCollege,
} = require("../controllers/collegeController");

// GET all colleges
router.get("/", getColleges);

// POST new college
router.post("/", async (req, res) => {
  try {
    const college = await College.create(req.body);
    res.status(201).json(college);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
// DELETE college
router.delete("/:id", async (req, res) => {
  try {
    const college = await College.findByIdAndDelete(req.params.id);

    if (!college) {
      return res.status(404).json({ message: "College not found" });
    }

    res.json({ message: "College deleted successfully" });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;