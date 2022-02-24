import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";

import App from "./components/app";
import "../static/styles/main.scss"

ReactDOM.render(
    <Router>
        <App>
          Cargando
        </App>
    </Router>,
    document.getElementById("root")
);
  