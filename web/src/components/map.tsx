import maplibregl from "maplibre-gl";
import { useRef, useEffect, useState, useReducer } from "react";
import "maplibre-gl/dist/maplibre-gl.css";
import styles from "../css_modules/map.module.css";
import { data2geojson } from "../utils/utils";
import { useCounters } from "../App";
import { useNavigate } from "react-router-dom";
import { renderToString } from "react-dom/server";

function Map({ identity }: { identity: number | undefined }) {
  const counters = useCounters();
  const map = useRef<any>(null);
  const popup = useRef<any>(null);
  const popup_hover = useRef<any>(null);
  const mapContainer = useRef<any>(null);
  const [lat] = useState(52.452907468939145);
  const [lng] = useState(-1.827910517089181);
  const [zoom] = useState(9);
  const [API_KEY] = useState("2pdGAnnIuClGHUCta2TU");

  const forceUpdate = useReducer((x) => x + 1, 0)[1];
  const navigate = useNavigate();
  const [marker, setMarker] = useState<any>();
  const max = Math.max(...counters.map((val) => val.last_week_count));

  const [filterVal, setFilterVal] = useState<number>(0);

  useEffect(() => {
    if (map.current && counters.length > 0) {
      const source = map.current.getSource("counters");
      if (source !== undefined) {
        source.setData(data2geojson(counters));
      }
    }
  });

  useEffect(() => {
    if (marker !== undefined) {
      var counter = counters.filter((x) => x.identity === identity)[0];
      (marker as maplibregl.Marker).setLngLat([counter.lon, counter.lat]);
      (map.current as maplibregl.Map).setCenter([counter.lon, counter.lat]);
      (map.current as maplibregl.Map).setZoom(16);
      // (map.current as maplibregl.Map).removeLayer("unclustered-point");
      map.current.setFilter("unclustered-point", [
        "all",
        ["!=", "identity", Number(identity)],
        [">=", "last_week_count", Number(filterVal)],
      ]);
    }
  }, [identity]);

  // Update styling based on filter val
  useEffect(() => {
    if (map.current !== null) {
      if (map.current._isReady) {
        map.current.setFilter("unclustered-point", [
          "all",
          ["!=", "identity", Number(identity)],
          [">=", "last_week_count", Number(filterVal)],
        ]);
      }
    }
  }, [filterVal]);

  useEffect(() => {
    if (map.current) return; //stops map from intializing more than once

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
      center: [lng, lat],
      zoom: zoom,
    });

    map.current._isReady = false;

    map.current.on("load", function () {
      map.current.addControl(
        new maplibregl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true,
          },
          trackUserLocation: true,
        })
      );

      console.log("Creating counters", counters.length);

      map.current.addSource("counters", {
        type: "geojson",
        data: data2geojson([]),
      });

      map.current.addLayer({
        id: "unclustered-point",
        type: "circle",
        source: "counters",
        filter: [
          "all",
          ["!=", "identity", Number(identity)],
          [">", "last_week_count", filterVal],
        ],
        layout: {
          "circle-sort-key": ["get", "last_week_count"],
        },
        paint: {
          "circle-color": [
            "interpolate",
            ["linear"],
            ["get", "last_week_count"],
            0,
            "#f7d756",
            500,
            "#F2845C",
            1000,
            "#8f0da3",
            2000,
            "#5700A4",
            4000,
            "#444444"
          ],
          "circle-radius": 10,
          "circle-stroke-width": 1,
          "circle-stroke-color": "#ffffff50",
        },
      });

      if (identity !== undefined) {
        var counter = counters.filter((x) => x.identity === identity)[0];

        var marker = new maplibregl.Marker({
          color: "#FF3333",
          draggable: false,
        })
          .setLngLat([counter.lon, counter.lat])
          .addTo(map.current);

        setMarker(marker);

        (map.current as maplibregl.Map).setCenter([counter.lon, counter.lat]);
        (map.current as maplibregl.Map).setZoom(16);
      }

      map.current.on("click", "unclustered-point", function (e: any) {
        // Remove old popup to remove double binding onclick
        if (popup.current != null) {
          popup.current.remove();
        }

        var coordinates = e.features[0].geometry.coordinates.slice();
        var today_count = e.features[0].properties.today_count;
        var last_week_count = e.features[0].properties.last_week_count;
        var identity = e.features[0].properties.identity;

        popup.current = new maplibregl.Popup({ closeButton: false });

        let html = renderToString(
          <>
            <div className={styles.popup_holder}>
              <div>
                <div> Today </div>
                <div className={styles.popup_text_main}> {today_count}</div>
              </div>
              <div>
                <div> Last Week </div>
                <div className={styles.popup_text_main}> {last_week_count}</div>
              </div>
            </div>
            <div id="popup_button" className={styles.popup_button}>
              More Data ...
            </div>
          </>
        );

        popup.current
          .setLngLat([coordinates[0], coordinates[1]])
          .setHTML(html)
          .addTo(map.current);

        document
          .getElementById("popup_button")
          ?.addEventListener("click", () => navigate("/counter/" + identity));
      });

      map.current.on("mousemove", "unclustered-point", (e: any) => {
        var identity = e.features[0].properties.identity;

        if (popup_hover.current !== null) {
          if (identity === popup_hover.current.identity) {
            return;
          }
          popup_hover.current.remove();
        }

        map.current.getCanvas().style.cursor = "pointer";
        var coordinates = e.features[0].geometry.coordinates.slice();
        var today_count = e.features[0].properties.today_count;
        var last_week_count = e.features[0].properties.last_week_count;

        popup_hover.current = new maplibregl.Popup({ closeButton: false });

        let html = `<div class=${styles.popup_holder_hover}> 
                      <div>
                        <div> Today </div>
                        <div class=${styles.popup_text_main}>  ${today_count}</div>
                      </div>
                      <div>
                        <div> Last Week </div>
                        <div class=${styles.popup_text_main}>  ${last_week_count}</div>
                      </div>
                     </div>`;

        popup_hover.current.identity = identity;

        popup_hover.current
          .setLngLat([coordinates[0], coordinates[1]])
          .setHTML(html)
          .addTo(map.current);
      });

      map.current.on("mouseleave", "unclustered-point", () => {
        map.current.getCanvas().style.cursor = "grab";
        if (popup_hover.current != null) {
          popup_hover.current.remove();
          popup_hover.current = null;
        }
      });

      map.current._isReady = true;
      forceUpdate(); //force update to reload the source
    });
  });

  return (
    <>
      <div ref={mapContainer} className={styles.mapContainer} />
      {identity === undefined ? (
        <>
          <Settings
            max={max}
            val={filterVal}
            callback={(val: number) => setFilterVal(val)}
          ></Settings>
          <Key></Key>
        </>
      ) : (
        <></>
      )}
    </>
  );
}

