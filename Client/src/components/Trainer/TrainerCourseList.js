import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './Trainer.css';
import { Link } from "react-router-dom";

function TrainerCourseList({courses}) {
    console.log(courses)
    const url = 'http://localhost:5000/get_trainer_' + courses + '_courses';
    const nextPage = (e) => {
        localStorage.setItem('course_id', e.entry.course_id);
        localStorage.setItem('course_name', e.entry.course_name);
        localStorage.setItem('pre_req', e.entry.pre_req);
    }
    const [classList, setClassList] = useState([])
    const emp_id = localStorage.getItem('emp_id')

    async function getClassList() {
        try{
            const onSubmit =
                await axios({
                method: 'post',
                url: url,
                data: {emp_id: emp_id},
                })
                if (onSubmit.status == 200){
                    setClassList(onSubmit.data)
                }
                return onSubmit.status
            }
            catch (err) {
                console.log(err);
            }
        
    }

    useEffect(() => getClassList(), [courses])

    return (
        <div className='list_course'>
            {classList.map(entry => (
                <div>
                    <Link to ={'course/class'}
                    style={{textDecoration: 'none'}}
                    >
                        <h3 onClick={() => nextPage({entry})}>({entry['course_id']}) {entry['course_name']}</h3>
                    </Link>
                    <p>Pre-Requisite course: {entry['pre_req']}</p>
                    <p>Description</p>
                </div>
            ))}
        </div>
    )
}
export default TrainerCourseList