import React, {useState, useEffect} from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import './Trainer.css';
import Nav from './Nav';
import TrainerCourseSection from './TrainerCourseSection';
import Quiz from './Quiz';
import { GrFormAdd } from 'react-icons/gr';
import axios from 'axios';

function TrainerCourse( {match}) {
            
    const [sectionName, setSectionName] = useState('');
    const [materials, setMaterials] = useState('');
    const [sectionList, setSectionList] = useState([])
    const [nextSection, setNextSection] = useState(1);
    const classID = match.params.id
    const [quizID, setQuizID] = useState('')
    const [duration, setDuration] = useState(0)

    const course_id = localStorage.getItem('course_id');

    async function getSectionList(){
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://0.0.0.0:5002/section_info',
                data: {
                    class_id : match.params.id,
                    course_id : course_id
                },
            })
            if (onSubmit.status == 200){
                setSectionList(onSubmit.data)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    useEffect(() => getSectionList(), [])

    const style = {
        width: '100%',
        maxWidth: 360,
        bgcolor: 'background.paper',
    };
    
    const handleClick = (e) => {
        console.log(e.target.innerText)
        setSectionName( e.target.innerText)
    }
    
    async function addSection(){
        const nextID = sectionList[sectionList.length -1].section_id +1
        console.log(nextID)
        
        let data = {
            class_id : classID,
            course_id : course_id,
            section_id : nextID,
            materials : ""
        }
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://0.0.0.0:5002/add_section',
              data: data,
            //   credentials: 'include'
            })
            window.location.reload(false);
            return onSubmit.status
        }
        catch (err) {
          console.log(err);
        }
    };
    async function getQuizID(section_id){
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://0.0.0.0:5002/get_quiz_id',
              data: {
                section_id : section_id,
                class_id : classID,
                course_id : course_id
              },
            })
            if (onSubmit.status === 200){
                setQuizID(onSubmit.data.quiz_id)
                setDuration(onSubmit.data.time)
                console.log(onSubmit.data)
            }
            return onSubmit.status
        }
        catch (err) {
          console.log(err);
        }
        
    };
    return (
        <div>
            <Nav/>
            <div className='title'>
                <h2>Class {classID}</h2>
            </div>
            <div className='main_container'>
                <div className='side_menu'>
                    <List sx={style} component="nav" aria-label="mailbox folders">
                        <div style={{height: '90px', lineHeight: '90px'}}>
                            <h3>Table of Content</h3>
                        </div>
                        <Divider />
                        <div>
                        {sectionList.map(entry => (
                            <ListItem button divider onClick={(e) => {
                                {entry.materials !== null && setMaterials(entry.materials)}
                                setSectionName(entry.section_id)
                                getQuizID(entry.section_id)
                            }}>
                                <ListItemText style={{textAlign:'center'}} primary={'Section '+ entry.section_id} />
                            </ListItem>
                        ))}
                            <ListItem button onClick={addSection}>
                                <ListItemText style={{textAlign:'center'}} value="Add a section">
                                    <GrFormAdd/> 
                                    Add a section 
                                </ListItemText>
                            </ListItem>
                        </div>
                        <Divider light />
                        <div>
                            <ListItem button onClick={handleClick}>
                                <ListItemText style={{textAlign:'center'}} primary="Final Quiz" value="Final Quiz"/>
                            </ListItem>
                        </div>
                    </List>
                </div>
                <div className='right_menu'>
                    {sectionName ==='Final Quiz' ? (
                        <Quiz name={sectionName} quiz_id={parseInt(course_id.toString() + classID.toString())}/>
                    ) : (
                        <div style={{textAlign:'center'}}>
                            <TrainerCourseSection name={sectionName} materials={materials} classID={classID} courseID={course_id} show={false}/>
                            {console.log(parseInt((duration % (60 * 60)) / 60))}
                            <Quiz name={sectionName} classID={classID} quiz_id={quizID} currentHour={parseInt(duration / (60 * 60))} currentMin={parseInt((duration % (60 * 60)) / 60)}/>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
export default TrainerCourse