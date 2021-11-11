import React, { useEffect, useState } from "react";
import Nav from "./Nav";
// import '../Style.css';
import Button from "@mui/material/Button";
import axios from "axios";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import TextField from "@mui/material/TextField";
import { DataGrid } from "@mui/x-data-grid";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
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

const columns = [
  { field: "empid", headerName: "Employee ID", width: 180 },
  { field: "name", headerName: "Name", width: 180 },
  { field: "progress", headerName: "Progress", width: 180 },
  { field: "role", headerName: "Role", width: 180 },
  { field: "status", headerName: "Status", width: 180 },
];

function TrainerClassList({ match }) {
  const [selected, setSelected] = useState([]);
  const [classList, setClassList] = useState([]);
  const [employeeList, setEmployeeList] = useState([]);
  const courseID = localStorage.getItem("course_id");
  const [totalLearners, setTotalLearners] = useState("");
  const availLearners = localStorage.getItem("intake");

  async function getClassList() {
    let data = { course_id: courseID };
    try {
      const onSubmit = await axios({
        method: "post",
        url: "http://3.18.143.100:5001/get_learners",
        data: data,
      });
      if (onSubmit.status === 200) {
        const myList = onSubmit.data;
        let temp = [];
        for (let i = 0, len = myList.length; i < len; i++) {
          let label = myList[i].emp_name + " (" + myList[i].emp_id + ")";
          let emp_id = myList[i].emp_id;
          let name = myList[i].emp_name;
          temp.push({ label: label, emp_id: emp_id, name: name });
        }
        setEmployeeList(temp);
      }
    } catch (err) {
      console.log(err);
    }

    try {
      const onSubmit = await axios({
        method: "post",
        url: "http://3.18.143.100:5000/get_class_list",
        data: { class_id: match.params.id },
      });
      if (onSubmit.status === 200) {
        setTotalLearners(onSubmit.data.length);
        console.log(onSubmit.data);
        let tempList = onSubmit.data;
        let temp = [];
        for (let i = 0, len = tempList.length; i < len; i++) {
          let emp_id = tempList[i].emp_id;
          let name = tempList[i].emp_name;
          let role = tempList[i].class_status;
          let progress = tempList[i].progress;
          let status = tempList[i].status;
          temp.push({
            id: emp_id,
            empid: emp_id,
            name: name,
            role: role,
            progress: progress,
            status: status,
          });
        }
        setClassList(temp);
      }
      return onSubmit.status;
    } catch (err) {
      console.log(err);
    }
  }

  useEffect(() => {
    getClassList();
  }, []);

  const selectLearners = (ids) => {
    const selectedIDs = new Set(ids);
    const selectedRowData = classList.filter((row) => selectedIDs.has(row.id));
    setSelected(selectedRowData);
  };

  return (
    <div>
      <Nav />
      <div style={{ textAlign: "center" }}>
        <h3>Class {match.params.id}</h3>
      </div>
      <div style={{ height: 600, width: "70%" }} className="table">
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
        <h4
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-evenly",
            marginBottom: "20px",
          }}
        >
          <div style={{ marginRight: "10px" }}>
            Total Learners: {totalLearners}{" "}
          </div>
          Seat Balance: {availLearners - totalLearners}
        </h4>
      </div>
    </div>
  );
}

export default TrainerClassList;
