import { useParams } from "react-router-dom";
import styles from "../css_modules/dashboard.module.css";
import dropdown_style from "../css_modules/dropdown.module.css";
import Graph from "./graph";
import { useCounters } from "../App";
import { useState } from "react";
import Map from "./map";
function Counter() {
  const { idenitiy } = useParams();
  const counters = useCounters();

  const counter = counters.filter((x) => x.identity == Number(idenitiy))[0];

  if (counter == undefined) {
    return <div></div>;
  }
  console.log(idenitiy);

  var prevMonday = new Date();
  prevMonday.setDate(
    prevMonday.getDate() - ((prevMonday.getDay() + 6) % 7) - 7
  );

  var thisMonday = new Date();
  thisMonday.setDate(thisMonday.getDate() - ((thisMonday.getDay() + 6) % 7));

  var prevSunday = new Date();
  prevSunday.setDate(
    prevSunday.getDate() - ((prevSunday.getDay() + 6) % 7) - 1
  );

  return (
    <>
      <div className={styles.main}>
        <div className={styles.title_box}>
          <h4 className={styles.title}>{counter.name}</h4>
          <span> {counter.location_desc} </span>
        </div>

        <div className={styles.cardHolder}>
          <div className={styles.cardSubHolder}>
            <div className={styles.card}>
              <div className={styles.cardBody}>
                <div>Users Today</div>
                <div className={styles.cardDate}>
                  {new Date().toLocaleDateString()}
                </div>
                <div className={styles.cardCount}>{counter.today_count}</div>
              </div>
            </div>

            <div className={styles.card}>
              <div className={styles.cardBody}>
                <div>Users Yesterday</div>
                <div className={styles.cardDate}>
                  {new Date(
                    new Date().valueOf() - 1000 * 60 * 60 * 24
                  ).toLocaleDateString()}
                </div>
                <div className={styles.cardCount}>
                  {counter.yesterday_count}
                </div>
              </div>
            </div>
          </div>
          <div className={styles.cardSubHolder}>
            <div className={styles.card}>
              <div className={styles.cardBody}>
                <div>Users This Week</div>
                <div className={styles.cardDate}>
                  {thisMonday.toLocaleDateString()} -{" "}
                  {new Date().toLocaleDateString()}
                </div>
                <div className={styles.cardCount}>{counter.week_count}</div>
              </div>
            </div>

            <div className={styles.card}>
              <div className={styles.cardBody}>
                <div>Users Last Week</div>
                <div className={styles.cardDate}>
                  {prevMonday.toLocaleDateString()} -{" "}
                  {prevSunday.toLocaleDateString()}
                </div>
                <div className={styles.cardCount}>
                  {counter.last_week_count}
                </div>
              </div>
            </div>
          </div>
        </div>

        <GraphHolder
          type={"day"}
          default_chart_style={"area"}
          default_time_interval={"1 hour"}
          title={"Daily Overview"}
          identity={counter.identity}
        ></GraphHolder>

        <GraphHolder
          type={"week"}
          default_chart_style={"bar"}
          default_time_interval={"1 day"}
          title={"Weekly Overview"}
          identity={counter.identity}
        ></GraphHolder>

        <GraphHolder
          type={"month"}
          default_chart_style={"bar"}
          default_time_interval={"1 week"}
          title={"Week by Week Overview"}
          identity={counter.identity}
        ></GraphHolder>

        <div className={`${styles.card} ${styles.map_holder}`}>
          <Map identity={Number(idenitiy)}></Map>
        </div>
      </div>
    </>
  );
}

