import { Counter } from "../types/types";

function data2geojson(data:Counter[]) {

    const tempData = []
    for (let i = 0; i < data.length; i++) {

        tempData.push({
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [data[i].lon, data[i].lat]
          }, "properties": {
            "identity": data[i].identity,
          }
        })
      }

    return ({
      "type": "FeatureCollection",
      "features": tempData
    });
  }

  export {data2geojson};