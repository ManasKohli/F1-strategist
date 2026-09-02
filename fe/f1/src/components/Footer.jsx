import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer__content">

        <div className="footer__brand">
          <p>F1 STRATEGIST</p>
          <span>Machine Learning for Race Strategy</span>
        </div>

        <nav className="footer__links" aria-label="Footer navigation">
          <a
            href="https://github.com/ManasKohli/F1-strategist"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>

          <Link to="/simulator">
            Simulator
          </Link>

          <Link to="/model">
            Model
          </Link>
        </nav>

      </div>
    </footer>
  );
};

export default Footer;