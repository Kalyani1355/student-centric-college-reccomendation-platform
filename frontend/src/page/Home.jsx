import { useState } from "react";
import { Link } from "react-router-dom";
import "../App.css";
import hero from "../assets/hero.jpg";
import CollegeCard from "../components/CollegeCard";
import Footer from "../components/Footer";
import axios from "axios";

function Home() {
  const [city, setCity] = useState("");
  const [searchText, setSearchText] = useState("");
  const [favorites, setFavorites] = useState([]);
  const [colleges, setColleges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const [compareColleges, setCompareColleges] = useState([]);

  // ================= COMPARE =================
  const toggleCompare = (college) => {
    const currentCompare = Array.isArray(compareColleges)
      ? compareColleges
      : [];

    const alreadySelected = currentCompare.some(
      (item) => item._id === college._id
    );

    if (alreadySelected) {
      setCompareColleges(
        currentCompare.filter(
          (item) => item._id !== college._id
        )
      );
      return;
    }

    if (currentCompare.length >= 3) {
      alert("You can compare maximum 3 colleges.");
      return;
    }

    setCompareColleges([
      ...currentCompare,
      college,
    ]);
  };

  // ================= SEARCH =================
  const searchColleges = async () => {
    const selectedCourse = searchText.trim();
    const selectedCity = city.trim();

    if (!selectedCourse) {
      alert("Please enter a course.");
      return;
    }

    try {
      setLoading(true);
      setHasSearched(true);
      setColleges([]);

      console.log("SEARCH COURSE:", selectedCourse);
      console.log("SEARCH CITY:", selectedCity);

      const response = await axios.get(
        "http://localhost:5000/api/search",
        {
          params: {
            course: selectedCourse,
            city: selectedCity,
          },
        }
      );

      console.log("SEARCH RESPONSE:", response.data);

      if (Array.isArray(response.data)) {
        setColleges(response.data);
      } else {
        setColleges([]);
      }
    } catch (error) {
      console.error("SEARCH ERROR:", error);

      setColleges([]);

      alert(
        "Search failed. Please make sure Python backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // ================= COURSE BUTTON =================
  const handleCourseSearch = (course) => {
    setSearchText(course);
    setHasSearched(false);

    document
      .getElementById("college-search")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  // ================= FAVORITE =================
  const toggleFavorite = (id) => {
    if (favorites.includes(id)) {
      setFavorites(
        favorites.filter(
          (fav) => fav !== id
        )
      );
    } else {
      setFavorites([
        ...favorites,
        id,
      ]);
    }
  };

  return (
    <div className="home-page">

      {/* ================= HERO ================= */}
      <section
        className="home-hero"
        id="home"
        style={{
          backgroundImage: `url(${hero})`,
        }}
      >
        <div className="home-hero-overlay"></div>

        <div className="home-hero-content">

          <span className="home-hero-badge">
            🎓 Smart College Finder
          </span>

          <h1>
            Find Your Dream College
          </h1>

          <p>
            Discover colleges based on your preferred
            course, city and requirements.
          </p>

          {/* ================= SEARCH BOX ================= */}
          <div
            className="home-search-box"
            id="college-search"
          >

            {/* COURSE */}
            <div className="home-search-field">
              <label>🎓 Course</label>

              <input
                type="text"
                placeholder="Enter Course (Example: MCA)"
                value={searchText}
                onChange={(e) => {
                  setSearchText(e.target.value);
                  setHasSearched(false);
                }}
              />
            </div>

            {/* CITY */}
            <div className="home-search-field">
              <label>📍 City</label>

              <input
                type="text"
                placeholder="Enter City (Example: Pune)"
                value={city}
                onChange={(e) => {
                  setCity(e.target.value);
                  setHasSearched(false);
                }}
              />
            </div>

            {/* SEARCH BUTTON */}
            <button
              className="home-search-btn"
              onClick={searchColleges}
              disabled={loading}
            >
              {loading
                ? "Searching..."
                : "🔍 Search"}
            </button>

          </div>

          <p className="home-search-note">
            Enter your course and city to discover
            matching colleges.
          </p>

        </div>
      </section>


      {/* ================= SEARCH RESULTS ================= */}
      {hasSearched && (
        <section
          className="home-section search-results-section"
        >

          <div className="home-section-heading">

            <span>RESULTS</span>

            <h2>
              Colleges For You
            </h2>

            <p>
              {city
                ? `Showing colleges matching ${searchText} in ${city}`
                : `Showing colleges matching ${searchText}`}
            </p>

          </div>


          {/* LOADING */}
          {loading ? (

            <div className="home-result-message">

              <div className="home-spinner"></div>

              <h3>
                Finding colleges...
              </h3>

              <p>
                Checking available colleges for your search.
              </p>

            </div>

          ) : !Array.isArray(colleges) ||
            colleges.length === 0 ? (

            /* NO RESULT */
            <div className="home-result-message">

              <div className="no-result-icon">
                🔍
              </div>

              <h3>
                No colleges found
              </h3>

              <p>
                Try another course or city.
              </p>

            </div>

          ) : (

            /* RESULTS */
            <div className="home-college-grid">

              {colleges.map((college) => (

                <CollegeCard
                  key={college._id}
                  college={college}
                  favorites={favorites}
                  toggleFavorite={toggleFavorite}
                  compareColleges={compareColleges}
                  toggleCompare={toggleCompare}
                />

              ))}

            </div>

          )}

        </section>
      )}


      {/* ================= COMPARE BAR ================= */}
      {Array.isArray(compareColleges) &&
        compareColleges.length > 0 && (

        <div className="compare-bar">

          <div>
            <strong>
              {compareColleges.length} College
              {compareColleges.length > 1
                ? "s"
                : ""} Selected
            </strong>

            <span>
              Select up to 3 colleges to compare
            </span>
          </div>

          <button
            className="compare-main-btn"
            onClick={() => {
              document
                .getElementById("compare-section")
                ?.scrollIntoView({
                  behavior: "smooth",
                });
            }}
          >
            ⚖ Compare Colleges
          </button>

        </div>
      )}


      {/* ================= COMPARE SECTION ================= */}
      {Array.isArray(compareColleges) &&
        compareColleges.length > 0 && (

        <section
          className="compare-section"
          id="compare-section"
        >

          <div className="home-section-heading">

            <span>
              COMPARISON
            </span>

            <h2>
              Compare Colleges
            </h2>

            <p>
              Compare your selected colleges side by side.
            </p>

          </div>


          <div className="compare-table-wrapper">

            <table className="compare-table">

              <thead>

                <tr>

                  <th>
                    Information
                  </th>

                  {compareColleges.map(
                    (college) => (

                    <th
                      key={college._id}
                    >

                      <div className="compare-college-name">
                        {college.name}
                      </div>

                      <button
                        className="remove-compare-btn"
                        onClick={() =>
                          toggleCompare(college)
                        }
                      >
                        ✕ Remove
                      </button>

                    </th>

                  ))}

                </tr>

              </thead>


              <tbody>

                {/* CITY */}
                <tr>

                  <td>
                    📍 City
                  </td>

                  {compareColleges.map(
                    (college) => (

                    <td
                      key={college._id}
                    >
                      {college.city || "N/A"}
                    </td>

                  ))}

                </tr>


                {/* COURSE */}
                <tr>

                  <td>
                    🎓 Detected Courses
                  </td>

                  {compareColleges.map(
                    (college) => (

                    <td
                      key={college._id}
                    >

                      {Array.isArray(college.courses)
                        ? college.courses.join(", ")
                        : "N/A"}

                    </td>

                  ))}

                </tr>


                {/* WEBSITE */}
                <tr>

                  <td>
                    🌐 Website
                  </td>

                  {compareColleges.map(
                    (college) => (

                    <td
                      key={college._id}
                    >

                      {college.website ? (

                        <a
                          href={
                            college.website.startsWith("http")
                              ? college.website
                              : `https://${college.website}`
                          }
                          target="_blank"
                          rel="noopener noreferrer"
                          className="compare-details-btn"
                        >
                          Official Website
                        </a>

                      ) : (
                        "N/A"
                      )}

                    </td>

                  ))}

                </tr>


                {/* REMOVE */}
                <tr>

                  <td>
                    Action
                  </td>

                  {compareColleges.map(
                    (college) => (

                    <td
                      key={college._id}
                    >

                      <button
                        className="remove-compare-btn"
                        onClick={() =>
                          toggleCompare(college)
                        }
                      >
                        Remove
                      </button>

                    </td>

                  ))}

                </tr>

              </tbody>

            </table>

          </div>

        </section>
      )}


      {/* ================= POPULAR COURSES ================= */}
      <section
        className="home-section courses-section"
        id="courses"
      >

        <div className="home-section-heading">

          <span>
            EXPLORE
          </span>

          <h2>
            Popular Courses
          </h2>

          <p>
            Start your college search by selecting
            your preferred course.
          </p>

        </div>


        <div className="home-course-grid">

          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("B.Tech")
            }
          >
            <div className="course-icon">
              ⚙️
            </div>

            <h3>
              B.Tech
            </h3>

            <p>
              Engineering & Technology
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>


          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("BCA")
            }
          >

            <div className="course-icon">
              💻
            </div>

            <h3>
              BCA
            </h3>

            <p>
              Computer Applications
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>


          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("MCA")
            }
          >

            <div className="course-icon">
              🎓
            </div>

            <h3>
              MCA
            </h3>

            <p>
              Master of Computer Applications
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>


          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("MBA")
            }
          >

            <div className="course-icon">
              📊
            </div>

            <h3>
              MBA
            </h3>

            <p>
              Business & Management
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>


          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("B.Sc")
            }
          >

            <div className="course-icon">
              🔬
            </div>

            <h3>
              B.Sc
            </h3>

            <p>
              Science & Research
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>


          <button
            className="home-course-card"
            onClick={() =>
              handleCourseSearch("B.Pharm")
            }
          >

            <div className="course-icon">
              💊
            </div>

            <h3>
              B.Pharm
            </h3>

            <p>
              Pharmacy & Healthcare
            </p>

            <span>
              Explore Colleges →
            </span>

          </button>

        </div>

      </section>


      {/* ================= FIND MY COLLEGE ================= */}
      <section
        className="find-my-college-section"
        id="find-college"
      >

        <div className="find-my-college-container">

          <div className="find-my-college-content">

            <span>
              PERSONALIZED SEARCH
            </span>

            <h2>
              Find the Right College
              <br />
              For Your Future
            </h2>

            <p>
              Not sure which college is right for you?
              Tell us about your preferences and explore
              colleges that match your requirements.
            </p>

            <Link
              to="/find-college"
              className="find-college-main-btn"
            >
              Find My College →
            </Link>

          </div>


          <div className="find-my-college-features">

            <div className="find-feature">

              <div>🎓</div>

              <h3>
                Choose Course
              </h3>

              <p>
                Select the course you want to study.
              </p>

            </div>


            <div className="find-feature">

              <div>📍</div>

              <h3>
                Enter City
              </h3>

              <p>
                Enter your preferred city.
              </p>

            </div>


            <div className="find-feature">

              <div>⭐</div>

              <h3>
                Set Preferences
              </h3>

              <p>
                Choose your college preferences.
              </p>

            </div>

          </div>

        </div>

      </section>


      {/* ================= EDUCATION ================= */}
      <section
        className="home-section education-section"
      >

        <div className="home-section-heading">

          <span>
            EDUCATION
          </span>

          <h2>
            Explore Education Levels
          </h2>

          <p>
            Find colleges according to your education level.
          </p>

        </div>


        <div className="education-level-grid">

          <Link
            to="/graduation"
            className="education-level-card"
          >

            <div className="education-card-icon">
              🎓
            </div>

            <div>

              <h3>
                Graduation
              </h3>

              <p>
                B.Tech, BCA, B.Sc, BBA, B.Com and more
              </p>

            </div>

            <span>
              →
            </span>

          </Link>


          <Link
            to="/education"
            className="education-level-card"
          >

            <div className="education-card-icon">
              📚
            </div>

            <div>

              <h3>
                Post Graduation
              </h3>

              <p>
                MCA, MBA, M.Sc and other postgraduate programs
              </p>

            </div>

            <span>
              →
            </span>

          </Link>


          <Link
            to="/education"
            className="education-level-card"
          >

            <div className="education-card-icon">
              🔬
            </div>

            <div>

              <h3>
                PhD
              </h3>

              <p>
                Research and doctoral programs
              </p>

            </div>

            <span>
              →
            </span>

          </Link>

        </div>

      </section>


      {/* ================= WHY EDUFINDER ================= */}
      <section
        className="home-section why-edufinder-section"
      >

        <div className="home-section-heading">

          <span>
            WHY EDUFINDER
          </span>

          <h2>
            Everything You Need to Find Your College
          </h2>

          <p>
            A simple way to explore and compare colleges.
          </p>

        </div>


        <div className="why-edufinder-grid">

          <div className="why-card">

            <div>
              🔎
            </div>

            <h3>
              Easy Search
            </h3>

            <p>
              Search colleges using course and city.
            </p>

          </div>


          <div className="why-card">

            <div>
              📊
            </div>

            <h3>
              Compare Information
            </h3>

            <p>
              Compare available college information.
            </p>

          </div>


          <div className="why-card">

            <div>
              🏫
            </div>

            <h3>
              Official College Website
            </h3>

            <p>
              Visit the official college website
              for complete and updated information.
            </p>

          </div>


          <div className="why-card">

            <div>
              ❤️
            </div>

            <h3>
              Save Favorites
            </h3>

            <p>
              Keep track of colleges you are interested in.
            </p>

          </div>

        </div>

      </section>


      {/* ================= CONTACT ================= */}
      <section
        className="home-contact-section"
        id="contact"
      >

        <div className="home-contact-container">

          <div className="home-contact-info">

            <span>
              GET IN TOUCH
            </span>

            <h2>
              Have Questions?
            </h2>

            <p>
              If you need help finding a college or have
              questions about EduFinder, feel free to contact us.
            </p>

            <div className="contact-info-item">

              <div>
                📧
              </div>

              <div>

                <strong>
                  Email
                </strong>

                <p>
                  support@edufinder.com
                </p>

              </div>

            </div>


            <div className="contact-info-item">

              <div>
                📍
              </div>

              <div>

                <strong>
                  Location
                </strong>

                <p>
                  Maharashtra, India
                </p>

              </div>

            </div>

          </div>


          <div className="home-contact-card">

            <h3>
              Contact Us
            </h3>

            <input
              type="text"
              placeholder="Your Name"
            />

            <input
              type="email"
              placeholder="Your Email"
            />

            <textarea
              placeholder="Your Message"
              rows="5"
            ></textarea>

            <button
              type="button"
              onClick={() =>
                alert(
                  "Thank you! Your message has been received."
                )
              }
            >
              Send Message →
            </button>

          </div>

        </div>

      </section>


      {/* ================= FOOTER ================= */}
      <Footer />

    </div>
  );
}

export default Home;