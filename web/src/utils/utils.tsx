import { CounterPlus } from "../types/types";

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

function collisions2geojson(data: any) {
  const tempData = [];
  for (let i = 0; i < data.length; i++) {
    tempData.push({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [data[i].longitude, data[i].latitude],
      },
      properties: {
        severity: Number(data[i].severity),
        severity_inverse: -Number(data[i].severity),
        // today_count: data[i].today_count,
        // last_week_count: data[i].last_week_count,
      },
    });
  }

  return {
    type: "FeatureCollection",
    features: tempData,
  };
}

function junctions2geojson(data: any) {
  const tempData = [];
  for (let i = 0; i < data.length; i++) {
    tempData.push({
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [data[i].lon, data[i].lat],
      },
      properties: {
        score: Number(data[i].score),
      },
    });
  }

  return {
    type: "FeatureCollection",
    features: tempData,
  };
}


export { data2geojson, collisions2geojson,junctions2geojson };
