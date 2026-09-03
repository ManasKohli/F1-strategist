const StrategyMetrics = ({ pitLap, lapsUntilPit, formData }) => {
  const metrics = [
    ["Pit Lap", pitLap],
    ["Laps To Pit", lapsUntilPit],
    ["Current Position", `P${formData.position}`],
    ["Tyre Age", formData.tyre_age],
  ];

  return (
    <section className="strategy-metrics" aria-label="Strategy metrics">
      {metrics.map(([label, value]) => (
        <div className="strategy-metric" key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </section>
  );
};

export default StrategyMetrics;