function Settings({
  max,
  val,
  callback,
}: {
  max: number;
  val: number;
  callback: any;
}) {
  return (
    <div className={styles.settings_holder}>
      <div className={styles.settings}>
        <div className={styles.settings_header}>
          <span className={styles.settings_header_left}>Filter Counters</span>
          <span className={styles.settings_header_right}>{val} / Week</span>
        </div>
        <input
          onChange={(val) => callback(val.target.value)}
          className={styles.settings_range}
          type="range"
          min="0"
          max={max}
          defaultValue={val}
          id="myRange"
        />
      </div>
    </div>
  );
}

function Key() {
  return (
    <div className={styles.key_holder}>
      Cyclists /w
      <div className={styles.key_item}>
        <i style={{ background: "#444444" }} className={styles.key_colour}></i>
        4000
      </div>
      <div className={styles.key_item}>
        <i style={{ background: "#5700A4" }} className={styles.key_colour}></i>
        2000
      </div>
      <div className={styles.key_item}>
        <i style={{ background: "#8f0da3" }} className={styles.key_colour}></i>
        1000
      </div>
      <div className={styles.key_item}>
        <i style={{ background: "#F2845C" }} className={styles.key_colour}></i>
        500
      </div>
      <div className={styles.key_item}>
        <i style={{ background: "#f7d756" }} className={styles.key_colour}></i>
        0
      </div>
    </div>
  );
}

export default Map;
