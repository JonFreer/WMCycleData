import { Counter, CounterPlus } from "../types/types";

function data2geojson(data: CounterPlus[]) {
  const tempData = [];
  for (let i = 0; i < data.length; i++) {
    tempData.push({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [data[i].lon, data[i].lat],
      },
      properties: {
        identity: data[i].identity,
        today_count: data[i].today_count,
        last_week_count: data[i].last_week_count,
      },
    });
  }

  return {
    type: "FeatureCollection",
    features: tempData,
  };
}

export { data2geojson };
