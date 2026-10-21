import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import axios from "axios";
import "../App.css";

function FindCollege() {
  const [searchParams] = useSearchParams();

  const courseFromUrl = searchParams.get("course") || "";

  const [course, setCourse] = useState(courseFromUrl);
  const [city, setCity] = useState("");
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const navigate = useNavigate();

  const findColleges = async () => {
    if (!course || !city) {
      alert("Please select Course and City");
      return;
    }

    try {
      setLoading(true);
      setSearched(true);

      const response = await axios.get(
        "http://localhost:5000/api/search",
        {
          params: {
            course: course,
            city: city,
          },
        }
      );

      console.log("COLLEGES:", response.data);

      setColleges(response.data);
    } catch (error) {
      console.error("Find College Error:", error);
      alert("Unable to find colleges. Please check Python backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="find-college-page">

      <div className="find-college-container">

        <h1>🎓 Find Your College</h1>

        <p>
          Select your preferred course and city.
        </p>

        {/* COURSE */}
        <div className="find-field">

          <label>🎓 Select Your Course</label>

        
          <input
  type="text"
  placeholder="Enter Course"
  value={course}
  onChange={(e) => setCourse(e.target.value)}
/>

        </div>

        {/* CITY */}
        <div className="find-field">

          <label>📍 Preferred City</label>

          <input
  type="text"
  placeholder="Enter City (Example: Pune)"
  value={city}
  onChange={(e) => setCity(e.target.value)}
/>

        </div>

        {/* BUTTON */}
        <button
          className="find-college-btn"
          onClick={findColleges}
        >
          {loading ? "Finding..." : "🔍 Find Colleges"}
        </button>

      </div>

      {/* RESULTS */}
      {searched && (
        <div className="recommended-section">

          <h2>Recommended Colleges</h2>

          {loading ? (
            <p>Finding colleges...</p>
          ) : colleges.length === 0 ? (
            <p>
              No colleges found for {course} in {city}.
            </p>
          ) : (
            <div className="college-name-list">

              {colleges.map((college, index) => (

                <div
                  className="college-name-item"
                  key={college._id}
                  onClick={() =>
                    navigate(`/college/${college._id}`)
                  }
                >

                  <span>
                    {index + 1}.
                  </span>

                  <span>
                    {college.name}
                  </span>

                </div>

              ))}

            </div>
          )}

        </div>
      )}

    </div>
  );
}

export default FindCollege;