import React, {useState, useEffect} from 'react';
import Nav from './Nav';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import './Learner.css';
import axios from 'axios';

function LearnerClass() {

    const today = new Date();
    const courseName = localStorage.getItem("course_name");
    const [classList, setClassList] = useState([])
    const courseID = localStorage.getItem("course_id");
    const emp_id = localStorage.getItem('emp_id')
    let history = useHistory();

    async function getClassList() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://3.18.143.100:5000/get_learner_classes',
                data: {course_id: courseID, emp_id:emp_id},
            })
            if (onSubmit.status === 200){
                setClassList(onSubmit.data)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    async function withdraw(class_id) {
        let data = {learner: [{empid: emp_id}], class_id:class_id, course_id: courseID}
        try{
          const onSubmit =
            await axios({
              method: 'delete',
              url: 'http://3.18.143.100:5000/withdraw_learners',
              data: data,
            })
            if (onSubmit.status === 200){
                history.push("/l/home")
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    }

    useEffect(() => getClassList(), [])

    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>{courseName} Class</h3>
            </div>

            {/* loop here */}
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
                    {(today.getTime() < (new Date(entry.end_enrol).getTime())) && (
                        <div style={{marginLeft:"5%", marginBottom: '2%'}}>
                            <Button variant="contained" color='error' value={entry.class_id} onClick={(e) =>withdraw(e.target.value)}>Withdraw</Button>
                        </div>
                    )}
                    {(today.getTime() < (new Date(entry.start_date).getTime())) ? (
                        <div className='button'>
                            <Button variant="outlined" value={entry.class_id} onClick={(e) => history.push("/l/course/classes/" + e.target.value)} disabled>View</Button>
                        </div>
                    ) : (
                        <div className='button'>
                            <Button variant="outlined" value={entry.class_id} onClick={(e) => history.push("/l/course/classes/" + e.target.value)}>View</Button>
                        </div>
                    )}
                    
                </div>
            ))}
            
            {/* end of loop */}
        </div>
    )
}

export default LearnerClass