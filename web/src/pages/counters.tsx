import { useCounters } from "../App";
import dashboard_styles from "../css_modules/dashboard.module.css";
import styles from "../css_modules/counters.module.css";
import { CounterPlus } from "../types/types";
import { Link } from "react-router-dom";

function Counters() {
  const counters = useCounters();
  return (
    <div className={styles.main}>
      {counters
        .filter((x) => x.name !== "")
        .map(function (object, i) {
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
    <div className={`${dashboard_styles.button} ${styles.counterCardButton}`}>
      {props.count(props.counter)} {props.description}
    </div>
  );
}

function CounterCard({ counter }: { counter: CounterPlus }) {
  return (
    <Link
      to={"/counter/" + counter.identity}
      className={`${dashboard_styles.card} ${styles.counterCard}`}
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
              description="last week"
            />
          </div>
        </div>
      </div>
    </Link>
  );
}

export default Counters;
