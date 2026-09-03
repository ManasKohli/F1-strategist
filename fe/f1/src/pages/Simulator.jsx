import { useState } from "react";

import SimulatorHero from "../components/simulator/SimulatorHero";
import RaceStateForm from "../components/simulator/RaceStateForm";
import TyreStateForm from "../components/simulator/TyreStateForm";
import RaceConditions from "../components/simulator/RaceConditions";
import WeatherConditions from "../components/simulator/WeatherConditions";
import SimulationButton from "../components/simulator/SimulationButton";
import StrategyResult from "../components/simulator/StrategyResult";
import StrategyTimeline from "../components/simulator/StrategyTimeline";

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
    race_condition: "",
    rain_condition: "",
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

    const raceCondition = formData.race_condition;

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
          rainfall: formData.rain_condition !== "",
          safety_car_active: raceCondition === "safety_car_active",
          vsc_active: raceCondition === "vsc_active",
          yellow_flag: raceCondition === "yellow_flag",
          red_flag_active: raceCondition === "red_flag_active",
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

            <SimulationButton loading={loading} />

          </form>
        </div>

        <div className="simulator-panel simulator-panel--results">
          <StrategyResult result={result} formData={formData} loading={loading} error={error}/>
        </div>
      </section>
      
    </main>
  );
};

 export default Simulator;