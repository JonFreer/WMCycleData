import { useEffect, useRef, useState } from "react";
import { Count } from "../types/types";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import apexchart from "apexcharts";
import { count } from "console";

function Graph({
  identity,
  time_interval,
  style,
  default_start_date,
  default_end_date,
  type,
}: {
  identity: number;
  time_interval: string;
  style: "bar" | "area";
  default_start_date: Date | null;
  default_end_date: Date | null;
  type: "day" | "week" | "month";
}) {
  console.log("RERENDER");

  const min = useRef<number>(2 ^ 53);
  // const [min, setMin] = useState<number>(2^53);

  // By defualt the min and max should be set to the props

  const series: ApexAxisChartSeries = [];

  function updateCounts(counts: Count[]) {
    const series: ApexAxisChartSeries = [
      {
        name: "Users In",
        data: counts.map((x) => [new Date(x.timestamp).getTime(), x.count_in]),
      },
      {
        name: "Users Out",
        data: counts.map((x) => [new Date(x.timestamp).getTime(), x.count_out]),
      },
    ];

    apexchart.exec(type, "updateSeries", series, false);
  }

  function getCounts(_min: number = 0, _max: number = 0) {
    console.log(time_interval);
    const requestOptions = {
      method: "GET",
    };

    let query =
      "/api/counts/?time_interval=" +
      encodeURIComponent(time_interval) +
      "&identity=" +
      identity;

    query = query + "&start_time=" + Math.floor(_min / 1000);

    fetch(query, requestOptions).then((response) => {
      console.log(response);
      if (response.status == 200) {
        response.json().then((data: Count[]) => {
          console.log(data);
          let filtered = data.filter(
            (x) => x.counter == identity && x.mode == "cyclist"
          );
          updateCounts(filtered);
        });
      } else {
        console.log("/api/counters", response.text);
      }
    });
  }

  useEffect(() => {
    if (default_start_date != undefined) {
      getCounts(default_start_date.getTime() - 604800000);
      min.current = default_start_date.getTime() - 604800000;
      // setMin();
    } else {
      getCounts();
    }
  }, [style, time_interval, identity, default_start_date, default_end_date]);

  const options: ApexOptions = {
    chart: {
      id: type,
      type: "area",
      stacked: false,
      // height: "100%",
      height: "100px",
      zoom: {
        type: "x",
        enabled: true,
        autoScaleYaxis: true,
      },
      toolbar: {
        autoSelected: "zoom",
      },
      events: {
        zoomed: function (chartContext, { xaxis, yaxis }) {
          if (xaxis.min < min.current) {
            min.current = xaxis.min - 100000000;
            getCounts(min.current, xaxis.max);

            chartContext.updateOptions({
              xaxis: {
                min: xaxis.min,
                max: xaxis.max,
              },
            });
          }
        },
      },
    },
    dataLabels: {
      enabled: false,
    },
    markers: {
      size: 0,
    },
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        inverseColors: false,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [20, 100, 100, 100],
      },
    },
    yaxis: {
      labels: {
        formatter: function (val: any) {
          return val.toFixed(0);
        },
      },
      title: {
        text: "Users",
      },
    },
    xaxis: {
      type: "datetime",
      labels: {
        datetimeUTC: false,
      },
      tooltip: {
        enabled: false,
      },
    },
    tooltip: {
      y: {
        formatter: function (val: any) {
          return val.toFixed(0);
        },
      },
      x: {
        format: "H:mm dddd dd MMM",
      },
    },
  };

  if (options.xaxis) {
    // options.xaxis.min = min;
    if (default_start_date != null) {
      options.xaxis.min = default_start_date.getTime();
      // setMax(default_end_date.getTime());
    }
    // options.xaxis.max = max;
    if (default_end_date != null) {
      options.xaxis.max = default_end_date.getTime();
      // setMax(default_end_date.getTime());
    }
  }

  if (
    type == "week" &&
    options.xaxis != undefined &&
    options.tooltip != undefined &&
    options.tooltip.x != undefined
  ) {
    (options.xaxis as ApexXAxis).labels = {
      datetimeUTC: false,
      format: "ddd dd/MM",
    };

    options.tooltip.x.format = "ddd dd/MM";
  }

  if (style == "bar") {
    options.fill = {};
  }

  return (
    <ReactApexChart
      key={style}
      type={style}
      height={"100%"}
      options={options}
      series={series}
    ></ReactApexChart>
  );
}

export default Graph;
