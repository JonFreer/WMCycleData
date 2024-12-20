import { useParams } from "react-router-dom";
import styles from "../css_modules/dashboard.module.css";
import dropdown_style from "../css_modules/dropdown.module.css";
import Graph from "./graph";
import { useCounters } from "../App";
import { useState, useMemo } from "react";
import Map from "./map";
import WeekGraphHolder from "./weekGraph";

const Counter = () => {
  const { idenitiy } = useParams();
  const counters = useCounters();

  const counter = useMemo(
    () => counters.find((x) => x.identity === Number(idenitiy)),
    [counters, idenitiy]
  );

  const prevMonday = useMemo(() => {
    const date = new Date();
    date.setDate(date.getDate() - ((date.getDay() + 6) % 7) - 7);
    return date;
  }, []);

  const thisMonday = useMemo(() => {
    const date = new Date();
    date.setDate(date.getDate() - ((date.getDay() + 6) % 7));
    return date;
  }, []);

  const prevSunday = useMemo(() => {
    const date = new Date();
    date.setDate(date.getDate() - ((date.getDay() + 6) % 7) - 1);
    return date;
  }, []);

  if (!counter) {
    return <div></div>;
  }

  return (
    <div className={styles.main}>
      <div className={styles.title_box}>
        <h4 className={styles.title}>{counter.name}</h4>
        <span>{counter.location_desc}</span>
      </div>

      <div className={styles.cardHolder}>
        <div className={styles.cardSubHolder}>
          <Card
            title="Users Today"
            date={new Date().toLocaleDateString()}
            count={counter.today_count}
          />
          <Card
            title="Users Yesterday"
            date={new Date(Date.now() - 86400000).toLocaleDateString()}
            count={counter.yesterday_count}
          />
          <Card
            title="Users This Week"
            date={`${thisMonday.toLocaleDateString()} - ${new Date().toLocaleDateString()}`}
            count={counter.this_week_count}
          />
          <Card
            title="Users Last Week"
            date={`${prevMonday.toLocaleDateString()} - ${prevSunday.toLocaleDateString()}`}
            count={counter.last_week_count}
          />
        </div>
      </div>

      <GraphHolder
        type="day"
        defaultChartStyle="area"
        defaultTimeInterval="1 hour"
        title="Daily Overview"
        identity={counter.identity}
      />
      <WeekGraphHolder identity={counter.identity} />
      <GraphHolder
        type="month"
        defaultChartStyle="bar"
        defaultTimeInterval="1 week"
        title="Week by Week Overview"
        identity={counter.identity}
      />
      <div className={`${styles.card} ${styles.map_holder}`}>
        <Map identity={Number(idenitiy)} />
      </div>
    </div>
  );
};

const Card = ({ title, date, count }:{title:string,date:string,count:number}) => (
  <div className={styles.card}>
    <div className={styles.cardBody}>
      <div>{title}</div>
      <div className={styles.cardDate}>{date}</div>
      <div className={styles.cardCount}>{count}</div>
    </div>
  </div>
);

