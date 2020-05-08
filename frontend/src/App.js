import React from 'react';
import './App.css';
import StyledDropzone from './StyledDropzone'
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import {Detail} from "./Detail";

function App() {
    return (
        <div id="body">
            <header>
                <h1>detector</h1>
            </header>
            <Router>
                <div>
                    <Switch>
                        <Route exact path="/">
                            <StyledDropzone/>
                        </Route>
                        <Route path="/detail">
                            <Detail/>
                        </Route>
                    </Switch>
                </div>
            </Router>
        </div>
    );
}

export default App;
