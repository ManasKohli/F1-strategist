const ModelStatus = () => {
  const details = [
    ["Model", "Random Forest Regression"],
    ["Target", "Laps Until Pit"],
    ["Features", "35 race strategy features"],
    ["Status", "Ready"],
  ];

  return (
    <footer className="model-status">
      {details.map(([label, value]) => (
        <div key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </footer>
  );
};

export default ModelStatus;
