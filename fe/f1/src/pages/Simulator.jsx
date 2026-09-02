import { useState } from "react";
import "../styles/simulator.css";

const Simulator = () => {
  const [formData, setFormData] = useState({
    race: "Monaco_Grand_Prix",
    driver: "LEC",
    lap_number: 25,
    position: 3,
    compound: "HARD",
    tyre_age: 3,
    fresh_tyre: false,
    safety_car_active: false,
    vsc_active: false,
    yellow_flag: false,
    red_flag_active: false,
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const runSimulation = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/simulate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...formData,
          lap_number: Number(formData.lap_number),
          position: Number(formData.position),
          tyre_age: Number(formData.tyre_age),
        }),
      });

      if (!response.ok) {
        throw new Error("Simulation request failed.");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(
        "Unable to connect to the strategy engine. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="simulator-page">
      <section className="simulator-hero">
        <div className="simulator-hero__content">
          <p className="simulator-eyebrow">F1 STRATEGIST / SIMULATOR</p>

          <h1>
            Make the call.
            <br />
            <span>Before the pit wall does.</span>
          </h1>

          <p className="simulator-hero__description">
            Enter a race situation and let the strategy engine predict when
            the driver should make their next pit stop.
          </p>
        </div>
      </section>

      <section className="simulator-workspace">
        <div className="simulator-panel simulator-panel--inputs">
          <div className="panel-heading">
            <div>
              <p className="panel-label">01 / RACE STATE</p>
              <h2>Configure the situation</h2>
            </div>
          </div>

          <form onSubmit={runSimulation}>
            <div className="form-section">
              <h3>Race Information</h3>

              <div className="form-grid">
                <label>
                  <span>Race</span>
                  <select
                    name="race"
                    value={formData.race}
                    onChange={handleChange}
                  >
                    <option value="Monaco_Grand_Prix">
                      Monaco Grand Prix
                    </option>
                  </select>
                </label>

                <label>
                  <span>Driver</span>
                  <select
                    name="driver"
                    value={formData.driver}
                    onChange={handleChange}
                  >
                    <option value="LEC">Charles Leclerc</option>
                  </select>
                </label>
              </div>

              <div className="form-grid">
                <label>
                  <span>Current Lap</span>
                  <input
                    type="number"
                    name="lap_number"
                    min="1"
                    value={formData.lap_number}
                    onChange={handleChange}
                  />
                </label>

                <label>
                  <span>Position</span>
                  <input
                    type="number"
                    name="position"
                    min="1"
                    value={formData.position}
                    onChange={handleChange}
                  />
                </label>
              </div>
            </div>

            <div className="form-section">
              <h3>Tyre State</h3>

              <div className="form-grid">
                <label>
                  <span>Compound</span>
                  <select
                    name="compound"
                    value={formData.compound}
                    onChange={handleChange}
                  >
                    <option value="SOFT">Soft</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="HARD">Hard</option>
                  </select>
                </label>

                <label>
                  <span>Tyre Age</span>
                  <input
                    type="number"
                    name="tyre_age"
                    min="0"
                    value={formData.tyre_age}
                    onChange={handleChange}
                  />
                </label>
              </div>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  name="fresh_tyre"
                  checked={formData.fresh_tyre}
                  onChange={handleChange}
                />
                <span>Fresh tyre</span>
              </label>
            </div>

            <div className="form-section">
              <h3>Race Conditions</h3>

              <div className="condition-grid">
                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    name="safety_car_active"
                    checked={formData.safety_car_active}
                    onChange={handleChange}
                  />
                  <span>Safety Car</span>
                </label>

                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    name="vsc_active"
                    checked={formData.vsc_active}
                    onChange={handleChange}
                  />
                  <span>Virtual Safety Car</span>
                </label>

                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    name="yellow_flag"
                    checked={formData.yellow_flag}
                    onChange={handleChange}
                  />
                  <span>Yellow Flag</span>
                </label>

                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    name="red_flag_active"
                    checked={formData.red_flag_active}
                    onChange={handleChange}
                  />
                  <span>Red Flag</span>
                </label>
              </div>
            </div>

            <button
              className="simulate-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "RUNNING SIMULATION..." : "RUN STRATEGY ENGINE"}
            </button>
          </form>
        </div>

        <div className="simulator-panel simulator-panel--result">
          <div className="panel-heading">
            <div>
              <p className="panel-label">02 / STRATEGY ENGINE</p>
              <h2>Prediction</h2>
            </div>
          </div>

          {!result && !loading && !error && (
            <div className="result-empty">
              <div className="result-empty__number">01</div>
              <h3>Awaiting race scenario</h3>
              <p>
                Configure the race state and run the strategy engine to see
                the predicted pit window.
              </p>
            </div>
          )}

          {loading && (
            <div className="result-empty">
              <div className="loading-indicator">CALCULATING</div>
              <h3>Running the model...</h3>
              <p>
                Preparing the race state and passing it through the prediction
                pipeline.
              </p>
            </div>
          )}

          {error && (
            <div className="result-error">
              <p className="panel-label">ENGINE ERROR</p>
              <h3>Could not run simulation</h3>
              <p>{error}</p>
            </div>
          )}

          {result && (
            <div className="result-content">
              <p className="result-label">PREDICTED PIT LAP</p>

              <div className="pit-lap">
                <span>Lap</span>
                <strong>{result.predicted_pit_lap}</strong>
              </div>

              <div className="result-stats">
                <div>
                  <span>Current Lap</span>
                  <strong>{result.current_lap}</strong>
                </div>

                <div>
                  <span>Laps Until Pit</span>
                  <strong>{result.laps_until_pit}</strong>
                </div>
              </div>

              <div className="strategy-message">
                <p>
                  Based on the supplied race state, the model predicts the
                  next pit stop around lap{" "}
                  <strong>{result.predicted_pit_lap}</strong>.
                </p>
              </div>
            </div>
          )}
        </div>
      </section>

      <section className="simulator-process">
        <div className="process-heading">
          <p className="panel-label">03 / UNDER THE HOOD</p>
          <h2>What happens when you run it?</h2>
        </div>

        <div className="process-grid">
          <div className="process-step">
            <span>01</span>
            <h3>Race State</h3>
            <p>
              Your inputs describe the current race, driver, tyres, position,
              and track conditions.
            </p>
          </div>

          <div className="process-step">
            <span>02</span>
            <h3>Feature Preparation</h3>
            <p>
              FastAPI combines your inputs with the historical race state
              required by the model.
            </p>
          </div>

          <div className="process-step">
            <span>03</span>
            <h3>Random Forest</h3>
            <p>
              The trained regression model processes the 35 race strategy
              features.
            </p>
          </div>

          <div className="process-step">
            <span>04</span>
            <h3>Strategy Decision</h3>
            <p>
              The prediction is returned to React and converted into a
              readable pit-stop recommendation.
            </p>
          </div>
        </div>
      </section>

      <section className="simulator-limitations">
        <p className="panel-label">CURRENT MODEL</p>

        <h2>What the model predicts</h2>

        <p>
          The current strategy engine predicts <strong>laps until the next
          pit stop</strong>. Tire selection, number of stops, expected race
          finish, and complete multi-stop strategy are planned as future
          extensions.
        </p>
      </section>
    </main>
  );
};

export default Simulator;
