import { useCounters } from "../App";
import dashboard_styles from "../css_modules/dashboard.module.css";
import styles from "../css_modules/counters.module.css";
import { Counter, CounterPlus } from "../types/types";
function Counters() {
  const counters = useCounters();

  return (
    <div className={styles.main}>
      {counters.map(function (object, i) {
        return <CounterCard counter={object} key={i} />;
      })}
    </div>
  );
}

function CounterCard({ counter }: { counter: CounterPlus }) {
  return (
    <a
      href={"/counter/" + counter.identity}
      className={`${dashboard_styles.card} ${styles.cardGap}`}
    >
      <div className={`${dashboard_styles.cardBody} ${styles.cardHolder}`}>
        <div className={styles.cardDetails}>
          <h4 className={styles.cardTitle}>{counter.name}</h4>
          <p>{counter.location_desc}</p>
          <div className={dashboard_styles.buttonHolder}>
            <a
              className={dashboard_styles.button}
              href={"/counter/" + counter.identity}
            >
              {counter.today_count} users today
            </a>
            <a
              className={dashboard_styles.button}
              href={"/counter/" + counter.identity}
            >
              {counter.week_count} users last week
            </a>
          </div>
        </div>
        <div className={styles.cardContentBG}>
          <div className={styles.cardContentFiller}></div>
          <div className={styles.cardContent}>
            <p className={styles.cardContentTitle}>Users Yesterday</p>
            <h2 className={styles.cardContentNumber}>
              {" "}
              {counter.yesterday_count}
            </h2>
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardContentTitle}>Weekly Users</p>
            <h2 className={styles.cardContentNumber}>{counter.week_count}</h2>
          </div>
        </div>
      </div>
    </a>
  );
}

export default Counters;
