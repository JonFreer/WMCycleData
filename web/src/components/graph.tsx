import React, { useRef, useEffect, useState, ChangeEvent } from 'react';
import { Count, Counter } from '../types/types';
import Chart from "react-apexcharts";
import ReactApexChart from 'react-apexcharts';
import { ApexOptions } from 'apexcharts';

function Graph({ identity }: { identity: number }) {


    const [counts, setCounts] = useState<Count[]>([]);

    function getCounts() {

        const requestOptions = {
            method: 'GET',
        };

        fetch('/api/counts', requestOptions)
            .then(response => {
                console.log(response)
                if (response.status == 200) {
                    response.json().then((data:Count[]) => {
                        console.log(data)
                        let filtered = data.filter(x=> x.counter == identity)
                        setCounts(filtered)
                    });
                } else {
                    console.log("/api/counters", response.text)
                }
            })
    }

    useEffect(() => {
        getCounts();
    }, [])

    const state = {
        series: [{
          name: "Users In",
          data: counts.map(x => [x.timestamp,x.count_in])
        },
        {
          name: "Users Out",
          data: counts.map(x => [x.timestamp,x.count_out])
        }
      ]
    }
    const options:ApexOptions = {
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
          // title: {
          //   text: 'Stock Price Movement',
          //   align: 'left'
          // },
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
              formatter: function (val:any) {
                return (val ).toFixed(0);
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
              formatter: function (val:any) {
                return (val).toFixed(0)
              }
            }
          }
        }
      
    return (

            <ReactApexChart type={"area"} height={"100%"} options={options} series={state.series}></ReactApexChart>
    )


}

export default Graph;