function Courses() {
  const courses = [
    "B.Tech",
    "BCA",
    "MCA",
    "MBA",
    "B.Sc",
    "M.Tech",
  ];

  return (
    <div style={{ padding: "40px" }}>
      <h1>Our Courses</h1>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        {courses.map((course) => (
          <div
            key={course}
            style={{
              width: "220px",
              padding: "20px",
              borderRadius: "12px",
              background: "#fff",
              boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
              textAlign: "center",
            }}
          >
            <h3>{course}</h3>
            <p>Explore top colleges for {course}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Courses;