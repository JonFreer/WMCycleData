import { useParams } from "react-router-dom";
import NavBar from "./navBar";
import styles from "../css_modules/dashboard.module.css"
import dropdown_style from "../css_modules/dropdown.module.css"
import Graph from "./graph";
import { useCounters } from "../App";
import { useState } from "react";
import Map from "./map";
function Counter() {
    const { idenitiy } = useParams()
    const counters = useCounters();

    const counter = counters.filter(x => x.identity == Number(idenitiy))[0]
    const [time_interval, set_time_interval] = useState<string>("1 hour");
    const [chart_style, set_chart_style] = useState<"bar" | "area">("area");

    if (counter == undefined) {
        return (<div></div>)
    }
    console.log(idenitiy)

    return (<>
        <div className={styles.main}>
            <div className={styles.title_box}>
                <h4 className={styles.title}>{counter.name}</h4>
                <span> {counter.location_desc} </span>
            </div>



            <div className={styles.cardHolder}>

                <div className={styles.card}>
                    <div className={styles.cardBody}>
                        <h5>Users today</h5>
                        <h3>{counter.today_count}</h3>
                    </div>
                </div>

                <div className={styles.card}>
                    <div className={styles.cardBody}>
                        <h5>Users this week</h5>
                        <h3>{counter.week_count}</h3>
                    </div>
                </div>
            </div>

            <div className={styles.card}>
                <div className={styles.cardHeader}>
                    <span className={styles.headerTitle}>Weekly Overview</span>
                    <TimeSelect id={time_interval} setter={set_time_interval}></TimeSelect>
                    <StyleSelect id={chart_style} setter={set_chart_style}></StyleSelect>

                </div>
                <div className={styles.cardBody} style={{ "paddingTop": "0px" }}>
                    <Graph style={chart_style} time_interval={time_interval} identity={counter.identity}></Graph>
                </div>
            </div>

            <div className={`${styles.card} ${styles.map_holder}`} >
                <Map identity={Number(idenitiy)}></Map>
            </div>

        </div>

    </>)
}

function TimeSelect({ id, setter }: { id: string, setter: any }) {
    return (
        <select onChange={(x) => setter(x.target.value)} defaultValue={id} className={dropdown_style.main} name="time_select" id="time_select">
            <option value="1 hour">Hourly</option>
            <option value="1 day">Daily</option>
            <option value="1 week">Weekly</option>
            <option value="1 month">Monthly</option>
        </select>
    )
}

function StyleSelect({ id, setter }: { id: string, setter: any }) {
    return (
        <select onChange={(x) => setter(x.target.value)} defaultValue={id} className={dropdown_style.main} name="style_select" id="style_select">
            <option value="bar">Bar</option>
            <option value="area">Line</option>
        </select>
    )
}

export default Counter;