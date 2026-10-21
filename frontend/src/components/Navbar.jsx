import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>🎓 EduFinder</h2>

      <ul>
        {/* Home */}
        <li>
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "active-link" : ""
            }
          >
            Home
          </NavLink>
        </li>

        {/* Find My College */}
        <li>
          <NavLink
            to="/find-college"
            className={({ isActive }) =>
              isActive ? "active-link" : ""
            }
          >
            🤖 Find My College
          </NavLink>
        </li>

        {/* Courses */}
        <li>
          <NavLink
            to="/courses"
            className={({ isActive }) =>
              isActive ? "active-link" : ""
            }
          >
            Courses
          </NavLink>
        </li>

        {/* About */}
        <li>
          <NavLink
            to="/about"
            className={({ isActive }) =>
              isActive ? "active-link" : ""
            }
          >
            About
          </NavLink>
        </li>

        {/* Contact */}
        <li>
          <NavLink
            to="/contact"
            className={({ isActive }) =>
              isActive ? "active-link" : ""
            }
          >
            Contact
          </NavLink>
        </li>
      </ul>

      
    </nav>
  );
}

export default Navbar;