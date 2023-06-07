import React, { useRef, useEffect, useState, ChangeEvent } from 'react';
import { Link } from 'react-router-dom';
// import './navbar.css'
import styles from '../css_modules/navBar.module.css'
class NavBar extends React.Component<{}, {}> {

    render() {
        return (<div className={styles.navBar}>
            <Link className={styles.title} to="/">
                West Midlands Cycle Data

                <div className={styles.beta}>Beta</div>
            </Link>

            {/* <button className='navBar_button'> */}

            <Link className={styles.link} to="/about">
                About
            </Link>

            {/* <Link className='navBar_submit' to="/submit">
                <IoMdAddCircle className={"navBar_icon"}></IoMdAddCircle>Contribute
            </Link> */}

            {/* </button> */}
        </div>)
    }
}

export default NavBar;