import maplibregl from "maplibre-gl";
import { useState, useRef } from "react";
import styles from "../css_modules/map.module.css";
import { useEffect } from "react";

import collisions from '../data/bham_collisions.json';
import junctions from '../data/bham_junctions.json';

import { collisions2geojson, junctions2geojson } from "../utils/utils";

function Collisions() {

    const map = useRef<any>(null);
    const mapContainer = useRef<any>(null);
    const [lat] = useState(52.452907468939145);
    const [lng] = useState(-1.827910517089181);
    const [zoom] = useState(9);
    const [API_KEY] = useState("2pdGAnnIuClGHUCta2TU");

    useEffect(() => {
      if (map.current) return; //stops map from intializing more than once
  
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
        center: [lng, lat],
        zoom: zoom,
      });

      map.current.on("load", function () {
        map.current.addControl(
          new maplibregl.GeolocateControl({
            positionOptions: {
              enableHighAccuracy: true,
            },
            trackUserLocation: true,
          })
        );

        map.current.addSource("collisions", {
          type: "geojson",
          data:collisions2geojson(collisions),
        });

        map.current.addSource("junctions", {
          type: "geojson",
          data:junctions2geojson(junctions),
        });

        map.current.addLayer({
          id: "unclustered-point",
          type: "circle",
          source: "collisions",
          layout: {
            "circle-sort-key": ["get", "severity_inverse"],
          },
          paint: {
            "circle-color":  [
              "interpolate",
              ["linear"],
              ["get", "severity"],
              0,
              "#f7d756",
              1,
              "#ff4133",
              2,
              "#b23dc4",
              3,
              "#ffbf40",
              4000,
              "#444444"
            ],
            "circle-radius": 6,
            "circle-stroke-width": 1,
            "circle-stroke-color": "#ffffff50",
          },
        });

        map.current.addLayer({
          id: "junctions",
          type: "circle",
          source: "junctions",
          // layout: {
          //   "circle-sort-key": ["get", "severity_inverse"],
          // },
          paint: {
            "circle-color":  [
              "interpolate",
              ["linear"],
              ["get", "score"],
              0,
              "#f7d756",
              1,
              "#ff4133",
              10,
              "#630b0f",
              20,
              "#ffbf40",
              4000,
              "#444444"
            ],
            "circle-radius": 8,
            "circle-stroke-width": 1,
            // "circle-stroke-color": "#ffffff50",
            "circle-stroke-color": "#000",
          },
        });

      });
  

    });
    
    return (
      <div className="main">
            <div ref={mapContainer} className={styles.mapContainer} />
      </div>
    );
  }
  
  export default Collisions;
