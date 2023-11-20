import styles from "../css_modules/about.module.css";

function About() {
  return (
    <>
      <h1 className={styles.title}>WM Cycle Data</h1>
      {/* <h2 className={styles.subtitle}>Subtitle</h2> */}
      <div className={styles.about_box_holder}>
        <div className={styles.about_box}>
          {/* <a className={styles.about_box_a}> */}
            <div>
              <p className={styles.about_box_paragraph}>
                Welcome to WMCycleData.com, a website dedicated to presenting
                comprehensive cycling figures for the West Midlands! We are
                passionate about promoting cycling as a sustainable and healthy
                mode of transportation, and we believe that access to accurate
                and up-to-date statistics is key to making informed decisions
                and driving positive change.
              </p>
              <p className={styles.about_box_paragraph}>
                Our website serves as a hub of information, providing an
                in-depth analysis of cycling trends, patterns, and insights
                specific to the West Midlands region. Whether you're a cyclist,
                a policymaker, a transportation enthusiast, or simply curious
                about the state of cycling in this area, our platform is
                designed to meet your needs.
              </p>

              <p className={styles.about_box_paragraph}>
                Join us on this journey as we unveil the story of cycling in the
                West Midlands, one statistic at a time.
              </p>
            </div>
          {/* </a> */}
        </div>

        <div className={styles.about_box}>
          <a className={styles.about_box_non_a}>
            <div>
              <h3 className={styles.about_box_heading}>
                <div className={styles.beta}>Beta</div>
              </h3>
              <p className={styles.about_box_paragraph}>
                This site is still under very heavy development: many aspects
                may change, data may be lost, features may be missing. Despite
                this we appreciate any use of this site during these early days
                and if you have any problems please feel free to reach out to
                cyclecounter@douvk.co.uk
              </p>
            </div>
          </a>
        </div>

        <div className={styles.about_box}>
          <div className={styles.about_box_non_a}>
            <div>
              <h3 className={styles.about_box_heading}>
                FAQ
              </h3>
              <p className={styles.about_box_paragraph}>
                  <h4>Where does the data come from?</h4>
                  All of the data is supplied by Transport For West Midlands. We store the data provided by TFWM and provide tools to visualise the data.

                  <h4>What is a counter?</h4>
                  TFWM uses Vivacity AI Cameras to perform traffic counting. These cameras count the incoming and outgoing traffic of their frames, classifying by a variety of modes such as car, cyclist and pedestrian.
                  Often a single camera can be used to count traffic across multiple areas, displayed in our tool as multiple counters.

                  <h4>Is the data accurate?</h4>
                  As with all automated counting methods there is a margin of error. Based on Vivacity's own documentation they state that their counters when evaluated against manual testing can undercount by as much as 20%. 
                  Furthermore we often see spikes in the data which do not correlate with expected traffic flow. We have taken the decision not to remove anomalies from the data and present the data as is.

                  <h4>Can I download the data?</h4>

                  We provide an API which allows querying of all our data. If you plan to download large amounts of data, please contact me at contact@douvk.co.uk and I can provide a dump.

                  <h4>I have more questions</h4>
                  
                  Feel free to contact me at contact@douvk.co.uk or <a href="https://twitter.com/JonathanFreer">@JonathanFreer</a> on Twitter.
              </p>
            </div>
          </div>
        </div>

        <div className={styles.about_box}>
          <a className={styles.about_box_a} href={"/api/docs"}>
            <div>
              <h3 className={styles.about_box_heading}>API</h3>
              <p className={styles.about_box_paragraph}>
                All of the data that we collect is publically accessible. It can
                be easily accessed through our API. Click here to visit the
                documentation. This data is provided to us by the BCC under the{" "}
                <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/">
                  Open Government Licence v3.0
                </a>
                . We futher distribute this data under the same licence.
              </p>
              <div className={styles.about_box_button}>Vist API</div>
            </div>
            <img
              className={styles.about_box_image}
              src={"/about/api.png"}
            ></img>
          </a>
        </div>

        <div className={styles.about_box}>
          <a
            className={styles.about_box_a}
            href={"https://github.com/JonFreer/WMCycleData"}
          >
            <div>
              <h3 className={styles.about_box_heading}>GitHub</h3>
              <p className={styles.about_box_paragraph}>
                Our code is open source and can be found on our GitHub. Feel
                free to check out the source code, suggest an improvement or
                raise an issue.
              </p>
              <div className={styles.about_box_button}>Vist GitHub</div>
            </div>
            <img
              className={styles.about_box_image}
              src={"/about/github.png"}
            ></img>
          </a>
        </div>
      </div>
    </>
  );
}

export default About;
