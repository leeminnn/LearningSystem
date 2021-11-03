import React, { useState, useEffect } from 'react';
import Nav from '../Nav';
import '../Style.css';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import axios from 'axios';


function CreateCourse() {
    const [courseName, setCourseName] = useState('');
    const [prereq, setPrereq] = useState('');
    const [desc, setDescription] = useState('');
    const [classList, setClassList] = useState([]);
    const [courseID, setCourseID] = useState('');
    let history = useHistory();

    const getCourseList =() => {
        axios.get('http://0.0.0.0:5000/all_courses')
        .then((response) => {
            const myList = response.data
            let temp = []
            for (let i = 0, len = myList.length, text = ""; i < len; i++){
                let courseName = myList[i].course_name + " (" + myList[i].course_id + ")"
                let courseID = myList[i].course_id
                temp.push({label: courseName, courseID: courseID})
            }
            setClassList(temp)
        });
    };

    const checkClear = (reason, value) => {
        if (reason =='clear'){
            setCourseID('No Prerequisite Course')
        }
        else {
            setCourseID(value.courseID)
        }
    }

    useEffect(() => getCourseList(), [])

    async function create(){
        let data = {
            course_name: courseName,
            course_desc : desc,
            pre_req : courseID
        }
        console.log(data)
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://0.0.0.0:5000/add_course',
              data: data,
            })
            if (onSubmit.status == 200){
                history.push('/course')
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    console.log(courseID)
    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>Create Course</h3>
            </div>
            <div className='create_box'>
                <div className='box_content'>
                    <div style={{marginBottom:'20px'}}>
                        <div>Enter Course Name</div>
                        <div style={{width: '60%'}}>
                            <TextField value={courseName} fullWidth label="Course Name" id="Course Name" size="small" margin="dense" onChange={(e)=>setCourseName(e.target.value)}/>
                        </div>
                    </div>
                    <div style={{marginBottom:'20px'}}>
                        <div>Enter Course Description</div>
                        <div style={{width: '60%'}}>
                            <TextField id="outlined-multiline-flexible"
                            multiline
                            maxRows={4} 
                            value={desc} 
                            fullWidth 
                            label="Course Description" 
                            id="Course Description" 
                            size="small" margin="dense" 
                            onChange={(e)=>setDescription(e.target.value)}/>
                        </div>
                    </div>
                    <div className='pre_req'>
                        <div>Enter Prerequisite courses if have</div>
                        <div style={{width: '60%', marginTop:'10px'}}>
                            <Autocomplete
                                disablePortal
                                id="Prerequisites"
                                options={classList}
                                margin="dense"
                                size="small"
                                value={prereq}
                                onChange={(e, value, reason)=>{
                                    setPrereq(e.target.outerText); 
                                    checkClear(reason, value)
                                    // setCourseID(value.courseID); 
                                }}
                                // sx={{ width: 300 }}
                                renderInput={(params) => <TextField {...params} label="Courses" />}
                            />
                        </div>
                    </div>
                    <div style={{justifyContent:'flex-end', alignItems: 'flex-end', display:'flex'}}>
                        <Button variant="outlined" onClick={create}>Create Course</Button>
                    </div>
                </div>
                
            </div>
        </div>
    )
}

export default CreateCourse 