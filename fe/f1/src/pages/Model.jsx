import "../styles/model.css";

const Model = () => {
  return (
    <main className="model-page">

      {/* HERO */}
      <section className="model-hero">
        <p className="section-label">THE MODEL</p>

        <h1>
          Understanding the
          <br />
          <span>Strategy Engine.</span>
        </h1>

        <p className="model-intro">
          F1 Strategist uses a machine learning pipeline trained
          on historical Formula 1 race data to predict when a
          driver is likely to make their next pit stop.
        </p>
      </section>


      {/* MODEL OVERVIEW */}
      <section className="model-overview">

        <div className="model-overview__text">
          <p className="section-label">01 / MODEL OVERVIEW</p>

          <h2>Random Forest Regression</h2>

          <p>
            The current model is a Random Forest Regressor trained
            to predict the number of laps remaining until a driver's
            next pit stop.
          </p>

          <p>
            Instead of relying on a single decision tree, the model
            combines predictions from many trees to produce a more
            robust estimate.
          </p>
        </div>


        <div className="model-stat">
          <span>MODEL TYPE</span>
          <strong>Random Forest</strong>
        </div>

      </section>


      {/* TARGET */}
      <section className="model-target">

        <div>
          <p className="section-label">02 / TARGET</p>

          <h2>
            What is the model
            <br />
            predicting?
          </h2>
        </div>

        <div className="target-card">

          <span>PRIMARY TARGET</span>

          <strong>laps_until_pit</strong>

          <p>
            The model estimates how many laps remain before
            the driver makes their next pit stop.
          </p>

        </div>

      </section>


      {/* FEATURES */}
      <section className="model-features">

        <div className="model-features__header">

          <p className="section-label">03 / FEATURES</p>

          <h2>
            35 signals.
            <br />
            One prediction.
          </h2>

          <p>
            The model uses race state, driver information,
            tire data, lap-time trends, weather and track
            conditions as inputs.
          </p>

        </div>


        <div className="feature-groups">

          <div className="feature-group">
            <span>01</span>

            <div>
              <h3>Race State</h3>

              <p>
                Race, lap number, total laps, laps remaining
                and race progress.
              </p>
            </div>
          </div>


          <div className="feature-group">
            <span>02</span>

            <div>
              <h3>Driver & Position</h3>

              <p>
                Driver, team, current position, stint and
                pit-stop count.
              </p>
            </div>
          </div>


          <div className="feature-group">
            <span>03</span>

            <div>
              <h3>Tire Information</h3>

              <p>
                Tire compound, tire age, fresh tire status
                and stint length.
              </p>
            </div>
          </div>


          <div className="feature-group">
            <span>04</span>

            <div>
              <h3>Lap Performance</h3>

              <p>
                Lap time, previous lap time, rolling averages,
                pace changes and pace trends.
              </p>
            </div>
          </div>


          <div className="feature-group">
            <span>05</span>

            <div>
              <h3>Weather</h3>

              <p>
                Air temperature, track temperature, humidity,
                pressure, rainfall and wind speed.
              </p>
            </div>
          </div>


          <div className="feature-group">
            <span>06</span>

            <div>
              <h3>Track Conditions</h3>

              <p>
                Safety car, VSC, yellow flag, red flag and
                changing weather conditions.
              </p>
            </div>
          </div>

        </div>

      </section>


      {/* PIPELINE */}
      <section className="model-pipeline">

        <p className="section-label">04 / PIPELINE</p>

        <h2>From data to strategy.</h2>

        <div className="pipeline">

          <div className="pipeline-step">
            <span>01</span>
            <strong>Historical Data</strong>
            <p>Race telemetry, tire and weather data.</p>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <span>02</span>
            <strong>Feature Engineering</strong>
            <p>Transform raw data into model features.</p>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <span>03</span>
            <strong>Random Forest</strong>
            <p>Learn patterns in pit-stop timing.</p>
          </div>

          <div className="pipeline-arrow">→</div>

          <div className="pipeline-step">
            <span>04</span>
            <strong>Prediction</strong>
            <p>Estimate laps until the next pit.</p>
          </div>

        </div>

      </section>


      {/* LIMITATION */}
      <section className="model-note">

        <p className="section-label">05 / CURRENT SCOPE</p>

        <h2>One prediction. More to come.</h2>

        <p>
          The current model focuses specifically on pit-stop
          timing. Future versions can build additional strategy
          logic around tire selection, number of stops, pit
          windows and expected race outcome.
        </p>

      </section>

    </main>
  );
};

export default Model;