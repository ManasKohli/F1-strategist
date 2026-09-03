import { Link } from "react-router-dom";

const FinalCta = () => {
    return (
        <section className="final-cta" id="simulator">
            <div className="final-cta__content">
                <div className="final-cta__copy">
                    <p className="section-label final-cta__label">READY TO TEST THE STRATEGY?</p>

                    <h2>Put the model to the test.</h2>

                    <p>
                        Simulate a race and see how different conditions affect the
                        optimal strategy.
                    </p>
                </div>

                <Link to="/simulator" className="final-cta__link">
                    Try Simulator →
                </Link>
            </div>
        </section>
    );
};

export default FinalCta;
