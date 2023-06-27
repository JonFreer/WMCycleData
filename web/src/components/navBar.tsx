import React from "react";
import { Link } from "react-router-dom";
import styles from "../css_modules/navBar.module.css";
class NavBar extends React.Component<{}, {}> {
  render() {
    return (
      <div className={styles.navBar}>
        <Link className={styles.title} to="/">
          WMCD
          <div className={styles.beta}>Beta</div>
        </Link>

        <Link className={styles.link} to="/counters">
          Counters
        </Link>

        <Link className={styles.link} to="/about">
          About
        </Link>
      </div>
    );
  }
}

export default NavBar;
