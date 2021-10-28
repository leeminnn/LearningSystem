import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Login from './components/Login/Login';
import LearnerHome from './components/Learner/LearnerHome';
import LearnerCourse from './components/Learner/LearnerCourse';
import TrainerHome from './components/Trainer/TrainerHome';
import TrainerCourse from './components/Trainer/TrainerCourse';
import Classes from './components/Admin/Class/Classes';
import ClassList from './components/Admin/Class/ClassList';
import CreateCourse from './components/Admin/Course/CreateCourse';
import HomePage from './components/Admin/HomePage';
import EditCourse from './components/Admin/Course/EditCourse';
import CreateClass from './components/Admin/Class/CreateClass';
import LearnerClass from './components/Learner/LearnerClass';
import TrainerClass from './components/Trainer/TrainerClass';
import LearnerEnrol from './components/Learner/LearnerEnrol';
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Switch>
        <Route path ="/" exact component={Login}/>

        ## learner paths
        <Route path ="/l/home" component={LearnerHome}/>
        <Route path ="/l/course/class" component={LearnerClass}/>
        <Route path ="/l/course/classes/:id" component={LearnerCourse}/>
        <Route path ="/l/course/enrol" component={LearnerEnrol}/>

        ## trainer paths
        <Route path ="/t/home" component={TrainerHome}/>
        <Route path ="/t/course/class" component={TrainerClass}/>
        <Route path ="/t/course/classes/:id" component={TrainerCourse}/>

        ## admin paths
        <Route path ="/course" exact component={HomePage}/>
        <Route path ="/course/create" component={CreateCourse}/>
        <Route path ="/course/edit" component={EditCourse}/>
        <Route path ="/course/classes" component={Classes}/>
        <Route path ="/class/:id" component={ClassList}/>
        <Route path ="/course/class/create" component={CreateClass}/>
        

      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);