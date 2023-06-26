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
function StatCard(props: {
  counter: CounterPlus;
  count: (c: CounterPlus) => number;
  description: string;
}) {
  return (
    <a
      className={`${dashboard_styles.button} ${styles.counterCardButton}`}
      href={"/counter/" + props.counter.identity}
    >
      {props.count(props.counter)} {props.description}
    </a>
  );
}
function CounterCard({ counter }: { counter: CounterPlus }) {
  return (
    <a
      href={"/counter/" + counter.identity}
      className={`${dashboard_styles.card} ${styles.counterCard} ${styles.cardGap}`}
    >
      <div className={`${dashboard_styles.cardBody} ${styles.cardHolder}`}>
        <div className={styles.cardDetails}>
          <h4 className={styles.cardTitle}>{counter.name}</h4>
          <p>{counter.location_desc}</p>
          <div
            className={`${dashboard_styles.buttonHolder} ${styles.counterCardButtonHolder}`}
          >
            <StatCard
              counter={counter}
              count={(c) => c.today_count}
              description="today"
            />
            <StatCard
              counter={counter}
              count={(c) => c.yesterday_count}
              description="yesterday"
            />
            <StatCard
              counter={counter}
              count={(c) => c.last_week_count}
              description="past week"
            />
          </div>
        </div>
      </div>
    </a>
  );
}

export default Counters;
