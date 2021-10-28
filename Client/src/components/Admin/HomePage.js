import React, {useState, useEffect} from 'react';
import './Style.css';
import Nav from './Nav';
import Button from '@mui/material/Button';
import { Link } from "react-router-dom";
import axios from 'axios';

function HomePage () {
    const [classList, setClassList] = useState([])

    const nextPage = (e) => {
        localStorage.setItem('course_id', e.entry.course_id);
        localStorage.setItem('course_name', e.entry.course_name);
        localStorage.setItem('pre_req', e.entry.pre_req);
    }

    const getClassList =() => {
        axios.get('http://localhost:5000/all_courses')
        .then((response) => {
            const myList = response.data
            setClassList(myList)
        });
    };

    useEffect(() => getClassList(), [])
    console.log(classList)

    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>Courses</h3>
            </div>
            <div style={{ margin: '0 20%', alignItems:'flex-end', justifyContent:'flex-end', display:'flex'}}>
                <Link to='/course/create'
                    style={{textDecoration: 'none'}}
                >
                    <Button variant="outlined">Create Course</Button>
                </Link>
            </div>

            {classList.map(entry => (
                <div className='course_box'>
                    <div className='header'>
                        <div className='text'>
                            <b>({entry['course_id']}) {entry['course_name']}</b>
                        </div>
                    </div>
                    <div>
                        <div className='content'>
                            <p>Pre-Requisite course: {entry['pre_req']}</p>
                            <p>Course Description: {entry['course_desc']}</p>
                        </div>
                        <div className='button'>
                            <Link to = '/course/edit'
                            style={{textDecoration: 'none'}}>
                                <Button onClick={() => nextPage({entry})} variant="outlined" style={{margin:'0 30px'}}>Edit</Button>
                            </Link>

                            <Link to ='/course/classes'
                            style={{textDecoration: 'none'}}>
                                <Button onClick={() => nextPage({entry})} variant="contained">View</Button>
                            </Link>
                        </div>
                    </div>
                </div>
            ))}

        </div>
    )
}

export default HomePage 
