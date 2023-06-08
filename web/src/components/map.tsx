import maplibregl from 'maplibre-gl';
import React, { useRef, useEffect, useState } from 'react';
import 'maplibre-gl/dist/maplibre-gl.css';
import styles from '../css_modules/map.module.css'
// const map = new maplibregl.Map({
//     container: 'map',
//     style: 'https://demotiles.maplibre.org/style.json', // stylesheet location
//     center: [-74.5, 40], // starting position [lng, lat]
//     zoom: 9 // starting zoom
//     });

function Map(){

    const map = useRef<any>(null);
    const mapContainer = useRef<any>(null);
    const [lng] = useState(139.753);
    const [lat] = useState(35.6844);
    const [zoom] = useState(14);
    const [API_KEY] = useState('2pdGAnnIuClGHUCta2TU');

    useEffect(() => {
        if (map.current) return; //stops map from intializing more than once
        
        map.current = new maplibregl.Map({
          container: mapContainer.current,
          style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
          center: [lng, lat],
          zoom: zoom
        });
      
      });

    return(
         <div ref={mapContainer} className={styles.mapContainer} />
    );
}

export default Map;