import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../App.css";

function CollegeDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [college, setCollege] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/colleges/${id}`)
      .then((res) => {
        console.log("COLLEGE DATA:", res.data);
        setCollege(res.data);
        setLoading(false);
      })
      .catch((error) => {
        console.log("College Details Error:", error);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="details-loading">
        <div className="loading-spinner"></div>
        <h2>Loading college details...</h2>
      </div>
    );
  }

  if (!college) {
    return (
      <div className="details-loading">
        <h2>🏫 College Not Found</h2>
        <button onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>
    );
  }

  // =========================
  // COLLEGE IMAGE
  // =========================

  const imageUrl = college.image
    ? college.image.startsWith("http")
      ? college.image
      : `http://localhost:5174${college.image}`
    : "";

  // =========================
  // COURSES
  // =========================

  const courses = college.course
    ? college.course
        .replace(/\n/g, "")
        .replace(")", "")
        .split(",")
        .map((course) => course.trim())
        .filter(Boolean)
    : [];

  return (
    <div className="college-details-page">

      {/* =====================================
          TOP UTILITY BAR
      ===================================== */}

      <div className="college-topbar">
        <div className="college-topbar-container">

          <span>
            🎓 EduFinder College Information
          </span>

          <div className="topbar-links">
            <span>📞 Admission Help</span>
            <span>✉️ Contact</span>
          </div>

        </div>
      </div>


      {/* =====================================
          COLLEGE MAIN HEADER
      ===================================== */}

      <header className="college-main-header">

        <div className="college-brand">

          <div className="college-logo">
            🎓
          </div>

          <div className="college-brand-text">

            <h1>
              {college.name}
            </h1>

            <p>
              📍 {college.city}, Maharashtra
            </p>

          </div>

        </div>

        <div className="college-rating-large">

          <strong>
            ⭐ {college.rating}
          </strong>

          <span>
            College Rating
          </span>

        </div>

      </header>


      {/* =====================================
          MAIN NAVIGATION
      ===================================== */}

      <nav className="college-navigation">

        <div className="college-navigation-container">

          <button
            onClick={() =>
              document
                .getElementById("college-home")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Home
          </button>

          <button
            onClick={() =>
              document
                .getElementById("about")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            About
          </button>

          <button
            onClick={() =>
              document
                .getElementById("admissions")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Admissions
          </button>

          <button
            onClick={() =>
              document
                .getElementById("academics")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Academics
          </button>

          <button
            onClick={() =>
              document
                .getElementById("placement")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Placement
          </button>

          <button
            onClick={() =>
              document
                .getElementById("campus")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Campus Life
          </button>

          <button
            onClick={() =>
              document
                .getElementById("contact")
                ?.scrollIntoView({
                  behavior: "smooth",
                })
            }
          >
            Contact
          </button>

        </div>

      </nav>


      {/* =====================================
          NEWS / UPDATE BAR
      ===================================== */}

      <div className="college-news-bar">

        <div className="news-label">
          📢 Latest Updates
        </div>

        <div className="news-text">
          Admissions, courses and placement information
          available for students
        </div>

      </div>


      {/* =====================================
          HERO IMAGE
      ===================================== */}

      <section
        id="college-home"
        className="college-detail-hero"
      >

        {imageUrl ? (
          <img
            src={imageUrl}
            alt={`${college.name} campus`}
            onError={(e) => {
              console.log(
                "IMAGE FAILED:",
                imageUrl
              );

              e.currentTarget.style.display =
                "none";
            }}
          />
        ) : (
          <div className="no-college-image">
            🏫 College Image Not Available
          </div>
        )}

        <div className="hero-image-overlay">

          <div>

            <p className="hero-city">
              📍 {college.city}
            </p>

            <h2>
              {college.name}
            </h2>

            <p>
              🎓 {courses.join(" • ")}
            </p>

          </div>

        </div>

      </section>


      {/* =====================================
          QUICK INFORMATION
      ===================================== */}

      <section className="college-quick-info">

        <div className="quick-info-card">

          <div className="quick-icon">
            📍
          </div>

          <div>
            <span>Location</span>
            <strong>{college.city}</strong>
          </div>

        </div>


        <div className="quick-info-card">

          <div className="quick-icon">
            🎓
          </div>

          <div>
            <span>Courses</span>
            <strong>{courses.length}+ Programs</strong>
          </div>

        </div>


        <div className="quick-info-card">

          <div className="quick-icon">
            💰
          </div>

          <div>
            <span>Annual Fees</span>
            <strong>{college.fees}</strong>
          </div>

        </div>


        <div className="quick-info-card">

          <div className="quick-icon">
            📊
          </div>

          <div>
            <span>Placement</span>
            <strong>{college.placement}</strong>
          </div>

        </div>

      </section>


      {/* =====================================
          ABOUT
      ===================================== */}

      <section
        id="about"
        className="college-content-section"
      >

        <div className="section-heading">

          <span>ABOUT THE INSTITUTION</span>

          <h2>
            About {college.name}
          </h2>

        </div>

        <div className="about-content">

          <div className="about-main">

            <p>
              {college.description ||
                `${college.name} is an educational institution located in ${college.city}. Explore courses, admission information, campus facilities and placement opportunities through EduFinder.`}
            </p>

            <p>
              Students can use this page to explore
              available programs, fees, placement
              information and official college updates.
            </p>

          </div>

          <div className="about-highlight">

            <div>
              <strong>⭐ {college.rating}</strong>
              <span>Rating</span>
            </div>

            <div>
              <strong>{college.placement}</strong>
              <span>Placement</span>
            </div>

          </div>

        </div>

      </section>


      {/* =====================================
          ADMISSIONS
      ===================================== */}

      <section
        id="admissions"
        className="college-content-section light-section"
      >

        <div className="section-heading">

          <span>ADMISSION INFORMATION</span>

          <h2>
            Admissions
          </h2>

        </div>

        <div className="admission-grid">

          <div className="admission-card">

            <div className="admission-icon">
              📝
            </div>

            <h3>
              Eligibility
            </h3>

            <p>
              Eligibility requirements depend on
              the selected course and admission
              guidelines of the institution.
            </p>

          </div>


          <div className="admission-card">

            <div className="admission-icon">
              📄
            </div>

            <h3>
              Application
            </h3>

            <p>
              Students should check the official
              college website for current admission
              procedures and application dates.
            </p>

          </div>


          <div className="admission-card">

            <div className="admission-icon">
              💰
            </div>

            <h3>
              Fees
            </h3>

            <p>
              Current listed annual fee:
              <br />
              <strong>{college.fees}</strong>
            </p>

          </div>

        </div>

      </section>


      {/* =====================================
          ACADEMICS / COURSES
      ===================================== */}

      <section
        id="academics"
        className="college-content-section"
      >

        <div className="section-heading">

          <span>ACADEMIC PROGRAMS</span>

          <h2>
            Courses & Programs
          </h2>

        </div>

        <div className="course-detail-grid">

          {courses.map((course, index) => (

            <div
              className="course-detail-card"
              key={index}
            >

              <div className="course-number">
                {String(index + 1).padStart(2, "0")}
              </div>

              <div>

                <h3>
                  {course}
                </h3>

                <p>
                  Explore {course} programs,
                  academic information and
                  admission opportunities.
                </p>

              </div>

              <span className="course-arrow">
                →
              </span>

            </div>

          ))}

        </div>

      </section>


      {/* =====================================
          PLACEMENT
      ===================================== */}

      <section
        id="placement"
        className="college-content-section placement-section"
      >

        <div className="section-heading">

          <span>CAREER & PLACEMENT</span>

          <h2>
            Placement Information
          </h2>

        </div>

        <div className="placement-detail-grid">

          <div className="placement-detail-card">

            <div className="placement-detail-icon">
              📈
            </div>

            <span>
              Placement Rate
            </span>

            <strong>
              {college.placement}
            </strong>

          </div>


          <div className="placement-detail-card">

            <div className="placement-detail-icon">
              🏆
            </div>

            <span>
              Highest Package
            </span>

            <strong>
              {college.highestPackage || "N/A"}
            </strong>

          </div>


          <div className="placement-detail-card">

            <div className="placement-detail-icon">
              💼
            </div>

            <span>
              Average Package
            </span>

            <strong>
              {college.averagePackage || "N/A"}
            </strong>

          </div>

        </div>

        <div className="placement-note">

          <strong>
            💡 Career Information
          </strong>

          <p>
            Placement figures shown on EduFinder
            are provided as project data. Students
            should verify the latest placement
            statistics from the official college
            website before making decisions.
          </p>

        </div>

      </section>


      {/* =====================================
          CAMPUS LIFE
      ===================================== */}

      <section
        id="campus"
        className="college-content-section light-section"
      >

        <div className="section-heading">

          <span>STUDENT EXPERIENCE</span>

          <h2>
            Campus Life
          </h2>

        </div>

        <div className="campus-grid">

          <div className="campus-card">

            <div className="campus-card-icon">
              🏫
            </div>

            <h3>
              Campus
            </h3>

            <p>
              Explore the college campus and
              learning environment.
            </p>

          </div>


          <div className="campus-card">

            <div className="campus-card-icon">
              📚
            </div>

            <h3>
              Learning
            </h3>

            <p>
              Academic programs and learning
              opportunities for students.
            </p>

          </div>


          <div className="campus-card">

            <div className="campus-card-icon">
              👥
            </div>

            <h3>
              Student Community
            </h3>

            <p>
              Student activities, events and
              campus experiences.
            </p>

          </div>


          <div className="campus-card">

            <div className="campus-card-icon">
              💻
            </div>

            <h3>
              Facilities
            </h3>

            <p>
              Explore available academic and
              student facilities.
            </p>

          </div>

        </div>

      </section>


      {/* =====================================
          OFFICIAL WEBSITE
      ===================================== */}

      <section
        id="contact"
        className="official-college-section"
      >

        <div>

          <span>
            OFFICIAL INFORMATION
          </span>

          <h2>
            Want to know more?
          </h2>

          <p>
            Visit the official website of{" "}
            <strong>{college.name}</strong>{" "}
            for the latest admission,
            academic and placement updates.
          </p>

        </div>

        <button
          onClick={() =>
            window.open(
              college.website,
              "_blank"
            )
          }
        >
          🌐 Visit Official Website
        </button>

      </section>


      {/* =====================================
          BACK BUTTON
      ===================================== */}

      <div className="college-back-section">

        <button
          onClick={() => navigate(-1)}
        >
          ← Back to College Search
        </button>

      </div>


      {/* =====================================
          FOOTER
      ===================================== */}

      <footer className="college-detail-footer">

        <div>

          <h2>
            🎓 EduFinder
          </h2>

          <p>
            Find the right college for your
            education journey.
          </p>

        </div>

        <p>
          © 2026 EduFinder. All rights reserved.
        </p>

      </footer>

    </div>
  );
}

export default CollegeDetails;