import React from 'react';
import { Login, Main } from './containers';
import { render } from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { injectGlobal } from 'styled-components';

injectGlobal`
  body {
    padding: 0;
    margin: 0;
    font-family: 'Roboto';
  }
`

const root = document.getElementById('root');
render(
  <Router>
    <Switch>
      <Route exact path='/' component={Main} />
      <Route path='/login' component={Login} />
    </Switch>
  </Router> 
, root);