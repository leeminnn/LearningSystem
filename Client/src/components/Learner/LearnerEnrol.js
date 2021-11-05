import React, {useState, useEffect} from 'react';
import Nav from './Nav';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import './Learner.css';
import axios from 'axios';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

function LearnerEnrol() {
  
    const date = new Date()
    const courseName = localStorage.getItem("course_name");
    const [classList, setClassList] = useState([])
    const courseID = localStorage.getItem("course_id");
    const emp_id = localStorage.getItem('emp_id')
    const emp_name = localStorage.getItem('emp_name')
    let history = useHistory();


    async function enrollClass(e, entry) {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/enrol',
                data: {
                    emp_id : emp_id,
                    emp_name : emp_name,
                    course_id : entry.course_id,
                    course_name : entry.course_name,
                    class_id : e.target.value
                },
            })
            if (onSubmit.status === 200){
                alert("You have successfully request to enroll in class " + e.target.value + ". Please wait for HR approval.")
                history.push('/l/home')
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    }

    async function getClassList() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/all_eligible_classes',
                data: {course_id: courseID},
            })
            if (onSubmit.status === 200){
                const myList = onSubmit.data
                setClassList(myList)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    useEffect(() => getClassList(), [])
    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>{courseName} Class</h3>
            </div>

            {classList.length === 0 && (
                <h2 style={{textAlign: 'center', marginTop:'50px'}}>No classes for now</h2>
            )}

            {classList.map(entry => (
                <div className='course_list'>
                    <List sx={{ width: '50%', bgcolor: 'background.paper', margin: '0 5%'}}>
                        <ListItem alignItems="flex-start">
                            <ListItemText
                            primary={ "Class " + entry.class_id + " by " +  entry.emp_name}
                            secondary={
                                <Typography
                                sx={{ display: 'inline' }}
                                component="span"
                                variant="body2"
                                color="text.primary"
                                >
                                    {entry.start_enrol.slice(0, 16)} - {entry.end_enrol.slice(0, 16)}
                                </Typography>
                                }
                            />
                        </ListItem>
                    </List>
                    <div className='button'>
                        <Button variant="outlined" value={entry.class_id} onClick={(e) => enrollClass(e, entry)}>Enrol</Button>
                    </div>
                </div>
            ))}
                

        </div>
    )
}

export default LearnerEnrol