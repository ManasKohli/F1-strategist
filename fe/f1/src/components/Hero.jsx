import TeamCarousel from "./TeamCarousel";

const Hero = () => {
    return (
        <section className="hero">
            <div className="hero__content">
                <div className="hero__copy">
                    <p>F1 Strategist</p>

                    <h1>
                        Machine Learning for Race Strategy
                    </h1>

                    <p>
                        Predict optimal pit-stop timing using historical
                        race data, driver performance, tire degradation,
                        weather, and race conditions.
                    </p>

                    <a href="#simulator">
                        Try Simulator
                    </a>
                </div>

                <TeamCarousel />
            </div>
        </section>
    );
};

export default Hero;