import maplibregl from 'maplibre-gl';
import React, { useRef, useEffect, useState, useReducer } from 'react';
import 'maplibre-gl/dist/maplibre-gl.css';
import styles from '../css_modules/map.module.css'
import { Counter } from '../types/types';
import { data2geojson } from '../utils/utils';
import { useCounters } from '../App';
import { useNavigate } from 'react-router-dom';


function Map() { 

    const counters  = useCounters();
    const map = useRef<any>(null);
    const mapContainer = useRef<any>(null);
    const [lat] = useState(52.452907468939145);
    const [lng] = useState(-1.727910517089181);
    const [zoom] = useState(9);
    const [API_KEY] = useState('2pdGAnnIuClGHUCta2TU');
    const forceUpdate = useReducer(x => x + 1, 0)[1]
    const navigate = useNavigate();

    useEffect(() => {
        if (map.current && counters.length > 0) {
            const source = map.current.getSource("counters")
            if (source != undefined) {
                source.setData(data2geojson(counters));
            }
        }
    })

    useEffect(() => {
        if (map.current) return; //stops map from intializing more than once

        map.current = new maplibregl.Map({
            container: mapContainer.current,
            style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
            center: [lng, lat],
            zoom: zoom
        });

        map.current.on('load', function () {

            map.current.addControl(
                new maplibregl.GeolocateControl({
                    positionOptions: {
                        enableHighAccuracy: true
                    },
                    trackUserLocation: true
                })
            );

            console.log("Creating counters", counters.length)

            map.current.addSource('counters', {
                'type': 'geojson',
                data: data2geojson([]),
            });

            map.current.addLayer({
                id: 'unclustered-point',
                type: 'circle',
                source: 'counters',
                paint: {
                    'circle-color': '#3291fc',
                    'circle-radius': 10,
                    'circle-stroke-width': 4,
                    'circle-stroke-color': '#3291fc50'
                }

            });

            map.current.on('click', 'unclustered-point', function (e:any) {
                
                var identity = e.features[0].properties.identity;
                console.log(e)
                console.log(e.features)
                navigate("/counter/"+identity, { replace: true })
            })

            forceUpdate() //force update to reload the source
        })

    });

    return (
        <div ref={mapContainer} className={styles.mapContainer} />
    );
}

export default Map;