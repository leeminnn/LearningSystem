import React, {useState, useEffect} from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import './Learner.css';
import ProgressBar from "@ramonak/react-progress-bar";
import Nav from './Nav';
import DisplayQuiz from './DisplayQuiz';
import axios from 'axios';

const style = {
    width: '100%',
    maxWidth: 360,
    bgcolor: 'background.paper',
};

function LearnerCourse({match}) {
    const [sectionName, setSectionName] = useState('')
    const [progress, setProgress] = useState(10)
    const [sectionList, setSectionList] = useState([])
    const emp_Id = localStorage.getItem('emp_id')
    const [materials, setMaterials] = useState('')
    const [desc, setDesc] = useState('')
    const course_id = localStorage.getItem('course_id')
    const [quiz_id, setQuizID] = useState('')
    const [questionQuiz, setQuestionQuiz] = useState([]);
    const [sectionID, setSectionID] = useState('')

    async function getQuizID(e){
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://localhost:5002/get_quiz_id',
              data: {
                    // quiz_type =
                    section_id : e,
                    class_id : match.params.id,
                    course_id : course_id
                },
            })
            if (onSubmit.status == 200){
                setQuizID(onSubmit.data)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    async function getQuestions(){
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5002/get_questions',
                data: {
                  quiz_id : quiz_id['quiz_id']
                },
              })
              if (onSubmit.status === 200){
                const myList = onSubmit.data
                let temp = []
                for (let i = 0, len = myList.length, text = ""; i < len; i++){
                    console.log(myList[i])
                    temp.push(myList[i])
                }
                setQuestionQuiz(temp)
              }
              return onSubmit.status
          }
          catch (err) {
            console.log(err);
          }
    }
    useEffect(() => getQuestions(), [quiz_id])
    console.log(questionQuiz)
    console.log(quiz_id)
    async function getSectionList(){
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5002/get_user_sections',
                data: {
                    class_id : match.params.id,
                    course_id : course_id,
                    emp_id : emp_Id
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

    async function getProgress() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/learner_progress',
                data: {emp_id : emp_Id, class_id : match.params.id},
              })
              if (onSubmit.status == 200){
                  console.log(onSubmit.data)
                  setProgress(onSubmit.data.progress)
              }
              return onSubmit.status
          }
          catch (err) {
              console.log(err);
          }
    };

    useEffect(() => {getSectionList(); getProgress()}, [])
    console.log(quiz_id['quiz_id'])
    return (
        <div>
            <Nav/>
            <div className='title'>
                <h2> Class {match.params.id}</h2>
                <div style={{width: '60%', margin:'auto'}}> 
                    <ProgressBar bgColor="#6a1b9a" completed={progress} />
                </div>
            </div>
            <div className='main_container'>
                <div className='side_menu'>
                    <List sx={style} component="nav" aria-label="mailbox folders">
                        <div style={{height: '90px', lineHeight: '90px'}}>
                            <h3>Table of Content</h3>
                        </div>
                        <Divider />
                        {sectionList.map(entry => (
                            <ListItem button divider onClick={(e) => {
                                    getQuizID(entry.section_id);
                                    setSectionID(entry.section_id)
                                    setSectionName('Section ' + entry.section_id); 
                                    setMaterials(entry.materials); 
                                    setDesc(entry.section_desc);
                                    
                                }}>
                                <ListItemText style={{textAlign:'center'}} primary={'Section '+ entry.section_id} />
                            </ListItem>
                        ))}
                        <Divider light />
                        { progress == 100 &&
                            <ListItem button onClick={()=> {
                                setSectionName('Final Quiz');
                                setDesc("You have 30 minutes to complete this quiz which would determine your final grade for this module.")
                                getQuizID(" ")

                            }}>
                                <ListItemText style={{textAlign:'center'}} primary="Final Quiz" />
                            </ListItem>
                        }
                    </List>
                </div>
                <div className='section_details'>
                    <h3>{sectionName}</h3>
                    <h4>{desc}</h4>
                    { sectionName != 'Final Quiz' && (
                        <a href={materials}>{materials}</a>
                    )}
                    <DisplayQuiz quiz_id={quiz_id} quiz_num={quiz_id['quiz_id']} questions={questionQuiz} class_id={match.params.id} section_id={sectionID}/>
                </div>
            </div>
        </div>
    )
}
export default LearnerCourse