const StrategyExplanation = ({ formData }) => {
  const conditionLabels = {
    safety_car_active: "Safety Car",
    vsc_active: "VSC",
    yellow_flag: "Yellow Flag",
    red_flag_active: "Red Flag",
  };
  const raceCondition = conditionLabels[formData.race_condition] || "No Safety Car or VSC currently active";

  return (
    <section className="strategy-section strategy-explanation" aria-labelledby="strategy-explanation-title">
      <p className="result-label">WHY THIS CALL?</p>
      <h3 id="strategy-explanation-title">The race state points to a measured stop.</h3>
      <div className="explanation-grid">
        <div>
          <span>Tyre Age</span>
          <p>Current {formData.compound} tyre has completed {formData.tyre_age} laps.</p>
        </div>
        <div>
          <span>Race Position</span>
          <p>Driver is currently running P{formData.position}.</p>
        </div>
        <div>
          <span>Race Conditions</span>
          <p>{raceCondition}.</p>
        </div>
      </div>
    </section>
  );
};

export default StrategyExplanation;
