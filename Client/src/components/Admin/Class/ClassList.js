import React, {useEffect, useState} from 'react';
import Nav from '../Nav';
import '../Style.css';
import Button from '@mui/material/Button';
import axios from 'axios';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import { DataGrid } from '@mui/x-data-grid';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Autocomplete from '@mui/material/Autocomplete';


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

const columns = [
{ field: 'empid', headerName: 'Employee ID', width: 180 },
{ field: 'name', headerName: 'Name', width: 180 },
{ field: 'progress', headerName: 'Progress', width: 180 },
{ field: 'role', headerName: 'Role', width: 180 },
{ field: 'status', headerName: 'Status', width: 180 }
];


function ClassList( {match} ) {

    const [openApprove, setOpenApprove] = useState(false);
    const [openAssign, setOpenAssign] = useState(false);
    const [nameList, setNameList] = useState([]);
    const [selected, setSelected] = useState([]);
    const [approvee, setApprovee] = useState([]);
    const [classList, setClassList] = useState([])
    const [employeeList, setEmployeeList] = useState([])
    const [approvedName, setApprovedName] = useState([])
    const courseID = localStorage.getItem('course_id')
    const [ID, setID] = useState('');
    const [labelID, setlabelID] = useState('');
    const [learner, setLearner] = useState('');
    const [pending, setPending] = useState([])
    const [totalLearners, setTotalLearners] = useState('');
    const availLearners = localStorage.getItem('intake');
    const today = new Date();
    const [disableButton, setDisableButton] = useState(false);


    async function getClassInfo() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/class_info',
                data: { class_id: match.params.id},
            })
            if (onSubmit.status === 200){
                if (today.getTime() >= new Date(onSubmit.data[0].end_enrol).getTime()) {
                    setDisableButton(true)
                }
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };


    async function getPendingList() {
        try{
            const onSubmit =
              await axios({
                method: 'post',
                url: 'http://localhost:5000/pending_approval',
                data: {class_id: match.params.id, course_id: courseID},
            })
            if (onSubmit.status === 200){
                let tempList = onSubmit.data
                let temp = []
                for (let i = 0, len = tempList.length; i < len; i++){
                    let emp_id = tempList[i].emp_id;
                    let name = tempList[i].emp_name;
                    temp.push([emp_id, name] )
                }
                setPending(temp)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    async function getClassList() {
        let data = {course_id: courseID}
        try{
            const onSubmit =
            await axios({
                method: 'post',
                url: 'http://localhost:5001/get_learners',
                data: data,
              })
              if (onSubmit.status === 200){
                const myList = onSubmit.data
                let temp = []
                for (let i = 0, len = myList.length; i < len; i++){
                    let label = myList[i].emp_name + " (" + myList[i].emp_id + ")"
                    let emp_id = myList[i].emp_id
                    let name = myList[i].emp_name
                    temp.push({label: label, emp_id: emp_id, name:name})
                }
                setEmployeeList(temp)
                }
            }
            catch (err) {
                console.log(err);
            }

        try{
            const onSubmit =
               await axios({
                method: 'post',
                url: 'http://localhost:5000/get_class_list',
                data: {class_id: match.params.id},
            })
            if (onSubmit.status === 200){
                setTotalLearners(onSubmit.data.length)
                let tempList = onSubmit.data
                let temp = []
                for (let i = 0, len = tempList.length; i < len; i++){
                    let emp_id = tempList[i].emp_id;
                    let name = tempList[i].emp_name;
                    let role = tempList[i].class_status;
                    let progress = tempList[i].progress;
                    let status = tempList[i].status;
                    temp.push({ id: emp_id, empid: emp_id, name: name, role: role, progress: progress, status: status })
                }
                setClassList(temp)
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {getClassInfo(); getClassList(); getPendingList()}, [])


    const selectLearners = (ids) => {
        const selectedIDs = new Set(ids);
        const selectedRowData = classList.filter((row) =>
            selectedIDs.has(row.id)
        );
        setSelected(selectedRowData)
    }

    const handleCheckbox = (event) => {
        let information = event.target.value.split(",")
        let emp_id = information[0]
        let name = information[1]
        if ( event.target.checked === true) {
            setApprovee({
                ...approvee,
                [emp_id]: event.target.checked,
            });
            setApprovedName([
                ...approvedName,
                name
            ]);
        }
        else {
            delete approvee[event.target.value[0]]; 
        }
    };
    
    async function withdraw() {
        let data = {learner: selected, class_id: match.params.id, course_id: courseID}
        try{
          const onSubmit =
            await axios({
              method: 'delete',
              url: 'http://localhost:5000/withdraw_learners',
              data: data,
            })
            if (onSubmit.status === 200){
                window.location.reload(false);
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    }

    async function deletePending(temp) {
        let data = {learner: temp, course_id: courseID}
        try{
          const onSubmit =
            await axios({
              method: 'delete',
              url: 'http://localhost:5000/remove_pending',
              data: data,
            })
            if (onSubmit.status === 200){
                window.location.reload(false);
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
        }
    }

    async function approvePending(temp) {
        let data = {learner: temp, class_id: match.params.id, course_id: courseID, learnerName:approvedName}
        if (temp.length < (availLearners - totalLearners)) {
            try{
            const onSubmit =
                await axios({
                method: 'put',
                url: 'http://localhost:5000/enroll_engineer',
                data: data,
                })
            }
            catch (err) {
                console.log(err);
            }

            let info = {emp_id: temp, class_id: match.params.id, course_id: courseID}
            try{
            const onSubmit =
                await axios({
                method: 'post',
                url: 'http://localhost:5002/declare_ungraded_quiz',
                data: info,
                })
                if (onSubmit.status === 200){
                    window.location.reload(false);
                }
                return onSubmit.status
            }
            catch (err) {
                console.log(err);
            }
        }
        else {
            alert("There are only " + (availLearners - totalLearners) + " available slots left")
            window.location.reload(false);
        }
    }

    async function enrolLearners(ID) {
        let data = {learner: ID, class_id: match.params.id, course_id: courseID, learnerName:learner}
        if (ID.length < (availLearners - totalLearners)) {
            try{
                const onSubmit =
                  await axios({
                    method: 'put',
                    url: 'http://localhost:5000/assign_engineer',
                    data: data,
                  })
              }
              catch (err) {
                  console.log(err);
              }
      
              let info = {emp_id: ID, class_id: match.params.id, course_id: courseID}
              try{
                const onSubmit =
                  await axios({
                    method: 'post',
                    url: 'http://localhost:5002/declare_ungraded_quiz',
                    data: info,
                  })
                  if (onSubmit.status === 200){
                      window.location.reload(false);
                  }
                  return onSubmit.status
              }
              catch (err) {
                  console.log(err);
              }
        }
        else {
            alert("There are only " + (availLearners - totalLearners) + " available slots left")
            window.location.reload(false);
        }
    }

    const addPending = () => {
        if (Object.keys(approvee).length > 0){
            let temp = []
            for (let id in approvee){
                temp.push(id)
            }
            approvePending(temp)
            setOpenApprove(false)
        
        } else{
            setOpenApprove(false)
        }
    }

    const removePending = () => {
        if (Object.keys(approvee).length > 0){
            let temp = []
            for (let id in approvee){
                temp.push(id)
            }
            deletePending(temp)
            setOpenApprove(false)
        
        } else{
            setOpenApprove(false)
        }
    }

    const addEmployees = () => {
        if (Object.keys(ID).length > 0) {
            enrolLearners(ID)
            setOpenAssign(false)
        }
        else{
            setOpenAssign(false)
        }
    }

    return (
        <div>
            <Nav/>
            <div style={{textAlign:'center'}}>
                <h3>Class {match.params.id}</h3>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent:'space-evenly', marginBottom:'20px'}}>
                <div style={{float:'left'}}>
                    <Button onClick={()=>setOpenApprove(true)} size="small" color="success" variant="contained" disabled={disableButton} >Pending Approval</Button>
                    <Modal
                        open={openApprove}
                        onClose={()=>setOpenApprove(false)}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <Box sx={style}>
                            <b>Pending Approval:</b>
                            <FormGroup>
                            {pending.map(entry => (
                                <div>
                                    <FormControlLabel key={entry[0]} control={
                                        <Checkbox value={entry} onChange={(e) => handleCheckbox(e)}/>
                                    }
                                    label={entry[1]} />
                                </div>
                            ))}
                            </FormGroup>
                            <div style={{float:'left'}}>
                                <Button size="small" color='error' variant="contained" onClick={removePending}>reject learner</Button>
                            </div>
                            <div style={{float:'right'}}>
                                <Button size="small" variant="contained" onClick={addPending}>Add learner</Button>
                            </div>
                        </Box>
                    </Modal>
                </div>
                <div style={{float:'right'}}>
                    <Button onClick={()=>setOpenAssign(true)} size="small" variant="outlined">Add new Learners</Button>
                    <Modal
                        open={openAssign}
                        onClose={()=>setOpenAssign(false)}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <Box sx={style}>
                            <b>Add Employees:</b>
                            {nameList.map(entry => 
                                <p key={entry}>{entry}</p>
                            )}
                            <div style={{marginBottom: '40px', display: 'flex', alignItems:'center', marginTop:'10px'}}>
                                <Autocomplete
                                    value={labelID}
                                    disableClearable
                                    fullWidth
                                    disablePortal
                                    id="learnerlist"
                                    options={employeeList}
                                    margin="dense"
                                    size="small"
                                    onChange={(e, value)=>{setID([...ID, value.emp_id]); setlabelID(value.label); setLearner([...learner, value.name])}}
                                    renderInput={(params) => <TextField {...params} label="Employee ID" />}
                                />
                                <Button variant="outlined" onClick={()=>{
                                    setNameList([...nameList, labelID])
                                }}>Enter</Button>
                            </div>
                            <div style={{float:'right'}}>
                                <Button size="small" variant="contained" onClick={addEmployees}>Add employees</Button>
                            </div>
                        </Box>
                    </Modal>
                </div>
            </div>
            <div style={{ height: 600, width:'70%'}} className='table'>
                <DataGrid
                    rows={classList}
                    columns={columns}
                    pageSize={10}
                    rowsPerPageOptions={[5]}
                    checkboxSelection
                    onSelectionModelChange={selectLearners}
                />
            </div>
            <div>
                <h4 style={{ display: 'flex', alignItems: 'center', justifyContent:'space-evenly', marginBottom:'20px'}}>
                    <div style={{marginRight:'10px'}}>Total Learners: {totalLearners} </div>
                    Seat Balance: {availLearners - totalLearners}
                    <Button onClick={withdraw} size="small" color="error" variant="contained">Withdraw</Button>
                </h4>
            </div>
        </div>
    )
}

export default ClassList