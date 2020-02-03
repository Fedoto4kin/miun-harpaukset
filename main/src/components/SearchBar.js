import React, { Component } from "react";
import { Form, InputGroup, Button,  Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'


class SearchBar extends React.Component {

  constructor(props) {
    super(props);



    this.handleFilterTextChange = this.handleFilterTextChange.bind(this);
  }
  
  handleFilterTextChange(e) {
    this.props.onFilterTextChange(e.target.value);
  }
  
  render() {

    const wordCount = this.props.word_count;
    let message = '';

    if (this.props.filterText) {
      if (wordCount) {
        message = 'On löydän ' + wordCount;
        message += ((wordCount > 1) ?  ' šanoida': ' šano')
      } else
        message = 'Ei nimidä löydän';
    } 

    return (
     <Container>
       <Form>
        <Form.Group>
      
       <InputGroup className='input-group-lg'>
         <Form.Input  type="text" 
            placeholder="Täššä zavodikkua kirjuttua, štobi eččie šanakniigašša" 
            value={this.props.filterText}
            onChange={this.handleFilterTextChange} 
            className='input-lg'
          />
        <InputGroup.Append>
          <InputGroup.Text><FontAwesomeIcon icon={faSearch} /></InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
      </Form.Group>
      <Form.Group>
        
         {this.props.loading ?
             <div className="spinner-border text-info  "></div>:
             <h5> {message} </h5> }
      
        </Form.Group>
      </Form>
      </Container>
    );
  }
}

export {SearchBar};