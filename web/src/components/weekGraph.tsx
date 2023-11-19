import { useEffect, useRef } from "react";
import { Count } from "../types/types";
import ReactApexChart from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import apexchart from "apexcharts";
import styles from "../css_modules/dashboard.module.css";

function WeekGraph({
  identity,
  style,
}: {
  identity: number;
  style: "bar" | "area";
}) {
  const series: ApexAxisChartSeries = [
    { name: "Cyclists", data: [] },
    { name: "E-Scooter", data: [] },
    { name: "Pedestrians", data: [] },
    { name: "Cars", data: [] },
    { name: "Bus", data: [] },
  ];

  function updateCounts(counts: Count[]) {
    const series: ApexAxisChartSeries = [
      {
        name: "Cyclists",
        data: counts
          .filter((x) => x.mode === "cyclist")
          .map((x) => x.count_out + x.count_in),
      },
      {
        name: "E-Scooter",
        data: counts
          .filter((x) => x.mode === "escooter")
          .map((x) => x.count_out + x.count_in),
      },

      {
        name: "Pedestrians",
        data: counts
          .filter((x) => x.mode === "pedestrian")
          .map((x) => x.count_out + x.count_in),
      },

      {
        name: "Cars",
        data: counts
          .filter((x) => x.mode === "car")
          .map((x) => x.count_out + x.count_in),
      },

      {
        name: "Bus",
        data: counts
          .filter((x) => x.mode === "bus")
          .map((x) => x.count_out + x.count_in),
      },
    ];

    for (let i = 0; i < series.length; i++) {
      if (series[i].data.length === 0) {
        series[i].data = [];
      }
    }

    apexchart.exec("weekly_average", "updateSeries", series, true);
  }

  function getCounts(_min: number = 0, _max: number = 0) {
    const requestOptions = {
      method: "GET",
    };

    let query = "/api/average_week/?identity=" + identity;

    fetch(query, requestOptions).then((response) => {
      if (response.status === 200) {
        response.json().then((data: any[]) => {
          let filtered = data.filter(
            (x) => x.identity === identity //&& x.mode === "cyclist"
          );

          updateCounts(filtered);
        });
      } else {
        console.error("/api/average_week", response.text);
      }
    });
  }

  useEffect(() => {
    getCounts();
  }, [style, identity]);

  const options: ApexOptions = {
    chart: {
      id: "weekly_average",
      type: "area",
      stacked: false,
      height: "100px",
      zoom: {
        type: "x",
        enabled: true,
        autoScaleYaxis: true,
      },
      toolbar: {
        autoSelected: "zoom",
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
      categories: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
      tooltip: {
        enabled: false,
      },
    },
    tooltip: {
      y: {
        formatter: function (val: any) {
          if (val === undefined) {
            return 0;
          }
          return val.toFixed(0);
        },
      },
      x: {
        format: "H:mm dddd dd MMM",
      },
    },
  };

  if (style === "bar") {
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

function WeekGraphHolder({ identity }: { identity: number }) {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        <span className={styles.headerTitle}>{"Weekly Average"}</span>
      </div>
      <div className={styles.cardBody} style={{ paddingTop: "0px" }}>
        <WeekGraph identity={identity} style={"bar"}></WeekGraph>
      </div>
    </div>
  );
}

export default WeekGraphHolder;
