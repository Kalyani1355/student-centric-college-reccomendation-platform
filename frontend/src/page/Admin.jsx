import { useState } from "react";
import axios from "axios";

function Admin() {
  const [college, setCollege] = useState({
    name: "",
    course: "",
    city: "",
    fees: "",
    placement: "",
    highestPackage: "",
    averagePackage: "",
    rating: "",
    image: "",
    website: "",
    description: "",
  });

  const handleChange = (e) => {
    setCollege({
      ...college,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post(
        "http://localhost:5000/api/colleges",
        college
      );

      alert("College Added Successfully ✅");

      setCollege({
        name: "",
        course: "",
        city: "",
        fees: "",
        placement: "",
        highestPackage: "",
        averagePackage: "",
        rating: "",
        image: "",
        website: "",
        description: "",
      });
    } catch (err) {
      console.log(err);
      alert("Error adding college");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Add College</h1>

      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="College Name" value={college.name} onChange={handleChange} /><br /><br />
        <input name="courses" placeholder="Courses" value={college.course} onChange={handleChange} /><br /><br />
        <input name="city" placeholder="City" value={college.city} onChange={handleChange} /><br /><br />
        <input name="image" placeholder="Image URL" value={college.image} onChange={handleChange} /><br /><br />
        <input name="website" placeholder="Website" value={college.website} onChange={handleChange} /><br /><br />

        <textarea
          name="description"
          placeholder="Description"
          value={college.description}
          onChange={handleChange}
        />

        <br /><br />

        <button type="submit">
          Add College
        </button>
      </form>
    </div>
  );
}

export default Admin;