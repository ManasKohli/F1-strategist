const ProjectedOutcome = ({
  currentPosition,
  projectedFinish,
  positionDelta,
  timeToLeader,
}) => {
  const deltaLabel = positionDelta > 0 ? `+${positionDelta}` : positionDelta;

  return (
    <section className="strategy-section projected-outcome">
      <p className="result-label">PROJECTED RACE OUTCOME</p>
      <div className="outcome-grid">
        <div>
          <span>Current Position</span>
          <strong>P{currentPosition}</strong>
        </div>
        <div>
          <span>Projected Finish</span>
          <strong>P{projectedFinish}</strong>
        </div>
        <div>
          <span>Position Delta</span>
          <strong>{deltaLabel}</strong>
        </div>
        <div>
          <span>Time To Leader</span>
          <strong>{timeToLeader}</strong>
        </div>
      </div>
      <p className="mock-note">FRONTEND MOCK DATA</p>
    </section>
  );
};

export default ProjectedOutcome;
