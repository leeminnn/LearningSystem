import React, {useState} from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Course from './Course';
import './Style.css';
import Nav from './Nav';

function LinkTab(props) {
    return (
      <Tab
        component="a"
        onClick={(event) => {
          event.preventDefault();
        }}
        {...props}
      />
    );
}

function Home() {

    const [page, setPage] = useState(<Course/>)
    const [value, setValue] = useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div className="home_body">
          <Nav/>
             <Box sx={{ width: '100%' }}>
                <Tabs value={value} onChange={handleChange} aria-label="nav tabs example">
                    <LinkTab label="All" />
                    <LinkTab label="Eligible" />
                    <LinkTab label="In Progress" />
                    <LinkTab label="Completed" />
                </Tabs>
            </Box>
            {page}
        </div>
    )
}

export default Home
