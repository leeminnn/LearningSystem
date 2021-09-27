import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Login from './components/Login/Login';
import Home from './components/Learner/Home';
import Admin from './components/Admin/Home';
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Switch>
        <Route path ="/" exact component={Login}/>
        <Route path ="/home" component={Home}/>
        <Route path ="/admin" component={Admin}/>
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);