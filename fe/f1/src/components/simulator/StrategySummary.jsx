const StrategySummary = ({ pitLap, lapsUntilPit, formData }) => {
  return (
    <section className="strategy-summary" aria-labelledby="strategy-summary-title">
      <p className="result-label">STRATEGY RECOMMENDATION</p>
      <h2 id="strategy-summary-title">Pit window</h2>
      <div className="strategy-summary__lap">
        <span>LAP</span>
        <strong>{pitLap}</strong>
      </div>
      <p className="strategy-summary__distance">{lapsUntilPit} LAPS TO PIT</p>
      <p className="strategy-summary__call">
        Continue the current {formData.compound} tyre stint and target a pit
        stop around Lap {pitLap}.
      </p>
    </section>
  );
};

export default StrategySummary;
