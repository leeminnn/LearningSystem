import React, {useState} from 'react';
import IconButton from '@mui/material/IconButton';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputLabel from '@mui/material/InputLabel';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import { BiShow, BiHide  } from 'react-icons/bi';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';
import { Link } from "react-router-dom";
import Radio from '@mui/material/Radio';
import './Login.css';



function Login() {

    
    const [checked, setChecked] = useState(false);
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [visibility, setVisibility] = useState(false)
    const [role, setRole] = useState("")

    const handleUsername = e => {
        setUsername(e.target.value);
    };

    const handlePassword = e => {
        setPassword(e.target.value)
    };

    const handleClickShowPassword = () => {
        if (visibility === false){
            setVisibility(true)
        }
        else {
            setVisibility(false)
        }
    };

    const handleCheck = () => {
        if (checked === false){
            setChecked(true)
            // localStorage.setItem('rememberMe', rememberMe);
        }
        else {
            setChecked(false)
        }
    }

    const handleRole = e => {
        setRole(e.target.value)
    }

    return (
        <div>
            <div className='Login_Nav'>
                <h3>All-In-One</h3>
                <h3>Learning Management System</h3>
            </div>
            <div className="login_form">
                <div className='role'>
                    <p>I am a</p>
                    <div style={{display: 'flex'}}>
                        <div>
                            <Radio
                                checked={role === 'learner'}
                                onChange={handleRole}
                                value="learner"
                                name="radio-buttons"
                                inputProps={{ 'aria-label': 'A' }}
                            /> Learner
                        </div>
                        <div>
                            <Radio
                                checked={role === 'trainer'}
                                onChange={handleRole}
                                value="trainer"
                                name="radio-buttons"
                                inputProps={{ 'aria-label': 'B' }}
                            /> Trainer
                        </div>
                        
                    </div>
                </div>
            </div>
            <div className='username' >
                <p>Enter your username</p>
                <TextField 
                    label="Username"
                id="outlined-size-normal margin-none"
                defaultValue={username}
                onChange={handleUsername}
                size="small"
                fullWidth 
                />
                
            </div>
            <div className='password'>
                <p>Enter your password</p>
                <FormControl variant="outlined" fullWidth >
                    <InputLabel htmlFor="outlined-adornment-password" size="small" >Password</InputLabel>
                    <OutlinedInput
                        id="outlined-adornment-password margin-none"
                        type={visibility ? 'text' : 'password'}
                        value={password}
                        onChange={handlePassword}
                        size="small" 
                        endAdornment={
                        <InputAdornment position="end">
                            <IconButton
                            aria-label="toggle password visibility"
                            onClick={handleClickShowPassword}
                            edge="end"
                            >
                                {visibility ? <BiHide /> : <BiShow />}
                            </IconButton>
                        </InputAdornment>
                        }
                        label="Password"
                    />
                </FormControl>
            </div>
            <div className="login_form">
                <div className='remember'>
                    <Checkbox
                        checked={checked}
                        onChange={handleCheck}
                        inputProps={{ 'aria-label': 'controlled' }}
                    />
                    Remember Me
                </div>
            </div>
            <div className='Login_button'>
                <Link to={"home"}>
                    <Button 
                    variant="contained"
                    style={{width:'20%'}}
                    >Login</Button>
                </Link>
            </div>
        </div>
    )
}

export default Login