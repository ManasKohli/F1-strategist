import driverDirectory from "./driverDirectory";

const races = [
  ["Abu_Dhabi_Grand_Prix", "Abu Dhabi Grand Prix"],
  ["Australian_Grand_Prix", "Australian Grand Prix"],
  ["Austrian_Grand_Prix", "Austrian Grand Prix"],
  ["Azerbaijan_Grand_Prix", "Azerbaijan Grand Prix"],
  ["Bahrain_Grand_Prix", "Bahrain Grand Prix"],
  ["Belgian_Grand_Prix", "Belgian Grand Prix"],
  ["British_Grand_Prix", "British Grand Prix"],
  ["Canadian_Grand_Prix", "Canadian Grand Prix"],
  ["Chinese_Grand_Prix", "Chinese Grand Prix"],
  ["Dutch_Grand_Prix", "Dutch Grand Prix"],
  ["Emilia_Romagna_Grand_Prix", "Emilia-Romagna Grand Prix"],
  ["Hungarian_Grand_Prix", "Hungarian Grand Prix"],
  ["Italian_Grand_Prix", "Italian Grand Prix"],
  ["Japanese_Grand_Prix", "Japanese Grand Prix"],
  ["Las_Vegas_Grand_Prix", "Las Vegas Grand Prix"],
  ["Mexico_City_Grand_Prix", "Mexico City Grand Prix"],
  ["Miami_Grand_Prix", "Miami Grand Prix"],
  ["Monaco_Grand_Prix", "Monaco Grand Prix"],
  ["Qatar_Grand_Prix", "Qatar Grand Prix"],
  ["Saudi_Arabian_Grand_Prix", "Saudi Arabian Grand Prix"],
  ["Singapore_Grand_Prix", "Singapore Grand Prix"],
  ["Spanish_Grand_Prix", "Spanish Grand Prix"],
  ["S\u00e3o_Paulo_Grand_Prix", "S\u00e3o Paulo Grand Prix"],
  ["United_States_Grand_Prix", "United States Grand Prix"],
];

const RaceStateForm = ({ formData, onChange, availableDrivers = driverDirectory }) => {
  return (
    <div className="form-section">
      <h3>Race Information</h3>

      <div className="form-grid">
        <label>
          <span>Race</span>

          <select
            name="race"
            value={formData.race}
            onChange={onChange}
          >
            {races.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span>Driver</span>

          <select
            name="driver"
            value={formData.driver}
            onChange={onChange}
          >
            {availableDrivers.map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
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
            onChange={onChange}
          />
        </label>

        <label>
          <span>Position</span>

          <input
            type="number"
            name="position"
            min="1"
            value={formData.position}
            onChange={onChange}
          />
        </label>
      </div>
    </div>
  );
};

export default RaceStateForm;