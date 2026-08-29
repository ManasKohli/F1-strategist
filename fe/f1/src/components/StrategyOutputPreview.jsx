const StrategyOutputPreview = () => {
    return (
        <section className="strategy-output" id="strategy-output">
            <div className="strategy-output__content">
                <p className="section-label">THE OUTPUT</p>

                <h2>
                    From prediction to race strategy.
                </h2>

                <p className="strategy-output__description">
                    The model evaluates the current race state and identifies the
                    strategy with the highest expected performance.
                </p>

                <div className="strategy-dashboard">
                    <div className="strategy-dashboard__header">
                        <span className="strategy-dashboard__title">RACE STRATEGY</span>
                        <span className="strategy-dashboard__lap">LAP 42 / 70</span>
                    </div>

                    <div className="strategy-dashboard__grid">
                        <div className="strategy-dashboard__stats">
                            <div className="strategy-stat">
                                <span>Driver</span>
                                <strong>Lando Norris</strong>
                            </div>

                            <div className="strategy-stat">
                                <span>Position</span>
                                <strong>P3</strong>
                            </div>

                            <div className="strategy-stat">
                                <span>Tyre</span>
                                <strong>Medium</strong>
                            </div>

                            <div className="strategy-stat">
                                <span>Tyre Age</span>
                                <strong>18 Laps</strong>
                            </div>
                        </div>

                        <div className="strategy-dashboard__recommendation">
                            <p className="strategy-dashboard__recommendation-header">
                                Recommended Strategy
                            </p>

                            <div className="strategy-recommendation__row">
                                <span>Pit Window</span>
                                <strong>LAP 47–49</strong>
                            </div>

                            <div className="strategy-recommendation__row">
                                <span>Next Tyre</span>
                                <strong>Hard</strong>
                            </div>

                            <div className="strategy-recommendation__row">
                                <span>Stops</span>
                                <strong>1</strong>
                            </div>

                            <div className="strategy-recommendation__row">
                                <span>Expected Result</span>
                                <strong>P2</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default StrategyOutputPreview;
