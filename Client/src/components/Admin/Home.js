import React from 'react';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import './Style.css';
import {TiTick, TiGroup, TiUserAdd, TiEdit, TiUserDelete, TiFolderAdd} from 'react-icons/ti';

function Admin() {
    return (
        <div>
            <Box sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    '& > :not(style)': {
                    m: 5,
                    width: 128,
                    height: 128,
                    },
            }}>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiFolderAdd size={70}/></div>
                        Create Courses
                    </div>
                </Paper>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiTick size={70}/></div>
                        Approve Learners
                    </div>
                </Paper>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiGroup size={70}/></div>
                        Assign Trainers
                    </div>
                </Paper>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiUserAdd size={70}/></div>
                        Assign Learners
                    </div>
                </Paper>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiEdit size={70}/></div>
                        Edit Courses
                    </div>
                </Paper>
                <Paper elevation={3}>
                    <div className='cards'>
                        <div><TiUserDelete size={70}/></div>
                        Withdraw Learners
                    </div>
                </Paper>
            </Box>
        </div>
    )
}

export default Admin