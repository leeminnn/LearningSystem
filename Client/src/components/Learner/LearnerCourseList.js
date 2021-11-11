import React, {useState, useEffect} from 'react';
import axios from 'axios';
import './Learner.css';
import { Link } from "react-router-dom";

function LearnerCourseList({courses}) {
    const emp_id = localStorage.getItem('emp_id')
    const url = 'http://3.18.143.100:5000/' + courses;
    const nextPage = (e) => {
        localStorage.setItem('course_id', e.entry.course_id);
        localStorage.setItem('course_name', e.entry.course_name);
        localStorage.setItem('pre_req', e.entry.pre_req);
    }
    const [classList, setClassList] = useState([])
    const [pending, setPending] = useState([])

    async function getClassList() {
        if (courses === 'eligible') {
            try{
                const onSubmit =
                await axios({
                    method: 'post',
                    url: url,
                    data: {emp_id : emp_id},
                })
                if (onSubmit.status === 200){
                      setClassList(onSubmit.data.eligible)
                      setPending(onSubmit.data.Pending)
                }
                return onSubmit.status
            }
            catch (err) {
                console.log(err);
            }
        }
        else{
            try{
                const onSubmit =
                await axios({
                    method: 'post',
                    url: url,
                    data: {emp_id : emp_id},
                })
                if (onSubmit.status === 200){
                      setClassList(onSubmit.data)
                }
                return onSubmit.status
            }
            catch (err) {
                console.log(err);
            }
        }
    }

    useEffect(() => getClassList(), [courses])

    return (
        <div className='list_course'>
                {classList.map(entry => (
                    <div style={{marginTop:'50px'}}>
                        {courses === "eligible" ? (
                            <Link to ='course/enrol'
                            style={{textDecoration: 'none'}}
                            >
                                <h3 onClick={() => nextPage({entry})}>({entry['course_id']})   {entry['course_name']}</h3>
                            </Link>
                        ) : courses === 'all_courses' ? (
                            <h3>({entry['course_id']})   {entry['course_name']}</h3>
                        ) : (
                            <Link to ='course/class'
                            style={{textDecoration: 'none'}}
                            >
                                <h3 onClick={() => nextPage({entry})}>({entry['course_id']})   {entry['course_name']}</h3>
                            </Link>
                        )}
                        <p>Pre-Requisite course: {entry['pre_req']}</p>
                        <p>Description: {entry['course_desc']}</p>
                    </div>
                ))}
                { courses === 'eligible' &&
                    pending.map(entry => (
                        <div style={{marginTop:'50px'}}>
                            <h3>({entry['course_id']})   {entry['course_name']}</h3>
                            <p>Pre-Requisite course: {entry['pre_req']}</p>
                            <p>Description: {entry['course_desc']}</p>
                        </div>
                    ))
                }
               
        </div>
    )
}

export default LearnerCourseList
