import React from "react";

function CollegeCard({
  college,
  favorites = [],
  toggleFavorite,
  compareColleges = [],
  toggleCompare,
}) {
  // ================= FAVORITE =================
  const isFavorite = favorites.includes(college?._id);

  // ================= COMPARE =================
  const isCompared =
    Array.isArray(compareColleges) &&
    compareColleges.some(
      (item) => item?._id === college?._id
    );

  // ================= WEBSITE =================
  const website = college?.website
    ? college.website.startsWith("http")
      ? college.website
      : `https://${college.website}`
    : null;

  // ================= COURSES =================
  let detectedCourses = "Course information not available";

  if (Array.isArray(college?.courses) && college.courses.length > 0) {
    detectedCourses = college.courses.join(", ");
  }

  return (
    <div className="college-card">

      {/* ================= FAVORITE BUTTON ================= */}
      <button
        type="button"
        className="favorite-btn"
        onClick={() => toggleFavorite(college._id)}
        aria-label="Add to favorites"
      >
        {isFavorite ? "❤️" : "♡"}
      </button>


      {/* ================= COLLEGE IMAGE ================= */}
      {college?.image ? (
        <img
          src={college.image}
          alt={college.name || "College"}
          className="college-image"
          onError={(e) => {
            e.currentTarget.style.display = "none";
          }}
        />
      ) : (
        <div className="college-image-placeholder">
          🏫
        </div>
      )}


      {/* ================= COLLEGE INFORMATION ================= */}
      <div className="college-card-content">

        {/* College Name */}
        <h3>
          {college?.name || "College Name"}
        </h3>


        {/* City */}
        <p>
          📍{" "}
          <strong>
            {college?.city || "City not available"}
          </strong>
        </p>


        {/* Automatically Detected Courses */}
        <p>
          🎓 <strong>Courses:</strong>{" "}
          {detectedCourses}
        </p>


        {/* ================= ACTION BUTTONS ================= */}
        <div className="college-card-actions">

          {/* Compare */}
          <button
            type="button"
            className="compare-btn"
            onClick={() => toggleCompare(college)}
          >
            {isCompared
              ? "✓ Compared"
              : "⚖ Compare"}
          </button>


          {/* Official Website */}
          {website && (
            <a
              href={website}
              target="_blank"
              rel="noopener noreferrer"
              className="view-details-btn"
            >
              View Official Website →
            </a>
          )}

        </div>

      </div>

    </div>
  );
}

export default CollegeCard;