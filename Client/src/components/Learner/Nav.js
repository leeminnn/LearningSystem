import React from 'react';
import { BiUserCircle } from 'react-icons/bi';
import './Learner.css';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { Link } from "react-router-dom";

function Nav() {

    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const emp_id = localStorage.getItem('emp_id')
    return (
        <div className='Learner_Nav'>
            <div style={{width: '80%', display: 'inline-block'}}>
                <Link to={'/l/home'}
                    style={{textDecoration: 'none', color: 'white'}}
                >
                    <h3>All-In-One</h3>
                    <h3>Learning Management System</h3>
                </Link>
            </div>
            <div style={{float: 'right', marginTop:'50px'}}>
                <div className="user_dropdown">
                    <BiUserCircle size={40} onClick={handleClick}/>
                    <span onClick={handleClick}>Employee ID: {emp_id}</span>
                </div>
                <Menu
                    id="basic-menu"
                    anchorEl={anchorEl}
                    open={open}
                    onClose={handleClose}
                    MenuListProps={{
                    'aria-labelledby': 'basic-button',
                    }}
                >
                    <MenuItem onClick={handleClose}>Profile</MenuItem>
                    <Link to={'/'}
                        style={{textDecoration: 'none', color: 'black'}}
                    >
                        <MenuItem onClick={handleClose}>Logout</MenuItem>
                    </Link>
                </Menu>
            </div>
            
        </div>
        
    )
}

export default Nav