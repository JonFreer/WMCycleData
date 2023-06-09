import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import Map from './components/map';

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import About from './pages/about';
import Counter from './components/counter';
import Counters from './pages/counters';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <App></App>,
    errorElement: <App />,
    children: [
      {
        path: "/",
        element: <Map />,
      },
      {
        path: "/counter",
        element: <Counters />,
      },
      {
        path: "/counters",
        element: <Counters />,
      },
      {
        path: "counter/:idenitiy",
        element: <Counter />,
      },
      {
        path: "/about",
        element: <About ></About>
      },
      {
        path: "*",
        element: <Map />,
      },
    ],
  },

]);

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
