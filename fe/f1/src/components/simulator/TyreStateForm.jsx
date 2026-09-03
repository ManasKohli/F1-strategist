const TyreStateForm = ({ formData, onChange }) => {
  return (
    <div className="form-section">
      <h3>Tyre State</h3>

      <div className="form-grid">
        <label>
          <span>Compound</span>

          <select
            name="compound"
            value={formData.compound}
            onChange={onChange}
          >
            <option value="SOFT">Soft</option>
            <option value="MEDIUM">Medium</option>
            <option value="HARD">Hard</option>
            <option value="INTERMEDIATE">Intermediate</option>
            <option value="WET">Full Wet</option>
          </select>
        </label>

        <label>
          <span>Tyre Age</span>

          <input
            type="number"
            name="tyre_age"
            min="0"
            value={formData.tyre_age}
            onChange={onChange}
          />
        </label>
      </div>

      <label className="checkbox-row">
        <input
          type="checkbox"
          name="fresh_tyre"
          checked={formData.fresh_tyre}
          onChange={onChange}
        />

        <span>Fresh tyre</span>
      </label>
    </div>
  );
};

export default TyreStateForm;