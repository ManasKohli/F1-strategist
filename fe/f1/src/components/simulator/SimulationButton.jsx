const SimulationButton = ({ loading, disabled = false }) => {
  return (
    <button
      className="simulate-button"
      type="submit"
      disabled={loading || disabled}
    >
      {loading ? "RUNNING SIMULATION..." : "RUN STRATEGY ENGINE"}
    </button>
  );
};

export default SimulationButton;