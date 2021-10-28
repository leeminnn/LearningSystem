import React, {useState} from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import LearnerCourseList from './LearnerCourseList';
import './Learner.css';
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

function LearnerHome() {

    const [page, setPage] = useState(<LearnerCourseList courses='all_courses'/>)
    const [value, setValue] = useState(0);

    const handleChange = (event, newValue) => {
      if (newValue === 1){
        setPage(<LearnerCourseList courses='eligible'/>)
      } else if (newValue === 2) {
        setPage(<LearnerCourseList courses='in_progress'/>)
      } else if (newValue === 3 ) {
        setPage(<LearnerCourseList courses='completed'/>)
      } else if (newValue === 0 ) {
        setPage(<LearnerCourseList courses='all_courses'/>)
      }
      setValue(newValue);
    };

    return (
        <div>
          <Nav/>
          <div className="home_body">
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
        </div>
    )
}

export default LearnerHome
