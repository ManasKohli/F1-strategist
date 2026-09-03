import StrategyTimeline from "./StrategyTimeline";

const StrategyResult = ({ result, formData, loading, error }) => {
  if (loading) {
    return (
      <div className="result-empty">
        <div className="loading-indicator">CALCULATING</div>
        <h3>Running the model...</h3>
        <p>Preparing the race state and passing it through the prediction pipeline.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-error">
        <p className="panel-label">ENGINE ERROR</p>
        <h3>Could not run simulation</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!result || !formData) {
    return (
      <div className="result-empty">
        <div className="loading-indicator">STRATEGY ENGINE</div>
        <h3>Ready for a race state</h3>
        <p>Submit the configuration to view the model's pit-stop prediction.</p>
      </div>
    );
  }

  const simulationResult = result;
  return (
    <div className="strategy-result">
      <div className="result-header">
        <div>
          <p className="panel-label">02 / STRATEGY ENGINE</p>
          <h2>Prediction</h2>
        </div>
        <div className="result-status">MODEL READY</div>
      </div>

      <div className="prediction-block">
        <p className="result-label">PREDICTED PIT LAP</p>
        <div className="pit-lap">
          <span>Lap</span>
          <strong>{simulationResult.predicted_pit_lap}</strong>
        </div>
      </div>

      <StrategyTimeline
        currentLap={simulationResult.current_lap}
        predictedPitLap={simulationResult.predicted_pit_lap}
        totalLaps={78}
      />

      <div className="result-stats">
        <div>
          <span>Current Lap</span>
          <strong>{simulationResult.current_lap}</strong>
        </div>
        <div>
          <span>Laps Until Pit</span>
          <strong>{simulationResult.laps_until_pit}</strong>
        </div>
        <div>
          <span>Position</span>
          <strong>P{formData.position}</strong>
        </div>
        <div>
          <span>Tyre Age</span>
          <strong>{formData.tyre_age}</strong>
        </div>
      </div>

      <div className="strategy-message">
        <p className="panel-label">STRATEGY CALL</p>
        <h3>PIT AROUND LAP {simulationResult.predicted_pit_lap}</h3>
        <p>
          The model predicts the next pit stop in approximately {" "}
          <strong>{simulationResult.laps_until_pit}</strong> laps.
        </p>
      </div>
    </div>
  );
};

export default StrategyResult;