import React, {useState, useEffect} from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Button from '@mui/material/Button';
import FormLabel from '@mui/material/FormLabel';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import axios from 'axios';
import './Learner.css';


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

function DisplayQuiz({quiz_id, quiz_num, questions, class_id, section_id, time}) {
    const quiz = [quiz_id];
    console.log(section_id)
    const [check, setCheck] = useState({});
    const [open, setOpen] = useState(false);
    const course_id = localStorage.getItem('course_id')
    const emp_id = localStorage.getItem('emp_id')
    const totalMarks = (quiz_id['total_mark']);
    const [finalScore, setFinalScore] = useState('');
    const [message, setMessage] = useState('');
    const [seconds, setSeconds] = useState(time);
    const [hours, setHours] = useState(0);
    const [mins, setMins] = useState(0);
    const [sec, setSecs] = useState(0);

    const handleOpen = () => setOpen(true);
    const handleClose = () => {
        setOpen(false);
        window.location.reload(false);
    }
    async function submitQuiz() {
        var score = 0;
        for (const i in check) {
            score+=check[i];
        }
        setFinalScore(score)
        if (score < (totalMarks*0.85)) {
            setMessage("You have fail the quiz")
            var result = "fail"
        }
        else {
            setMessage("You have pass the quiz")
            var result = "pass"
        }
        console.log(data)
        if (section_id!== "") {
            var data = {
                section_id : section_id,
                emp_id : emp_id,
                class_id : class_id,
                course_id : course_id
            }
            var URLink = 'http://0.0.0.0:5002/update_progress'
        } else{
            var data = {
                emp_id : emp_id,
                class_id : class_id,
                result: result,
                course_id : course_id
            }
            var URLink = 'http://0.0.0.0:5000/pass_final_quiz'
        }
        try{
            const onSubmit =
              await axios({
                method: 'put',
                url: URLink,
                data: data,
              })
              if (onSubmit.status === 200){
                handleOpen();
              }
              return onSubmit.status
          }
          catch (err) {
              console.log(err);
          }
    }

    const check_marks = (e, qnID, ans, mark) => {
        if (e.target.value === ans) {
            setCheck(prevState => ({
                ...prevState,
                [qnID]: mark
            }));
        }
        else {
            setCheck(prevState => ({
                ...prevState,
                [qnID]: 0
            }));
        }
    }

    useEffect(() => {
        if (seconds > 0) {
            setTimeout(() => setSeconds(seconds - 1), 1000);
            setHours(Math.floor(seconds / (60 * 60)))
            setMins(Math.floor((seconds % (60 * 60)) / 60))
            setSecs(Math.ceil((seconds % (60 * 60)) % 60 ))
        } else {
            setSeconds('BOOOOM!');
            submitQuiz()
        }
    });
    

    console.log(totalMarks*0.85)

    return (
        <div>
            <div>
                {hours} hours {mins} minutes {sec} seconds
            </div>
            <div className='quiz'>
                { quiz_num != undefined &&
                    <div>
                        {questions.map(entry => (
                            <div className='question' style={{textAlign: 'left'}}>
                                <FormLabel>{entry.quiz_desc} [{entry.mark} mark(s)]</FormLabel>
                                <RadioGroup
                                    aria-label="gender"
                                    defaultValue="female"
                                    name="radio-buttons-group"
                                >   
                                {entry['question_option'].map(option => (
                                    <div>
                                        <FormControlLabel id={entry.qn_id} value={option} control={<Radio />} label={option} onChange={(e) => check_marks(e, entry.qn_id, entry.quiz_ans, entry.mark)} />
                                    </div>
                                ))}
                                </RadioGroup>
                            </div>
                        ))}
                        <div>
                            <Button variant="contained" color="success" onClick={submitQuiz}>
                                Submit
                            </Button>
                            <Modal
                                open={open}
                                onClose={handleClose}
                                aria-labelledby="modal-modal-title"
                                aria-describedby="modal-modal-description"
                            >
                                <Box sx={style}>
                                <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                    {message} with the score of {finalScore}
                                </Typography>
                                </Box>
                            </Modal>
                        </div>
                    </div>
                }
            </div>
        </div>
    )
}

export default DisplayQuiz