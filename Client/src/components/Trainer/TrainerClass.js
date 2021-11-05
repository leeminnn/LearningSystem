import React, {useState, useEffect} from 'react';
import Nav from './Nav';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import { Link } from "react-router-dom";
import './Trainer.css';
import axios from 'axios';

function TrainerClass() {
    const courseName = localStorage.getItem("course_name");
    const [classList, setClassList] = useState([])
    const courseID = localStorage.getItem("course_id");
    const emp_id = localStorage.getItem("emp_id");
    let history = useHistory();

    async function getClassList() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/get_classes',
                data: {course_id: courseID, emp_id: emp_id},
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

    useEffect(() => getClassList(), [])
    
    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>{courseName} Class</h3>
            </div>

            {classList.map(entry => (
                <div className='course_list'>
                    <List sx={{ width: '50%', bgcolor: 'background.paper', margin: '0 5%'}}>
                        <ListItem alignItems="flex-start">
                            <ListItemText
                            primary={"Class " + entry.class_id+ " by " +  entry.emp_name}
                            secondary={
                                <Typography
                                sx={{ display: 'inline' }}
                                component="span"
                                variant="body2"
                                color="text.primary"
                                >
                                    {entry.start_date.slice(0, 16)} - {entry.end_date.slice(0, 16)}
                                </Typography>
                                }
                            />
                        </ListItem>
                    </List>
                    <div style={{display:'flex', margin: '2% 5%', justifyContent:'space-between'}}>
                        <div style={{float:'left'}}>
                            <Button variant="outlined" value={entry.class_id} onClick={(e) => history.push("/t/course/classlist/" + e.target.value)}>View Class List</Button>
                        </div>
                        <div style={{float:'right'}}>
                            <Button variant="outlined" value={entry.class_id} onClick={(e) => history.push("/t/course/classes/" + e.target.value)}>View Class Materials</Button>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}

export default TrainerClass