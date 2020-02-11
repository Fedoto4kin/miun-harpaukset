import React, { Component } from "react";
import ReactDOM from "react-dom";
import {Router, Route, syncHistoryWithStore, routerReducer} from "react-router-dom";
import { Navbar, ButtonGroup, Button,  Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion, faBookOpen } from '@fortawesome/free-solid-svg-icons'

import history from './history';

const WordTable = React.lazy(() => import('./WordTable'));
const About = React.lazy(() => import('./About'));
const SearchBar = React.lazy(() => import('./SearchBar'));


class FilterableWordTable extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      filterText: '',
      search: '',
      loading: false
    };
    
    this.handleFilterTextChange = this.handleFilterTextChange.bind(this);
    this.onFilterTextKeyPress = this.onFilterTextKeyPress.bind(this);
    this.onClickButton = this.onClickButton.bind(this);
  }

  componentDidMount() {
    if (this.props.match.params.search) { 
      this.setState({ filterText: this.props.match.params.search});
      this.setState({ search: this.props.match.params.search});
    }
  }

  onFilterTextKeyPress(e) {

    this.setState({ filterText: e.target.value}); 
    if(e.charCode==13){
      this.setState({ search:  e.target.value});
      history.push( e.target.value )
      e.preventDefault();
    }
  }

  onClickButton(e) {
      this.setState({ search: this.state.filterText});
      history.push(this.state.filterText);
      e.preventDefault();
  }

  handleFilterTextChange(filterText) { 
    this.setState({ filterText: filterText}); 
  }
  
  render() {

    return (
    <div>

          <Navbar dark bg="dark">
          <Container>
          <Navbar.Brand>
            <h2  className='text-info' style={{textShadow: "1px 1px #000"}} >
            <FontAwesomeIcon icon={faBookOpen} size="lg"  /> Šanakniiga</h2></Navbar.Brand>
            <ButtonGroup  className='float-right'>
              <Button disabled={true} className='btn-light' size="lg" ><FontAwesomeIcon icon={faCogs} size="lg" /></Button>
            &nbsp; 
             <React.Suspense  fallback={<span className="spinner-grow spinner-grow-sm"></span>}> 
            <About />
            </React.Suspense>
            </ButtonGroup>
           
           </Container>
          </Navbar>
           <Navbar light bg="light" pt='5' pb='2' mb='1' className='sticky-top'>
          <Container>
          <React.Suspense fallback='<div>...</div>'>
            <SearchBar
              filterText={this.state.filterText}
              onFilterTextChange={this.handleFilterTextChange}
              onFilterTextKeyPress={this.onFilterTextKeyPress}
              onClickButton={this.onClickButton}
            />
          </React.Suspense>
          </Container>
          </Navbar>
        <React.Suspense  fallback={<div>Pannah...</div>}>
          <WordTable search={this.state.search} />
        </React.Suspense>
        <div style={{height:'4em'}}>
        </div>

          <Navbar dark bg="dark" pt='3' pb='2' mt= '3' className='row-fluid fixed-bottom border-top border-white'>
          <Container>
            <h5  className='text-info'  >Miun harpaukšet karielan kieleh</h5>
          </Container>
          </Navbar>
      </div>
    );
  }
}

document.body.classList.add('bg-light');
ReactDOM.render((<Router history={history}>
     <Route exact path="/:search?" component={FilterableWordTable} >
     </Route>
  </Router>
  ), document.getElementById('app'));