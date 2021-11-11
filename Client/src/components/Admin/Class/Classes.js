import React, { useState, useEffect } from "react";
import Nav from "../Nav";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useHistory } from "react-router-dom";
import { Link } from "react-router-dom";
import axios from "axios";
import "../Style.css";

function Classes(props) {
  const [courseName, setCourseName] = useState(
    localStorage.getItem("course_name")
  );
  const [preReq, setPreReq] = useState(localStorage.getItem("pre_req"));
  const courseID = localStorage.getItem("course_id");
  const [classList, setClassList] = useState([]);
  let history = useHistory();

  async function getClassList() {
    try {
      const onSubmit = await axios({
        method: "post",
        url: "http://3.18.143.100:5000/all_classes",
        data: { course_id: courseID },
      });
      if (onSubmit.status == 200) {
        setClassList(onSubmit.data);
      }
      return onSubmit.status;
    } catch (err) {
      console.log(err);
    }
  }

  useEffect(() => getClassList(), []);
  console.log(classList);
  return (
    <div>
      <Nav />
      <div style={{ textAlign: "center" }}>
        <h3>{courseName} Classes</h3>
      </div>
      <div
        style={{
          margin: "0 20%",
          alignItems: "flex-end",
          justifyContent: "flex-end",
          display: "flex",
        }}
      >
        <Link to="/course/class/create" style={{ textDecoration: "none" }}>
          <Button variant="outlined">Create Class</Button>
        </Link>
      </div>

      {classList.map((entry) => (
        <div className="course_list">
          <List
            sx={{ width: "50%", bgcolor: "background.paper", margin: "0 5%" }}
          >
            <ListItem alignItems="flex-start">
              {console.log(entry)}
              <ListItemText
                primary={"Class " + entry.class_id + " by " + entry.emp_name}
                secondary={
                  <Typography
                    sx={{ display: "inline" }}
                    component="span"
                    variant="body2"
                    color="text.primary"
                  >
                    {entry.start_date.slice(0, 16)} -{" "}
                    {entry.end_date.slice(0, 16)}
                  </Typography>
                }
              />
            </ListItem>
          </List>
          <div className="button">
            <Button
              variant="outlined"
              value={entry.class_id}
              onClick={(e) => {
                history.push("/class/" + e.target.value);
                localStorage.setItem("intake", entry.intake);
              }}
            >
              View
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Classes;
