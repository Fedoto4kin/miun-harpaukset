import React, { Component } from "react";
import ReactDOM from "react-dom";
import axios from 'axios';
import { Navbar, Form, InputGroup, ButtonGroup, Button, Card, Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion, faBookOpen } from '@fortawesome/free-solid-svg-icons'


import { WordCard } from './WordCard'; 
import { SearchBar } from './SearchBar'; 
import { About } from './About'; 

class WordTable extends React.Component {
  render() {

    const filterText = this.props.filterText;
    const rows = [];

    this.props.words.forEach((word) => {
      rows.push(
        <WordCard
          word={word}
          key={word.id} 
        />
      );
    });

    if (this.props.loading) {
       return (< Card.Columns style={{opacity: 0.5}}>{rows}</Card.Columns>);
    } else {
       return (< Card.Columns>{rows}</Card.Columns>);
    }
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
      <div style={{height:"9rem"}}>
       
          <Navbar expand="lg" dark bg="dark" fixed="top" mb="5">
          <Container>
          <Navbar.Brand>
            <h2  className='text-info'  >
            <FontAwesomeIcon icon={faBookOpen} size="lg"  /> Šanakniiga</h2></Navbar.Brand>
            <ButtonGroup  className='float-right'>
              <Button disabled={true} className='btn-light' size="lg" ><FontAwesomeIcon icon={faCogs} size="lg" /></Button>
            &nbsp;  
            <About />
            </ButtonGroup>
           
           </Container>
          </Navbar>

      </div>
      <Container>
        <SearchBar
          filterText={this.state.filterText}
          onFilterTextChange={this.handleFilterTextChange}
          loading={this.state.loading}
          word_count={this.state.words.length}
        />
      </Container>
      <Container>
        <WordTable
          words={this.state.words}
          filterText={this.state.filterText}
          loading={this.state.loading}
        />
      </Container>
      </div>
    );
  }
}

document.body.classList.add('bg-light');
ReactDOM.render(
  <FilterableWordTable />,
  document.getElementById('app')
);