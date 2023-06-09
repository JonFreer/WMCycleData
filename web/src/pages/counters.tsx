import { useCounters } from "../App";
import dashboard_styles from "../css_modules/dashboard.module.css"
import styles from "../css_modules/counters.module.css"
import { Counter } from "../types/types";
function Counters() {

    const counters = useCounters();

    return (<div className={styles.main}>
        {counters.map(function (object, i) {
            return <CounterCard counter={object} key={i} />;
        })}
    </div>)
}

function CounterCard({ counter }: { counter: Counter }) {
    return (<a href={"/counter/"+counter.identity} className={`${dashboard_styles.card} ${styles.cardGap}`}>
        <div className={`${dashboard_styles.cardBody} ${styles.cardHolder}`}>
            <div className={styles.cardDetails}>
                <h4 className={styles.cardTitle}>{counter.name}</h4>
                <h3>5000</h3>
                <a className={dashboard_styles.button} href={"/counter/"+counter.identity}>View Counter</a>
            </div>
            <div className={styles.cardContentBG}>
                <div className={styles.cardContent}>
                    <p className={styles.cardContentTitle}>Users Today</p>
                    <h2 className={styles.cardContentNumber}> 300</h2>
                </div>
                <div className={styles.cardContent}>
                    <p className={styles.cardContentTitle}>Weekly Users</p>
                    <h2 className={styles.cardContentNumber}>5600</h2>
                </div>
            </div>
        </div>
    </a>)
}

export default Counters;
