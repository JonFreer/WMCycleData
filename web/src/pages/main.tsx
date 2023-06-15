import { useCounters } from "../App";
import Map from "../components/map";

function Main(){

    const counters = useCounters();
    
    return(
        <div className = "main">
            <Map identity={undefined}></Map>
        </div>
    )
}

export default Main;