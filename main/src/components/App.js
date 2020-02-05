import React, { Component } from "react";
import ReactDOM from "react-dom";
import axios from 'axios';
import { Navbar, Form, InputGroup, ButtonGroup, Button, Card, Container, Alert } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion, faBookOpen } from '@fortawesome/free-solid-svg-icons'


import { WordCard } from './WordCard'; 
import { SearchBar } from './SearchBar'; 
import { About } from './About'; 

class WordTable extends React.Component {
  render() {

    const filterText = this.props.filterText;
    const rows = [];

    const wordCount = this.props.words.length;
    let message = null;

    if (filterText) {
      if (wordCount) {
        message = 'On löydän ' + wordCount;
        message += ((wordCount > 1) ?  ' šanoida': ' šano')
      } else
        message = 'Ei nimidä löydän';
    } 


    this.props.words.forEach((word) => {
      rows.push(
        <WordCard
          word={word}
          key={word.id} 
        />
      );
    });



    return (<Container>
      { (filterText.length && !this.props.loading ) > 0 && <Alert className='text-center alert alert-secondary show'>{message}</Alert> } 
      { this.props.loading ?
        <Card.Columns style={{opacity: 0.5}}>{rows}</Card.Columns> :
        <Card.Columns>{rows}</Card.Columns> 
      }
      </Container>
    );
  }
}

class FilterableWordTable extends React.Component {

  constructor(props) {
    super(props);
    this._timeout =  null;
    this._wait = 800;
    this.state = {
      filterText: '',
      'words': [],
      'loading': false
    };
    
    this.handleFilterTextChange = this.handleFilterTextChange.bind(this);
  }

  handleFilterTextChange(filterText) {

   if (this._timeout) this._timeout = null;

   this.setState({ 'loading': true  });
   this.setState({
      filterText: filterText
    });

   if (this.state.filterText == '') { 

      this.setState({ 'words': []  }); 
      this._timeout = null;

   } else {

      this._timeout = setTimeout(() => {
        axios.get("/api/v0/lexicon", { params: {search: this.state.filterText}})
          .then((response) => {
            this.setState({ 'words': response.data  });
            this.setState({ 'loading': false  });
          });
      }, this._wait);
   }

  }


  
  render() {

    return (
    <div>

          <Navbar expand="lg" dark bg="dark">
          <Container>
          <Navbar.Brand>
            <h2  className='text-info' style={{textShadow: "1px 1px #000"}} >
            <FontAwesomeIcon icon={faBookOpen} size="lg"  /> Šanakniiga</h2></Navbar.Brand>
            <ButtonGroup  className='float-right'>
              <Button disabled={true} className='btn-light' size="lg" ><FontAwesomeIcon icon={faCogs} size="lg" /></Button>
            &nbsp;  
            <About />
            </ButtonGroup>
           
           </Container>
          </Navbar>
           <Navbar expand="lg" light bg="light" pt='5' pb='3' mb= '3' className='sticky-top'>
          <Container>
            <SearchBar
              filterText={this.state.filterText}
              onFilterTextChange={this.handleFilterTextChange}
              loading={this.state.loading}
            />
          </Container>
          </Navbar>
      
        <WordTable
          words={this.state.words}
          filterText={this.state.filterText}
          loading={this.state.loading}
        />

      </div>
    );
  }
}

document.body.classList.add('bg-light');
ReactDOM.render(
  <FilterableWordTable />,
  document.getElementById('app')
);