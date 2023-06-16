import React, { useRef, useEffect, useState, ChangeEvent } from 'react';
import { Count, Counter } from '../types/types';
import Chart from "react-apexcharts";
import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

function Graph(
  { identity, time_interval, style }: 
  { identity: number, 
    time_interval: string, 
    style: "bar" | "area" }) {


  const [counts, setCounts] = useState<Count[]>([]);

  function getCounts() {
    console.log(style)

    const requestOptions = {
      method: 'GET',
    };
    console.log(time_interval)
    fetch('/api/counts/?time_interval=' + encodeURIComponent(time_interval) + '&identity=' + identity, requestOptions)
      .then(response => {
        console.log(response)
        if (response.status == 200) {
          response.json().then((data: Count[]) => {
            console.log(data)
            let filtered = data.filter(x => x.counter == identity && x.mode == "cyclist")
            setCounts(filtered)
          });
        } else {
          console.log("/api/counters", response.text)
        }
      })
  } 

  // useEffect(()=>{
  //   this.forceUpdate();
  // },[style]
  // )

  useEffect(() => {
    getCounts();
  }, [style, time_interval,identity])

  const series: ApexAxisChartSeries = [{
    name: "Users In",
    data: counts.map(x => [new Date(x.timestamp).getTime(), x.count_in])
  },
  {
    name: "Users Out",
    data: counts.map(x => [new Date(x.timestamp).getTime(), x.count_out])
  }
  ]

  const options: ApexOptions = {
    chart: {
      type: 'area',
      stacked: false,
      // height: "100%",
      height: "100px",
      zoom: {
        type: 'x',
        enabled: true,
        autoScaleYaxis: true
      },
      toolbar: {
        autoSelected: 'zoom'
      }
    },
    dataLabels: {
      enabled: false
    },
    markers: {
      size: 0,
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        inverseColors: false,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [20, 100, 100, 100]
      },
    },
    yaxis: {
      labels: {
        formatter: function (val: any) {
          return (val).toFixed(0);
        },
      },
      title: {
        text: 'Users'
      },
    },
    xaxis: {
      type: 'datetime',
    },
    tooltip: {
      shared: false,
      y: {
        formatter: function (val: any) {
          return (val).toFixed(0)
        }
      }
    }
  }

  if(style == "bar"){
    options.fill = {};
  }else{
    // options.fill = {
    //   type: 'gradient',
    //   gradient: {
    //     shadeIntensity: 1,
    //     inverseColors: false,
    //     opacityFrom: 0.45,
    //     opacityTo: 0.05,
    //     stops: [20, 100, 100, 100]
    //   },
    // }
  }
  
  return (
    <ReactApexChart key={style} type={style} height={"100%"} options={options} series={series}></ReactApexChart>
  )


}

export default Graph;