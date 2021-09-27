import React from 'react';
import { BiUserCircle } from 'react-icons/bi';
import './Style.css';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

function Nav() {

    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };
    return (
        <div>
            <div className="user_dropdown">
                <BiUserCircle size={40} onClick={handleClick}/>
                <span onClick={handleClick}>Username</span>
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
                <MenuItem onClick={handleClose}>Logout</MenuItem>
            </Menu>
        </div>
        
    )
}

export default Nav