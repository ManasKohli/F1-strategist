const ProjectOverview = () => {
    return (
        <section className="project-overview">
            <div className="project-overview__content">

                <p className="section-label">THE PROJECT</p>

                <h2>
                    Smarter Decisions.
                    Better Strategy.
                </h2>

                <p>
                    F1 Strategist uses historical race data,
                    driver performance, tire degradation,
                    weather, and race conditions to predict
                    optimal race strategy.
                </p>

                <div className="project-cards">

                    <div className="project-card">
                        <span className="project-card__number">01</span>
                        <h3>DATA</h3>
                        <p>
                            Historical race and race-condition data used as inputs.
                        </p>

                        <ul className="project-card__list">
                            <li>Historical lap times</li>
                            <li>Tire compounds and stint data</li>
                            <li>Driver performance</li>
                            <li>Weather</li>
                            <li>Track and race conditions</li>
                        </ul>
                    </div>

                    <div className="project-card">
                        <span className="project-card__number">02</span>
                        <h3>ML MODEL</h3>
                        <p>
                            The machine learning model analyzes the input data and learns patterns to predict race performance and evaluate strategy scenarios.
                        </p>

                        <ul className="project-card__list">
                            <li>Feature extraction</li>
                            <li>Model predictions</li>
                            <li>Performance patterns</li>
                            <li>Strategy evaluation</li>
                        </ul>
                    </div>

                    <div className="project-card">
                        <span className="project-card__number">03</span>
                        <h3>STRATEGY</h3>
                        <p>
                            The model's predictions are used to recommend the most effective race strategy.
                        </p>

                        <ul className="project-card__list">
                            <li>Optimal pit-stop window</li>
                            <li>Tire compound selection</li>
                            <li>Number of stops</li>
                            <li>Expected race outcome</li>
                            <li>Strategy recommendation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    )
};

export default ProjectOverview;