function GraphHolder({
  identity,
  title,
  default_time_interval,
  default_chart_style,
  type,
}: {
  identity: number;
  title: string;
  default_time_interval: string;
  default_chart_style: "bar" | "area";
  type: "week" | "day" | "month";
}) {
  const [date_selected, set_date_selected] = useState<string>("default");
  const [time_interval, set_time_interval] = useState<string>(
    default_time_interval
  );
  const [chart_style, set_chart_style] = useState<"bar" | "area">(
    default_chart_style
  );

  var end_date: Date | null = new Date();
  var start_date: Date | null = new Date();
  start_date.setDate(start_date.getDate() - 7);

  if (type == "day") {
    if (date_selected == "today") {
      end_date = new Date();
      start_date = new Date(new Date().setHours(0, 0, 0, 0));
    } else if (date_selected == "default") {
      end_date = new Date(new Date().setHours(0, 0, 0, 0));
      start_date = new Date();
      start_date.setDate(new Date().getDate() - 1); //.setHours(0,0,0,0))
      start_date.setHours(0, 0, 0, 0);
    } else {
      end_date = new Date(date_selected);
      end_date.setHours(23, 59, 0, 0);
      start_date = new Date(date_selected);
      start_date.setHours(0, 0, 0, 0);
    }
  }

  if (type == "week") {
    if (date_selected == "week_to_date") {
      end_date = new Date();
      start_date = new Date();
      const today = start_date.getDate();
      const currentDay = start_date.getDay();
      start_date.setDate(today - (currentDay || 7));
      start_date.setHours(13, 0, 0, 0);
    } else if (date_selected == "default") {
      //last week
      end_date = new Date();
      const today = end_date.getDate();
      const currentDay = end_date.getDay();
      end_date.setDate(today - (currentDay || 7));
      end_date.setHours(13, 0, 0, 0);
      start_date = new Date(new Date().setDate(end_date.getDate() - 7));
      start_date.setHours(13, 0, 0, 0);
    } else {
      start_date = new Date(date_selected);
      const today = start_date.getDate();
      const currentDay = start_date.getDay();
      start_date.setDate(today - (currentDay || 7));
      start_date.setHours(13, 0, 0, 0);
      end_date = new Date(start_date);
      end_date = new Date(end_date.setDate(start_date.getDate() + 7));
    }
  }

  if (type == "month") {
    end_date = null;
    start_date = null;
  }

  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <span className={styles.headerTitle}>{title}</span>

        <div className={dropdown_style.options_holder}>
          <DateSelectorDaily
            type={type}
            id={date_selected}
            setter={set_date_selected}
          ></DateSelectorDaily>
          <TimeSelect
            id={time_interval}
            setter={set_time_interval}
          ></TimeSelect>
          <StyleSelect id={chart_style} setter={set_chart_style}></StyleSelect>
        </div>
      </div>
      <div className={styles.cardBody} style={{ paddingTop: "0px" }}>
        <Graph
          start_date={start_date}
          end_date={end_date}
          style={chart_style}
          time_interval={time_interval}
          identity={identity}
          type={type}
        ></Graph>
      </div>
    </div>
  );
}

function DateSelectorDaily({
  id,
  setter,
  type,
}: {
  id: string;
  setter: any;
  type: string;
}) {
  const [custom_date, set_custom_date] = useState<Date | null>(null);

  if (type == "day") {
    return (
      <div className={dropdown_style.multi_button_holder}>
        <div
          onClick={() =>
            setter((document.getElementById("start") as HTMLInputElement).value)
          }
          className={
            id != "today" && id != "default"
              ? `${dropdown_style.multi_button}  ${dropdown_style.picker} ${dropdown_style.left} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left}`
          }
        >
          {/* {custom_date == null ? "Custom" : "Date Set"} */}
          <input
            onChange={(x) => setter(x.target.value)}
            className={dropdown_style.input}
            type="date"
            id="start"
            name="start"
          ></input>
        </div>

        <div
          onClick={() => setter("default")}
          className={
            id == "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.active}`
              : `${dropdown_style.multi_button}`
          }
        >
          Yesterday
        </div>

        <div
          onClick={() => setter("today")}
          className={
            id == "today"
              ? `${dropdown_style.multi_button} ${dropdown_style.right} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.right}`
          }
        >
          Today
        </div>
      </div>
    );
  }

  if (type == "week") {
    return (
      <div className={dropdown_style.multi_button_holder}>
        <div
          onClick={() =>
            setter((document.getElementById("start") as HTMLInputElement).value)
          }
          className={
            id != "week_to_date" && id != "default"
              ? `${dropdown_style.multi_button}  ${dropdown_style.picker} ${dropdown_style.left} ${dropdown_style.active}`
              : `${dropdown_style.multi_button} ${dropdown_style.picker} ${dropdown_style.left}`
          }
        >
          {/* {custom_date == null ? "Custom" : "Date Set"} */}
          <input
            onChange={(x) => setter(x.target.value)}
            className={dropdown_style.input}
            type="date"
            id="start"
            name="start"
          ></input>
        </div>

        <div
          onClick={() => setter("default")}
          className={
            id == "default"
              ? `${dropdown_style.multi_button} ${dropdown_style.active}`
              : `${dropdown_style.multi_button}`
          }
        >
          Last Week
        </div>

        <div
          onClick={() => setter("week_to_date")}
          className={
            id == "week_to_date"
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
}

function TimeSelect({ id, setter }: { id: string; setter: any }) {
  return (
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
}

function StyleSelect({ id, setter }: { id: string; setter: any }) {
  return (
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
}

export default Counter;
