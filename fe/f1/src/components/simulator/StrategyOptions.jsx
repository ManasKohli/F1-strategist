const StrategyOptions = ({ strategies, selectedId, onSelect }) => {
  const selectedStrategy = strategies.find((strategy) => strategy.id === selectedId);

  return (
    <section className="strategy-section strategy-options" aria-labelledby="strategy-options-title">
      <div className="section-heading-row">
        <div>
          <p className="result-label">STRATEGY OPTIONS</p>
          <h3 id="strategy-options-title">Alternative strategies</h3>
        </div>
        <p className="mock-note">FRONTEND MOCK DATA</p>
      </div>

      <div className="strategy-options__grid">
        {strategies.map((strategy) => (
          <button
            className={`strategy-option ${selectedId === strategy.id ? "is-selected" : ""}`}
            key={strategy.id}
            type="button"
            onClick={() => onSelect(strategy.id)}
            aria-pressed={selectedId === strategy.id}
          >
            <span className="strategy-option__topline">
              <strong>{strategy.code}</strong>
              <span>{strategy.risk} RISK</span>
            </span>
            <span className="strategy-option__name">{strategy.name}</span>
            <span className="strategy-option__lap">PIT LAP {strategy.pitLap}</span>
            <span className="strategy-option__tyres">{strategy.tyreChange}</span>
            <span className="strategy-option__description">{strategy.description}</span>
          </button>
        ))}
      </div>

      <div className="selected-strategy-note">
        <span>SELECTED CALL</span>
        <p>{selectedStrategy.description}</p>
      </div>
    </section>
  );
};

export default StrategyOptions;
