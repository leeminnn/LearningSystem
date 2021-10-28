import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import TrainerCourseList from './TrainerCourseList';
import Nav from './Nav';
// import './Style.css';

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

function TrainerHome() {
    const [page, setPage] = useState(<TrainerCourseList/>)
    const [value, setValue] = useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div>
          <Nav/>
          <div className="home_body">
             <Box sx={{ width: '100%' }}>
                <Tabs value={value} onChange={handleChange} aria-label="nav tabs example">
                    <LinkTab label="In Progress" />
                    <LinkTab label="Completed" />
                </Tabs>
            </Box>
            {page}
          </div>
        </div>
    )
}
export default TrainerHome