const RaceConditions = ({ formData, onChange }) => {
  return (
    <div className="form-section">
      <h3>Race Conditions</h3>

      <label>
        <span>Track condition</span>

        <select
          name="race_condition"
          value={formData.race_condition}
          onChange={onChange}
        >
          <option value="">Normal</option>
          <option value="safety_car_active">Safety Car</option>
          <option value="vsc_active">Virtual Safety Car</option>
          <option value="yellow_flag">Yellow Flag</option>
          <option value="red_flag_active">Red Flag</option>
        </select>
      </label>
    </div>
  );
};

export default RaceConditions;
