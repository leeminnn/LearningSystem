import React, {useState, useEffect} from 'react';
import Divider from '@mui/material/Divider';
import TextField from '@mui/material/TextField';
import './Trainer.css';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import axios from 'axios';


function Quiz({name, classID, quiz_id}) {

    const [marks, setMarks] = useState(1);
    const [question, setQuestion] =useState();
    const [answer, setAnswer] = useState();
    const [first, setFirst] = useState();
    const [second, setSecond] = useState();
    const [third, setThird] = useState();
    const [questionQuiz, setQuestionQuiz] = useState([]);
    const [quizID, setQuizID] = useState(quiz_id)
    console.log(quiz_id)
    const course_id = localStorage.getItem('course_id')
    const class_id = classID
    const [count, setCount] = useState(0)

    const handleChange = (event) => {
        setMarks(event.target.value);
    };

    async function handleSubmit(){
        let question_option = answer
        if (first != ""){
            question_option = question_option.concat(",",first)
        }
        if (second != ""){
            question_option = question_option.concat(",",second)
        }
        if (third != ""){
            question_option = question_option.concat(",",third)
        }
        const formData = {
            "quiz_id" :  quiz_id,
            'question': question,
            'answer': answer,
            'question_option' : question_option,
            'mark': marks
        }
        console.log(formData)
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://localhost:5002/create_question',
              data: formData,
            })
            if (onSubmit.status === 200){
                setMarks(1);
                setQuestion();
                setAnswer();
                setFirst();
                setSecond();
                setThird();
                setCount(count+1)
            }
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
                  quiz_id : quiz_id
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
    console.log(questionQuiz)
    useEffect(() => getQuestions(), [quiz_id])
    useEffect(() => getQuestions(), [count])
    return (
        <div className='quiz_details'>
            {name !== '' &&
                <div className='section_contents'>
                    {name === 'Final Quiz' && <h2>{name}</h2>}
                    <div>
                        {questionQuiz.map((entry, index) => 
                            <div>
                                <h5>Question {index +1}</h5>
                                <div>Question Description : {entry.quiz_desc}</div>
                                <div>Question Answer : {entry.quiz_ans}</div>
                                <div> Question Options : {entry.question_option}</div>
                            </div>
                        )}
                    </div>
                    <div style={{marginBottom: '30px', marginTop: '30px'}}>
                        <Divider/>
                    </div>
                    <div className="quiz_content">
                        <div className="option">
                            Create a question
                            <TextField fullWidth label="Question" size="small" margin="dense" onChange={(event) => {setQuestion(event.target.value)}}/>
                        </div>
                        <div  className="question">
                            <div className="option">
                                Answer
                                <TextField
                                    fullWidth
                                    hiddenLabel
                                    id="filled-hidden-label-normal"
                                    size="small"
                                    margin="dense"
                                    onChange={(event) => {setAnswer(event.target.value)}}
                                />
                            </div>
                            <div className="option">
                                Option 1
                                <TextField
                                    fullWidth
                                    hiddenLabel
                                    id="filled-hidden-label-normal"
                                    size="small"
                                    margin="dense"
                                    onChange={(event) => {setFirst(event.target.value)}}
                                />
                            </div>
                            <div className="option">
                                Option 2
                                <TextField
                                    fullWidth
                                    hiddenLabel
                                    id="filled-hidden-label-normal"
                                    size="small"
                                    margin="dense"
                                    onChange={(event) => {setSecond(event.target.value)}}
                                />
                            </div>
                            <div className="option">
                                Option 3
                                <TextField
                                    fullWidth
                                    hiddenLabel
                                    id="filled-hidden-label-normal"
                                    size="small"
                                    margin="dense"
                                    onChange={(event) => {setThird(event.target.value)}}
                                />
                            </div>
                            <div style={{width: '100px', marginTop:'30px'}}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="demo-simple-select-label">Marks</InputLabel>
                                        <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={marks}
                                        label="Marks"
                                        onChange={handleChange}
                                        >
                                        <MenuItem value={1}>1</MenuItem>
                                        <MenuItem value={2}>2</MenuItem>
                                        <MenuItem value={3}>3</MenuItem>
                                        <MenuItem value={4}>4</MenuItem>
                                        <MenuItem value={5}>5</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Box>
                            </div>
                        </div>
                    </div>
                    <div style={{textAlign:'right', marginRight: '60px', marginBottom: '30px'}}>
                        <Button variant="outlined" onClick={handleSubmit}>
                            Add question
                        </Button>
                    </div>
                </div>
            }
        </div>
    )
}
export default Quiz