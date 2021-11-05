import React, {useState, useEffect} from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import axios from 'axios';
import './Trainer.css';


function TrainerCourseSection({name, materials, show, classID, courseID}) {

    const [selectedFile, setSelectedFile] = useState("");
    const [isFilePicked, setIsFilePicked] = useState(show);
    const [status, setStatus] = useState("");

    const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsFilePicked(true);
	};

    useEffect( () => {
        setIsFilePicked(show)
    }, [name])

    async function handleSubmission(){
        // showStatus()
        const formData = new FormData();
		formData.append('filename', selectedFile)
        formData.append('course_id', courseID)
        formData.append('class_id', classID)
        formData.append('section_id', name)
        try{
          const onSubmit =
            await axios({
              method: 'post',
              url: 'http://localhost:5002/upload_materials',
              data: formData,
            })
            if (onSubmit.status === 200){
                showStatus()
            }
            return onSubmit.status
        }
        catch (err) {
            console.log(err);
            setStatus("File not uploaded");
        }
    };

    const Input = styled('input')({
        display: 'none',
    });

    function showStatus() {
        alert("You have successfully uploaded " + selectedFile.name)
        setIsFilePicked(false)
        window.location.reload(false);
    }


    return (
        <div className="section">
            <div className='section_contents'>
                <h2>{ name !='' && <span>Section {name} </span>}</h2>
                <div>
                    <a href={materials}>{materials}</a>
                </div>
                { name !='' &&
                    <div className='box'>
                        <div>
                            <h2>{isFilePicked}</h2>
                            {isFilePicked ? (
                                <div>
                                    <p>Filename: {selectedFile.name}</p>
                                </div>
                            ) : (
                                <p>Select a file to show details</p>
                            )}
                            <label htmlFor="contained-button-file">
                                <Input accept=".zip" id="contained-button-file" multiple type="file" onChange={changeHandler}/>
                                <Button variant="contained" component="span">
                                    Upload
                                </Button>
                            </label>
                        </div>
                        <div>
                            <Button variant="contained" color="success" onClick={handleSubmission}>
                                Submit
                            </Button>
                        </div>
                    </div>
                }
            </div>
        </div>
    )
}
export default TrainerCourseSection