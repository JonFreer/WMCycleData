import { useLayoutEffect, useState } from "react";
import "./App.css";
import NavBar from "./components/navBar";
import { Outlet, useOutletContext } from "react-router-dom";
import { CounterPlus } from "./types/types";

function App() {
  const [counters, setCounters] = useState<CounterPlus[]>([]);

  function getCounters() {
    const requestOptions = {
      method: "GET",
    };
    fetch("/api/counters_plus/", requestOptions).then((response) => {
      if (response.status === 200) {
        response.json().then((data: CounterPlus[]) => {
          data = data.sort((a, b) => b.this_week_count - a.this_week_count);
          setCounters(data);
        });
      } else {
        console.log("/api/counters", response.text);
      }
    });
  }

  useLayoutEffect(() => {
    getCounters();
  }, []);

  return (
    <div className="App">
      <NavBar></NavBar>
      <Outlet context={counters}></Outlet>
    </div>
  );
}

export function useCounters(): CounterPlus[] {
  return useOutletContext<CounterPlus[]>();
}

export default App;
