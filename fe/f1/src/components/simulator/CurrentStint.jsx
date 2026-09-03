const CurrentStint = ({ formData }) => {
  const tyreHealth = Math.max(18, 100 - Number(formData.tyre_age) * 7);

  return (
    <section className="strategy-section current-stint" aria-labelledby="current-stint-title">
      <div className="section-heading-row">
        <div>
          <p className="result-label">CURRENT STINT</p>
          <h3 id="current-stint-title">{formData.compound}</h3>
        </div>
        <strong className="stint-laps">{formData.tyre_age} LAPS</strong>
      </div>
      <div className="stint-status-row">
        <span>STINT STATUS</span>
        <strong>HEALTHY</strong>
      </div>
      <div className="degradation-bar" aria-label="Visual tyre degradation indicator">
        <span style={{ width: `${tyreHealth}%` }} />
      </div>
      <p className="mock-note">VISUAL REPRESENTATION ONLY</p>
    </section>
  );
};

export default CurrentStint;
