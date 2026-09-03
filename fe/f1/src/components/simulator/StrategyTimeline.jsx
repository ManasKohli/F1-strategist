const StrategyTimeline = ({
  currentLap,
  predictedPitLap,
  selectedPitLap = predictedPitLap,
  totalLaps = 78,
}) => {
  const progress = Math.min(100, Math.max(0, (currentLap / totalLaps) * 100));
  const pitProgress = Math.min(100, Math.max(0, (selectedPitLap / totalLaps) * 100));
  const windowStart = Math.max(currentLap, predictedPitLap - 2);
  const windowEnd = Math.min(totalLaps, predictedPitLap + 2);
  const windowStartProgress = (windowStart / totalLaps) * 100;
  const windowWidth = ((windowEnd - windowStart) / totalLaps) * 100;

  const lapsUntilPit = selectedPitLap - currentLap;
  const currentLabelClass = progress < 18
    ? "timeline-marker-label--start"
    : progress > 82
      ? "timeline-marker-label--finish"
      : "";
  const pitLabelClass = Math.abs(pitProgress - progress) < 12
    ? "timeline-marker-label--lower"
    : "";

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
          <span className={`timeline-marker-label ${currentLabelClass}`}>
            CURRENT LAP {currentLap}
          </span>

          <span className="timeline-marker timeline-marker--current" />
        </div>

        <div
          className="timeline-pit"
          style={{ left: `${pitProgress}%` }}
        >
          <span className={`timeline-marker-label ${pitLabelClass}`}>
            PIT {selectedPitLap}
          </span>

          <span className="timeline-marker timeline-marker--pit" />
        </div>

        <div
          className="timeline-window"
          style={{ left: `${windowStartProgress}%`, width: `${windowWidth}%` }}
        />

        <div
          className="timeline-progress"
          style={{ width: `${pitProgress}%` }}
        />

      </div>

      <div className="timeline-distance">
        <span>{windowStart}–{windowEnd}</span>
        <strong>OPTIMAL WINDOW</strong>
        <span>{lapsUntilPit} laps to selected pit</span>
      </div>

    </div>
  );
};

export default StrategyTimeline;