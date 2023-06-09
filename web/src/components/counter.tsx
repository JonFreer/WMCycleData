import { useParams } from "react-router-dom";
import NavBar from "./navBar";
import styles from "../css_modules/dashboard.module.css"
import Graph from "./graph";
function Counter() {
    const { idenitiy } = useParams()

    console.log(idenitiy)
    
    return (<>
        <NavBar></NavBar>
        <div className={styles.main}>
            <div className={styles.title_box}>
                <h4 className={styles.title}>Bristol Road Cycle Counter</h4>
            </div>

            <div className={styles.cardHolder}>
                <div className={styles.card}>
                    <div className={styles.cardBody}>
                        <h5>Users this week</h5>
                        <h3>5000</h3>
                    </div>
                </div>
            </div>

            <div className={styles.card}>
                <div className={styles.cardHeader}>
                    <h4 className={styles.headerTitle}>Weekly Overview</h4>
                  

                </div>
                <div className={styles.cardBody}>
                        <Graph name={"Counter Name"}></Graph>
                    </div>
            </div>

        </div>

    </>)
}

export default Counter;