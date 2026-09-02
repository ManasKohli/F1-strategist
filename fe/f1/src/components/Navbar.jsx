import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar" aria-label="Main navigation">

      <div className="navbar__brand">
        <Link to="/project" className="navbar__brand-link">
          F1 STRATEGIST
        </Link>
      </div>

      <div className="navbar__nav" aria-label="Primary navigation">
        <Link to="/project">PROJECT</Link>
        <Link to="/simulator">SIMULATOR</Link>
        <Link to="/model">MODEL</Link>
      </div>

      <div className="navbar__actions">

        <a
          href="https://github.com/ManasKohli/F1-strategist"
          className="navbar__github"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>

        <Link to="/simulator" className="navbar__cta">
          TRY IT
        </Link>

      </div>

    </nav>
  );
};

export default Navbar;