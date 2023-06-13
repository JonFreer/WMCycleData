import styles from '../css_modules/about.module.css'

function About() {
    return (
        <>
            <h1 className={styles.title}>WM Cycle Data</h1>
            {/* <h2 className={styles.subtitle}>Subtitle</h2> */}
            <div className={styles.about_box_holder}>

                <div className={styles.about_box}>
                    <a className={styles.about_box_a}>
                        <div>
                            <h3 className={styles.about_box_heading}>
                                <div className={styles.beta}>Beta</div>
                            </h3>
                            <p className={styles.about_box_paragraph} >
                                This site is still under very heavy development: many aspects may change, data may be lost, features may be missing.
                                Despite this we appreciate any use of this site during these early days and if you have any problems please feel free to reach out to cyclecounter@douvk.co.uk
                            </p>
                        </div>

                    </a>
                </div>

                <div className={styles.about_box}>
                    <a className={styles.about_box_a} href={"/api/docs"}>
                        <div>
                            <h3 className={styles.about_box_heading}>
                                API
                            </h3>
                            <p className={styles.about_box_paragraph} >
                                All of the data that we collect is publically accessible. It can be easily accessed through our API.
                                Click here to visit the documentation.
                                This data is provided to us by the BCC under the <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/">Open Government Licence v3.0</a>.
                                We futher distribute this data under the same licence.
                            </p>
                            <div className={styles.about_box_button}>Vist API</div>
                        </div>
                        <img className={styles.about_box_image} src={process.env.PUBLIC_URL + "/about/api.png"}></img>
                    </a>
                </div>

                <div className={styles.about_box}>
                    <a className={styles.about_box_a} href={"/api/docs"}>
                        <div>
                            <h3 className={styles.about_box_heading}>
                                GitHub
                            </h3>
                            <p className={styles.about_box_paragraph} >
                                Our code is open source and can be found on our GitHub.
                                Feel free to check out the source code, suggest an improvement or raise an issue.
                            </p>
                            <div className={styles.about_box_button}>Vist GitHub</div>
                        </div>
                        <img className={styles.about_box_image} src={process.env.PUBLIC_URL + "/about/github.png"}></img>
                    </a>
                </div>

            </div>
        </>)
}

export default About;