const Navbar = () => {
    return (
        <nav className="navbar" aria-label="Main navigation">
            <div className="navbar__brand">
                <a href="#top" className="navbar__brand-link">F1 STRATEGIST</a>
            </div>

            <div className="navbar__nav" aria-label="Primary navigation">
                <a href="#project">PROJECT</a>
                <a href="#simulator">SIMULATOR</a>
                <a href="#model">MODEL</a>
            </div>

            <div className="navbar__actions">
                <a href="https://github.com/" className="navbar__github" target="_blank" rel="noreferrer">
                    GitHub
                </a>
                <a href="#simulator" className="navbar__cta">
                    TRY IT
                </a>
            </div>
        </nav>
    );
};

export default Navbar;