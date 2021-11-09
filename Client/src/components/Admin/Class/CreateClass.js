import React, { useState, useEffect } from 'react';
import Nav from '../Nav';
import '../Style.css';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import DateRangePicker from '@wojtekmaj/react-daterange-picker';
import Button from '@mui/material/Button';
import { useHistory } from "react-router-dom";
import axios from 'axios';


function CreateClass() {
    const [inputFieldClass, setInputFieldClass] = useState([new Date(), new Date()]);
    const [inputFieldEnrol, setInputFieldEnrol] = useState([new Date(), new Date()]);
    const [startClass, setStartClass] = useState();
    const [endClass, setEndClass] = useState();
    const [startEnrolment, setStartEnrolment] = useState();
    const [endEnrolment, setEndEnrolment] = useState();
    const [size, setSize] = useState('');
    const [trainerList, setTrainerList] = useState([]);
    // this is for emp_id
    const [ID, setID] = useState('');
    const [labelID, setlabelID] = useState('');
    const [trainerName, setTrainerName]= useState('');

    const course_id = localStorage.getItem('course_id')
    let history = useHistory();

    const inputClassDate =(e) => {
        setStartClass(e[0].toISOString().slice(0, 10).replace('T', ' '))
        setEndClass(e[1].toISOString().slice(0, 10).replace('T', ' '))
        setInputFieldClass([e[0], e[1]])
    }

    const inputEnrolmentDate =(e) => {
        setStartEnrolment(e[0].toISOString().slice(0, 10).replace('T', ' '))
        setEndEnrolment(e[1].toISOString().slice(0, 10).replace('T', ' '))
        setInputFieldEnrol([e[0], e[1]])
    }


    const getClassList =() => {
        axios.get('http://18.235.179.159:5001/get_trainers')
        .then((response) => {
            const myList = response.data
            let temp = []
            for (let i = 0, len = myList.length, text = ""; i < len; i++){
                let label = myList[i].emp_name + " (" + myList[i].emp_id + ")"
                let emp_id = myList[i].emp_id
                let name = myList[i].emp_name
                temp.push({label: label, emp_id: emp_id, name:name})
            }
            setTrainerList(temp)
        });
    };

    useEffect(() => getClassList(), [])

    async function create(){
        let data = {
            intake : size,
            emp_id : ID,
            emp_name: trainerName,
            course_id: course_id,
            start_date: startClass,
            end_date: endClass,
            start_enrol: startEnrolment,
            end_enrol: endEnrolment
        }

        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://18.235.179.159:5000/create_class',
              data: data,
            })
            if (onSubmit.status === 200){
                history.push('/course/classes')
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
            <div style={{textAlign:'center'}}>
                <h3>Create Class</h3>
            </div>
            <div className='create_box'>
                <div className='box_content'>
                    <div style={{marginBottom:'20px'}}>
                        <div style={{marginBottom: '10px'}}>Enter Trainer ID</div>
                        <div style={{width: '60%'}}>
                            <Autocomplete
                                value={labelID}
                                disablePortal
                                id="Prerequisites"
                                options={trainerList}
                                margin="dense"
                                size="small"
                                onChange={(e, value)=>{setID(value.emp_id); setlabelID(value.label); setTrainerName(value.name)}}
                                renderInput={(params) => <TextField {...params} label="Trainers" />}
                            />
                        </div>
                    </div>
                    <div className='pre_req'>
                        <div>Class Size</div>
                        <div style={{width: '60%'}}>
                            <TextField value={size} fullWidth label="Class Size" id="Class Size" size="small" margin="dense" onChange={(e)=>setSize(e.target.value)}/>
                        </div>
                    </div>
                    <div className='date_picker'>
                        <p>Enter Class Duration</p>
                        <DateRangePicker 
                            onChange={(e)=>inputClassDate(e)}
                            value={inputFieldClass}
                            />
                    </div>
                    <div className='date_picker'>
                        <p>Enter Enrolment Period</p>
                        <DateRangePicker 
                            onChange={(e)=>inputEnrolmentDate(e)}
                            value={inputFieldEnrol}
                            />
                    </div>
                    <div style={{justifyContent:'flex-end', alignItems: 'flex-end', display:'flex'}}>
                        <Button variant="outlined" onClick={create}>Create Class</Button>
                    </div>
                </div>
                
            </div>
        </div>
    )
}

export default CreateClass 