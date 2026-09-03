const StrategyTimeline = ({
  currentLap,
  predictedPitLap,
  totalLaps = 78,
}) => {
  const progress = (currentLap / totalLaps) * 100;
  const pitProgress = (predictedPitLap / totalLaps) * 100;

  const lapsUntilPit = predictedPitLap - currentLap;

  return (
    <div className="strategy-timeline">

      <div className="timeline-labels">
        <span>START</span>
        <span>FINISH</span>
      </div>

      <div className="timeline-track">

        <div
          className="timeline-current"
          style={{ left: `${progress}%` }}
        >
          <span className="timeline-marker-label">
            LAP {currentLap}
          </span>

          <span className="timeline-marker timeline-marker--current" />
        </div>

        <div
          className="timeline-pit"
          style={{ left: `${pitProgress}%` }}
        >
          <span className="timeline-marker-label">
            PIT {predictedPitLap}
          </span>

          <span className="timeline-marker timeline-marker--pit" />
        </div>

        <div
          className="timeline-progress"
          style={{ width: `${pitProgress}%` }}
        />

      </div>

      <div className="timeline-distance">
        <span>
          {lapsUntilPit} laps until predicted pit
        </span>
      </div>

    </div>
  );
};

export default StrategyTimeline;