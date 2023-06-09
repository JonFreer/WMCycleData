import { useParams } from "react-router-dom";
import NavBar from "./navBar";
import styles from "../css_modules/dashboard.module.css"
import Graph from "./graph";
import { useCounters } from "../App";
function Counter() {
    const { idenitiy } = useParams()
    const counters = useCounters();

    const counter = counters.filter(x => x.identity == Number(idenitiy))[0]

    if(counter == undefined){
        return(<div></div>)
    }
    console.log(idenitiy)


    return (<>
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
                        <Graph name={counter.name}></Graph>
                    </div>
            </div>

        </div>

    </>)
}

export default Counter;