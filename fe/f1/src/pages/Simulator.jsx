import { useEffect, useState } from "react";

import SimulatorHero from "../components/simulator/SimulatorHero";
import RaceStateForm from "../components/simulator/RaceStateForm";
import driverDirectory from "../components/simulator/driverDirectory";
import TyreStateForm from "../components/simulator/TyreStateForm";
import RaceConditions from "../components/simulator/RaceConditions";
import WeatherConditions from "../components/simulator/WeatherConditions";
import SimulationButton from "../components/simulator/SimulationButton";
import StrategyResult from "../components/simulator/StrategyResult";


import "../styles/simulator.css";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const Simulator = () => {
  const [formData, setFormData] = useState({
    race: "Monaco_Grand_Prix",
    driver: "LEC",
    lap_number: 25,
    position: 3,
    compound: "HARD",
    tyre_age: 3,
    fresh_tyre: false,
    race_condition: "",
    rain_condition: "",
  });

  const [result, setResult] = useState(null);
  const [resultFormData, setResultFormData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [availableDrivers, setAvailableDrivers] = useState(driverDirectory);

  useEffect(() => {
    const loadDrivers = async () => {
      const lapNumber = Number(formData.lap_number);
      const lapQuery = Number.isInteger(lapNumber) && lapNumber > 0
        ? `&lap_number=${lapNumber}`
        : "";

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/drivers?race=${encodeURIComponent(formData.race)}${lapQuery}`
        );
        if (!response.ok) return;

        const data = await response.json();
        const driverCodes = new Set(data.drivers);
        const driversForRace = driverDirectory.filter(([code]) => driverCodes.has(code));

        setAvailableDrivers(driversForRace);
        if (!driverCodes.has(formData.driver) && driversForRace.length > 0) {
          setFormData((previous) => ({
            ...previous,
            driver: driversForRace[0][0],
          }));
        }
      } catch {
        // Keep the local directory available while the backend is offline.
      }
    };

    loadDrivers();
  }, [formData.driver, formData.race, formData.lap_number]);

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
    setResultFormData({ ...formData });

    const raceCondition = formData.race_condition;

    try {
      const response = await fetch(`${API_BASE_URL}/api/simulate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          race: formData.race,
          driver: formData.driver,
          lap_number: Number(formData.lap_number),
          position: Number(formData.position),
          compound: formData.compound,
          tyre_age: Number(formData.tyre_age),
          fresh_tyre: formData.fresh_tyre,
          rain_condition: formData.rain_condition,
          safety_car_active: raceCondition === "safety_car_active",
          vsc_active: raceCondition === "vsc_active",
          yellow_flag: raceCondition === "yellow_flag",
          red_flag_active: raceCondition === "red_flag_active",
        }),
      });

      if (!response.ok) {
        const responseError = await response.json().catch(() => null);
        throw new Error(responseError?.detail || "Simulation request failed.");
      }

      const data = await response.json();

      setResult(data);
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to connect to the strategy engine. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="simulator-page">
      <SimulatorHero />

      <section className="simulator-workspace">
        <div className="simulator-panel simulator-panel--inputs">

          <div className="panel-heading">
            <p className="panel-label">01 / RACE STATE</p>
            <h2>Configure the situation</h2>
          </div>

          <form onSubmit={runSimulation}>

            <RaceStateForm
              formData={formData}
              onChange={handleChange}
              availableDrivers={availableDrivers}
            />

            <TyreStateForm
              formData={formData}
              onChange={handleChange}
            />

            <RaceConditions
              formData={formData}
              onChange={handleChange}
            />

            <WeatherConditions
              formData={formData}
              onChange={handleChange}
            />

            <SimulationButton loading={loading} disabled={availableDrivers.length === 0} />

            {availableDrivers.length === 0 && (
              <p className="form-help form-help--error">
                No drivers are available for this race state. Try another lap or race.
              </p>
            )}

          </form>
        </div>

        <div className="simulator-panel simulator-panel--results">
          <StrategyResult
            result={result}
            formData={resultFormData}
            loading={loading}
            error={error}
          />
        </div>
      </section>
      
    </main>
  );
};

 export default Simulator;