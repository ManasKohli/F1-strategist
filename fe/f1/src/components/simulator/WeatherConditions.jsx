const WeatherConditions = ({ formData, onChange }) => {
  return (
    <div className="form-section">
      <h3>Weather</h3>

      <label>
        <span>Rain conditions</span>

        <select
          name="rain_condition"
          value={formData.rain_condition}
          onChange={onChange}
        >
          <option value="">Normal</option>
          <option value="light_rain">Light Rain</option>
          <option value="heavy_rain">Heavy Rain</option>
        </select>
      </label>
    </div>
  );
};

export default WeatherConditions;