const GraphHolder = ({
  identity,
  title,
  defaultTimeInterval,
  defaultChartStyle,
  type,
}: {
  identity: number;
  title: string;
  defaultTimeInterval: string;
  defaultChartStyle: "bar" | "area";
  type: "week" | "day" | "month";
}) => {
  const [dateSelected, setDateSelected] = useState("default");
  const [timeInterval, setTimeInterval] = useState(defaultTimeInterval);
  const [chartStyle, setChartStyle] = useState(defaultChartStyle);

  const { startDate, endDate } = useMemo(() => {
    let start: Date | null = new Date();
    let end: Date | null = new Date();

    if (type === "day") {
      if (dateSelected === "today") {
        start.setHours(0, 0, 0, 0);
      } else if (dateSelected === "default") {
        start.setDate(start.getDate() - 1);
        start.setHours(0, 0, 0, 0);
        end.setHours(0, 0, 0, 0);
      } else {
        start = new Date(dateSelected);
        start.setHours(0, 0, 0, 0);
        end = new Date(dateSelected);
        end.setHours(23, 59, 0, 0);
      }
    } else if (type === "week") {
      if (dateSelected === "week_to_date") {
        const today = start.getDate();
        const currentDay = start.getDay();
        start.setDate(today - (currentDay || 7));
        start.setHours(13, 0, 0, 0);
      } else if (dateSelected === "default") {
        const today = end.getDate();
        const currentDay = end.getDay();
        end.setDate(today - (currentDay || 7));
        end.setHours(13, 0, 0, 0);
        start.setDate(end.getDate() - 7);
        start.setHours(13, 0, 0, 0);
      } else {
        start = new Date(dateSelected);
        const today = start.getDate();
        const currentDay = start.getDay();
        start.setDate(today - (currentDay || 7));
        start.setHours(13, 0, 0, 0);
        end = new Date(start);
        end.setDate(start.getDate() + 7);
      }
    } else if (type === "month") {
      start = null;
      end = null;
    }

    return { startDate: start, endDate: end };
  }, [dateSelected, type]);

  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <span className={styles.headerTitle}>{title}</span>
        <div className={dropdown_style.options_holder}>
          <DateSelectorDaily
            type={type}
            id={dateSelected}
            setter={setDateSelected}
          />
          <TimeSelect id={timeInterval} setter={setTimeInterval} />
          <StyleSelect id={chartStyle} setter={setChartStyle} />
        </div>
      </div>
      <div className={styles.cardBody} style={{ paddingTop: "0px" }}>
        <Graph
          defaultStartDate={startDate}
          defaultEndDate={endDate}
          style={chartStyle}
          timeInterval={timeInterval}
          identity={identity}
          type={type}
        />
      </div>
    </div>
  );
};

const DateSelectorDaily = ({ id, setter, type }: {
  id: string;
  setter: any;
  type: string;
}) => {
  if (type === "day") {
    return (
      <div className={dropdown_style.multi_button_holder}>
        <div
          onClick={() =>
            setter((document.getElementById("start") as HTMLInputElement).value)
          }
          className={
            id !== "today" && id !== "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left}`
          }
        >
          <input
            onChange={(x) => setter(x.target.value)}
            className={dropdown_style.input}
            type="date"
            id="start"
            name="start"
          />
        </div>
        <div
          onClick={() => setter("default")}
          className={
            id === "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.active}`
              : `${dropdown_style.multi_button}`
          }
        >
          Yesterday
        </div>
        <div
          onClick={() => setter("today")}
          className={
            id === "today"
              ? `${dropdown_style.multi_button} ${dropdown_style.right} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.right}`
          }
        >
          Today
        </div>
      </div>
    );
  }

  if (type === "week") {
    return (
      <div className={dropdown_style.multi_button_holder}>
        <div
          onClick={() =>
            setter((document.getElementById("start") as HTMLInputElement).value)
          }
          className={
            id !== "week_to_date" && id !== "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left}`
          }
        >
          <input
            onChange={(x) => setter(x.target.value)}
            className={dropdown_style.input}
            type="date"
            id="start"
            name="start"
          />
        </div>
        <div
          onClick={() => setter("default")}
          className={
            id === "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.active}`
              : `${dropdown_style.multi_button}`
          }
        >
          Last Week
        </div>
        <div
          onClick={() => setter("week_to_date")}
          className={
            id === "week_to_date"
              ? `${dropdown_style.multi_button} ${dropdown_style.right} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.right}`
          }
        >
          Week to Date
        </div>
      </div>
    );
  }

  return <div></div>;
};

const TimeSelect = ({ id, setter }: { id: string; setter: any }) => (
  <select
    style={{ marginLeft: "auto" }}
    onChange={(x) => setter(x.target.value)}
    defaultValue={id}
    className={dropdown_style.main}
    name="time_select"
    id="time_select"
  >
    <option value="1 hour">Hourly</option>
    <option value="1 day">Daily</option>
    <option value="1 week">Weekly</option>
    <option value="1 month">Monthly</option>
  </select>
);

const StyleSelect = ({ id, setter }: { id: string; setter: any }) => (
  <select
    onChange={(x) => setter(x.target.value)}
    defaultValue={id}
    className={dropdown_style.main}
    name="style_select"
    id="style_select"
  >
    <option value="bar">Bar</option>
    <option value="area">Line</option>
  </select>
);

export default Counter;
