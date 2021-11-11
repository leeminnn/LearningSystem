import React, { useState, useEffect } from "react";
import "../Style.css";
import Nav from "../Nav";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { useHistory } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import Autocomplete from "@mui/material/Autocomplete";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

function EditCourse(props) {
  const [courseName, setCourseName] = useState(
    localStorage.getItem("course_name")
  );
  const [prereq, setPrereq] = useState(localStorage.getItem("pre_req"));
  const id = localStorage.getItem("course_id");
  const [desc, setDescription] = useState("");
  const [classList, setClassList] = useState([]);
  const [courseID, setCourseID] = useState("");
  let history = useHistory();

  const checkClear = (reason, value) => {
    if (reason == "clear") {
      setCourseID("No Prerequisite Course");
    } else {
      setCourseID(value.courseID);
    }
  };

  async function getCourseList() {
    axios.get("http://3.18.143.100:5000/all_courses").then((response) => {
      const myList = response.data;
      let temp = [];
      for (let i = 0, len = myList.length, text = ""; i < len; i++) {
        let courseName =
          myList[i].course_name + " (" + myList[i].course_id + ")";
        let courseID = myList[i].course_id;
        temp.push({ label: courseName, courseID: courseID });
      }
      setClassList(temp);
    });

    try {
      const onSubmit = await axios({
        method: "post",
        url: "http://3.18.143.100:5000/course_info",
        data: { course_id: id },
      });
      if (onSubmit.status == 200) {
        setDescription(onSubmit.data[0].course_desc);
      }
      return onSubmit.status;
    } catch (err) {
      console.log(err);
    }
  }

  useEffect(() => getCourseList(), []);

  async function deleteCourse() {
    console.log("delete");
    let data = {
      course_id: id,
    };
    console.log(data);
    try {
      const onSubmit = await axios({
        method: "put",
        url: "http://3.18.143.100:5000/remove", //change endpoint
        data: data,
      });
      if (onSubmit.status === 200) {
        history.push("/course");
      }
      return onSubmit.status;
    } catch (err) {
      console.log(err);
    }
  }

  async function save() {
    if (prereq == "No Prerequisite Course") {
      var data = {
        course_id: id,
        course_name: courseName,
        course_desc: desc,
        pre_req: prereq,
      };
    } else {
      var data = {
        course_id: id,
        course_name: courseName,
        course_desc: desc,
        pre_req: courseID,
      };
    }

    console.log(data);
    try {
      const onSubmit = await axios({
        method: "put",
        url: "http://3.18.143.100:5000/update_course",
        data: data,
      });
      console.log(onSubmit.status);
      if (onSubmit.status == 200) {
        history.push("/course");
      }
    } catch (err) {
      console.log(err);
    }
  }

  console.log(courseID);
  return (
    <div>
      <Nav />
      <div style={{ textAlign: "center" }}>
        <h3>Edit Course</h3>
      </div>
      <div
        style={{
          margin: "0 20%",
          alignItems: "flex-end",
          justifyContent: "flex-end",
          display: "flex",
        }}
      >
        <Button variant="contained" color="error" onClick={deleteCourse}>
          Delete Course
        </Button>
      </div>
      <div className="approve_box">
        <div className="header">
          <div className="text" style={{ alignItems: "baseline" }}>
            <p style={{ marginRight: "10px" }}>({id})</p>
            <TextField
              id="standard-basic"
              variant="standard"
              fullWidth
              value={courseName}
              onChange={(e) => setCourseName(e.target.value)}
              InputProps={{ disableUnderline: true }}
            />
          </div>
        </div>
        <div>
          {/* Loop here */}
          <div className="content">
            <div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  marginBottom: "20px",
                }}
              >
                <div style={{ marginRight: "20px", width: "150px" }}>
                  Prerequisite course:
                </div>
                <Autocomplete
                  disablePortal
                  id="Prerequisites"
                  options={classList}
                  value={prereq}
                  margin="dense"
                  size="small"
                  onChange={(e, value, reason) => {
                    setPrereq(e.target.outerText);
                    checkClear(reason, value);
                    // setCourseID(value.courseID);
                  }}
                  sx={{ width: 300 }}
                  renderInput={(params) => <TextField {...params} />}
                />
              </div>

              <div style={{ display: "flex", alignItems: "center" }}>
                <div style={{ marginRight: "20px", width: "200px" }}>
                  Course Description:
                </div>
                <TextField
                  id="outlined-multiline-flexible"
                  multiline
                  maxRows={4}
                  value={desc}
                  fullWidth
                  id="Course Description"
                  size="small"
                  margin="dense"
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>
            </div>
          </div>
          {/* End Loop here */}

          <div className="approve_button">
            <Button onClick={save} variant="contained">
              Save
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
export default EditCourse;
