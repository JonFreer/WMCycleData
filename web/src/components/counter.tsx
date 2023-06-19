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
                <div className={styles.cardSubHolder}>
                    <div className={styles.card}>
                        <div className={styles.cardBody}>
                            <div>Users Today</div>
                            <div className={styles.cardCount}>{counter.today_count}</div>
                        </div>
                    </div>

                    <div className={styles.card}>
                        <div className={styles.cardBody}>
                            <div>Users Last Week</div>
                            <div className={styles.cardCount}>{counter.week_count}</div>
                        </div>
                    </div>
                </div>
                <div className={styles.cardSubHolder}>
                    <div className={styles.card}>
                        <div className={styles.cardBody}>
                            <div>Users Yesterday</div>
                            <div className={styles.cardCount}>{counter.yesterday_count}</div>
                        </div>
                    </div>

                    <div className={styles.card}>
                        <div className={styles.cardBody}>
                            <div >Users This Week</div>
                            <div className={styles.cardCount}>{counter.week_count}</div>
                        </div>
                    </div>
                </div>
            </div>

            <GraphHolder
                default_chart_style={"area"}
                default_time_interval={"1 hour"}
                title={"Daily Overview"}
                identity={counter.identity}></GraphHolder>

            <GraphHolder
                default_chart_style={"bar"}
                default_time_interval={"1 day"}
                title={"Weekly Overview"}
                identity={counter.identity}></GraphHolder>

            <GraphHolder
                default_chart_style={"bar"}
                default_time_interval={"1 week"}
                title={"Week by Week Overview"}
                identity={counter.identity}></GraphHolder>


            <div className={`${styles.card} ${styles.map_holder}`} >
                <Map identity={Number(idenitiy)}></Map>
            </div>

        </div>

    </>)
}

function GraphHolder({
    identity,
    title,
    default_time_interval,
    default_chart_style }:
    {
        identity: number,
        title: string,
        default_time_interval: string,
        default_chart_style: "bar" | "area"
    }) {

    const [time_interval, set_time_interval] = useState<string>(default_time_interval);
    const [chart_style, set_chart_style] = useState<"bar" | "area">(default_chart_style);

    return (
        <div className={styles.card}>
            <div className={styles.cardHeader}>
                <span className={styles.headerTitle}>{title}</span>
                <TimeSelect id={time_interval} setter={set_time_interval}></TimeSelect>
                <StyleSelect id={chart_style} setter={set_chart_style}></StyleSelect>

            </div>
            <div className={styles.cardBody} style={{ "paddingTop": "0px" }}>
                <Graph style={chart_style} time_interval={time_interval} identity={identity}></Graph>
            </div>
        </div>
    )
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