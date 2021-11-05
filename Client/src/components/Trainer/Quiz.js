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


function Quiz({name, classID, quiz_id, currentHour, currentMin}) {

    const [marks, setMarks] = useState(1);
    const [question, setQuestion] =useState();
    const [answer, setAnswer] = useState();
    const [first, setFirst] = useState();
    const [second, setSecond] = useState();
    const [third, setThird] = useState();
    const [questionQuiz, setQuestionQuiz] = useState([]);
    const [count, setCount] = useState(0)
    const [currentMarks, setCurrentMarks] = useState(0)
    const [hour, setHour] = useState(0);
    const [minutes, setMinutes] = useState(0);

    const handleChange = (event) => {
        setMarks(event.target.value);
    };

    const handleHour = (event) => {
        setHour(event.target.value);
    };
    const handleMinutes = (event) => {
        setMinutes(event.target.value);
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
        if (name === 'Final Quiz') {
            var URLink = 'http://localhost:5002/create_final_quiz_question';
        } else {
            var URLink = 'http://localhost:5002/create_question';
        }
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: URLink,
              data: formData,
            })
            if (onSubmit.status === 200){
                setMarks(1);
                setQuestion("");
                setAnswer("");
                setFirst("");
                setSecond("");
                setThird("");
                setCount(count+1)
            }
        }
        catch (err) {
          console.log(err);
        }
    };

    async function submitTime(){
        let duration = (hour * 3600 ) + (minutes*60)
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5002/update_quiz_time',
                data: {
                  quiz_id : quiz_id,
                  time : duration
                },
              })
              return onSubmit.status
          }
          catch (err) {
            console.log(err);
          }
    }

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
                let marks = 0
                for (let i = 0, len = myList.length; i < len; i++){
                    marks += myList[i]['mark']
                    temp.push(myList[i])
                }
                setQuestionQuiz(temp)
                setCurrentMarks(marks)
              }
          }
          catch (err) {
            console.log(err);
          }
    }
    
    useEffect(() => {
        getQuestions();
        if (parseInt(currentMin) > 0){
            setMinutes(parseInt(currentMin));
        }
        if (parseInt(currentHour) > 0){
            setHour(parseInt(currentHour));
        }

    }, [quiz_id])

    useEffect(() => getQuestions(), [count])
    return (
        <div className='quiz_details'>
            {name !== '' &&
                <div className='section_contents'>
                    {name === 'Final Quiz' && 
                        <div>
                            <h2>{name}</h2>
                            {currentMarks <50 ? (
                                <h3>You need {50 - currentMarks} more marks</h3>
                            ) : currentMarks === 50 ? (
                                <h3>Stop adding questions</h3>
                            ) : (
                                <h3>You have exceeded by {currentMarks - 50} marks</h3>
                            )}
                        </div>
                    }
                    <div style={{textAlign:'left', marginLeft:'10%'}}>
                        {questionQuiz.map((entry, index) => 
                            <div>
                                <h5>Question {index +1}</h5>
                                <div>Question Description : {entry.quiz_desc}</div>
                                <div>Question Answer : {entry.quiz_ans}</div>
                                <div> Question Options : {entry.question_option}</div>
                                <div> Marks : {entry.mark}</div>
                            </div>
                        )}
                    </div>
                    { name!== 'Final Quiz' && (
                        <div style={{marginLeft:'10%', marginTop:'3%', textAlign:'left'}}>
                            Enter duration of Quiz:
                            <div style={{display:'flex', alignItems:'center', marginTop:'10px'}}>
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={hour}
                                        onChange={handleHour}
                                        >
                                        {Array.from(Array(2), (e, i) => {
                                            return <MenuItem value={i}>{i}</MenuItem>
                                        })}
                                        </Select>
                                    </FormControl>
                                </Box> Hour(s)
                                <Box sx={{ minWidth: 120 }}>
                                    <FormControl fullWidth>
                                        <Select
                                        labelId="demo-simple-select-label"
                                        id="demo-simple-select"
                                        value={minutes}
                                        onChange={handleMinutes}
                                        >
                                        {Array.from(Array(60), (e, i) => {
                                            return <MenuItem value={i}>{i}</MenuItem>
                                        })}
                                        </Select>
                                    </FormControl>
                                </Box> Minutes(s)
                                <Button variant="contained" color="success" onClick={submitTime}>
                                    Enter
                                </Button>
                            </div>
                        </div>
                    )}
                    
                    
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