const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer__content">
                <div className="footer__brand">
                    <p>F1 STRATEGIST</p>
                    <span>Machine Learning for Race Strategy</span>
                </div>

                <nav className="footer__links" aria-label="Footer navigation">
                    <a href="#">GitHub</a>
                    <a href="#simulator">Simulator</a>
                    <a href="#">Model</a>
                </nav>
            </div>
        </footer>
    );
};

export default Footer;
