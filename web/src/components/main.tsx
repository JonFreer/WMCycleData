import { useEffect, useState } from 'react';
import { Counter } from '../types/types';
import Chart from "react-apexcharts";
import Graph from './graph';
import Map from './map';
function Main() {

    const [counters, setCounters] = useState<Counter[]>([]);

    function getCounters() {

        const requestOptions = {
            method: 'GET',
        };

        fetch('/api/counters', requestOptions)
            .then(response => {
                console.log(response)
                if (response.status == 200) {
                    response.json().then((data) => {
                        console.log(data)
                        setCounters(data)
                    });
                } else {
                    console.log("/api/counters", response.text)
                }
            })
    }

    useEffect(() => {
        getCounters();
    }, [])

    return (
        // <div>
            <Map></Map>
       
        // </div>
    )

}

export default Main;

     {/* {counters.map((element, index) => {
                return (
                    <div key={index}>
                        <h2>{element.name.toUpperCase()}</h2>
                        <Graph name={element.name}></Graph>
                        
                    </div>
                );
            })} */}