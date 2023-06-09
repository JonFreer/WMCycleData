import { Counter } from "../types/types";

function data2geojson(data:Counter[]) {

    const tempData = []
    for (let i = 0; i < data.length; i++) {

    //   if (props.data[i].state == 0 && settings.unclassified || props.data[i].state == 1 && settings.incomplete || props.data[i].state == 2 && settings.completed) {

        tempData.push({
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [data[i].lon, data[i].lat]
          }, "properties": {
            // "time": props.data[i].time,
            "id": data[i].identity,
            // "state": props.data[i].state,
          }
        })
      }
    // }

    return ({
      "type": "FeatureCollection",
      "features": tempData
    });
  }

  export {data2geojson};