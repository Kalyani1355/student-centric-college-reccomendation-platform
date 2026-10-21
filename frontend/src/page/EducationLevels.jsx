import { useNavigate } from "react-router-dom";
import "../App.css";

function EducationLevels() {
  const navigate = useNavigate();

  return (
    <div className="education-page">

      {/* PAGE HEADER */}
      <div className="education-header">
        <h1>Find Your College</h1>
        <p>
          Choose your education level to explore courses and colleges.
        </p>
      </div>

      {/* EDUCATION LEVELS */}
      <div className="education-container">

        {/* GRADUATION */}
        <div
          className="education-card"
          onClick={() => navigate("/graduation")}
        >
          <div className="education-icon">
            🎓
          </div>

          <h2>Graduation</h2>

          <p>
            Explore undergraduate courses and colleges.
          </p>

          <button>
            Explore Graduation
          </button>
        </div>


        {/* POST GRADUATION */}
        <div
          className="education-card"
          onClick={() => navigate("/post-graduation")}
        >
          <div className="education-icon">
            🎓
          </div>

          <h2>Post Graduation</h2>

          <p>
            Explore postgraduate courses and colleges.
          </p>

          <button>
            Explore Post Graduation
          </button>
        </div>


        {/* PHD */}
        <div
          className="education-card"
          onClick={() => navigate("/phd")}
        >
          <div className="education-icon">
            🔬
          </div>

          <h2>PhD</h2>

          <p>
            Explore doctoral programs and research colleges.
          </p>

          <button>
            Explore PhD
          </button>
        </div>

      </div>

    </div>
  );
}

export default EducationLevels;