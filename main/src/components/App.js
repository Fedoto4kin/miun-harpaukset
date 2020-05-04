import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Router, Route, syncHistoryWithStore, routerReducer } from "react-router-dom";
import { YMInitializer } from 'react-yandex-metrika';

import history from './history';
import Lexicon from './Lexicon';


document.body.classList.add('bg-light');

ReactDOM.render((<Router history={history}>
     <Route exact path="/:search?" component={Lexicon} >
     </Route>
     <YMInitializer accounts={[61458964]} />
  </Router>
  ), document.getElementById('app'));