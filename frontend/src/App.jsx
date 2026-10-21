import "./App.css";
import { Routes, Route } from "react-router-dom";
import EducationLevels from "./page/EducationLevels";
import Navbar from "./components/Navbar";
import Home from "./page/Home";
import CollegeDetails from "./page/CollegeDetails";
import Contact from "./page/Contact";
import About from "./page/About";
import Courses from "./page/Courses";
import Admin from "./page/Admin";
import FindCollege from "./page/FindCollege";

function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />

        {/* AI College Decision Assistant */}
        <Route path="/find-college" element={<FindCollege />} />

        <Route path="/college/:id" element={<CollegeDetails />} />

        <Route path="/contact" element={<Contact />} />

        <Route path="/about" element={<About />} />

        <Route path="/courses" element={<Courses />} />

      
<Route path="/education" element={<EducationLevels />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </>
  );
}

export default App;