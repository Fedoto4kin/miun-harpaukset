import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Navbar, ButtonGroup, Button,  Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion, faBookOpen, faInfoCircle } from '@fortawesome/free-solid-svg-icons'
import ReactTooltip from 'react-tooltip';
import ym from 'react-yandex-metrika';

const WordTable = React.lazy(() => import('./Lexicon/WordTable'));
const Made = React.lazy(() => import('./Lexicon/Made'));
const SearchBar = React.lazy(() => import('./Lexicon/SearchBar'));

import history from './history';

export default class Lexicon extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      search: '',
      reverse: false
    };
    
    this.getSearchStr = this.getSearchStr.bind(this);
    if (this.props.match.params.search) this.state.search = this.props.match.params.search;
    if (location.search.includes('reverse')) this.state.reverse = true;

  }

  componentDidMount() {
  	document.title = 'Šanakniiga – Miun harpaukšet karielan kieleh';

   }	

  getSearchStr(srt, rev) {
    this.setState({ search: srt, reverse: rev});
    if (rev) srt += '?reverse'
    history.push(srt); 
    ym('reachGoal', 'search', {search: srt});
  }

  render() {

    return (
    <div>
      <Navbar dark bg="dark">
      <Container>
      <Navbar.Brand>
        <h2  className='text-info' style={{textShadow: "1px 1px #000"}} >
            <FontAwesomeIcon icon={faBookOpen} size="lg"  />
            Tverinkarielan Šanakniiga<sup className='font-italic text-muted'>beta</sup>
        </h2>
      </Navbar.Brand>
        <ButtonGroup  className='float-right'>
             <Button className='btn-primary' data-tip='Avunda' data-for='help-button' >
                <FontAwesomeIcon icon={faInfoCircle} size="lg" />
             </Button>
        </ButtonGroup>
        <ReactTooltip id='help-button' place="left" type="info" border={true} effect="solid" />
       </Container>
      </Navbar>
       <Navbar light bg="light" pt='5' pb='2' mb='1' className='sticky-top'>
      <Container>
      <React.Suspense fallback={<span className="spinner-grow spinner-grow-lg"></span>} >
        <SearchBar
          search={this.state.search}
          reverse={this.state.reverse}
          pushSearchStr={this.getSearchStr}
        />
      </React.Suspense>
      </Container>
      </Navbar>
    <React.Suspense fallback={<div>...</div>} >
      <WordTable search={this.state.search}  reverse={this.state.reverse} />
    </React.Suspense>
    <div style={{height:'4em'}}>
    </div>

      <Navbar dark bg="dark" pt='3' pb='2' mt= '3' className='row-fluid fixed-bottom border-top border-white'>
      <Container>
        <h5  className='text-info'  >Miun harpaukšet karielan kieleh</h5>
       
         <React.Suspense  fallback={<span className="spinner-grow text-info"></span>}> 
               <Made />
        </React.Suspense>

      </Container>
      </Navbar>
      </div>
    );
  }
}
