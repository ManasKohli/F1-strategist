const SimulationButton = ({ loading }) => {
  return (
    <button
      className="simulate-button"
      type="submit"
      disabled={loading}
    >
      {loading ? "RUNNING SIMULATION..." : "RUN STRATEGY ENGINE"}
    </button>
  );
};

export default SimulationButton;