import React from 'react';
import './Style.css';
import { Link } from "react-router-dom";

function Nav() {
    return (
        <div className='Nav_bar'>
            <div style={{width: '80%', display: 'inline-block'}}>
                <Link to={'/course'}
                    style={{textDecoration: 'none', color: 'white'}}
                >
                    <h3>All-In-One</h3>
                    <h3>Learning Management System</h3>
                </Link>
            </div>
            <div style={{float: 'right', marginTop:'50px'}}>
                <Link to={"/"}
                        style={{textDecoration: 'none', color: "white"}}
                >
                    <h3>User Login</h3>
                </Link>
            </div>
        </div>
    )
}
export default Nav