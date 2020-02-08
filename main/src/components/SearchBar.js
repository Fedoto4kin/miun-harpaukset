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
    let suggestionsListComponent;
    
    return (

       <Form className="mx-2 d-inline w-100">
        <Form.Group> 
      
       <InputGroup className='input-group-lg'>
       <React.Fragment>
         <Form.Input  type="text" 
            placeholder="Täššä zavodikkua kirjuttua, štobi eččie šanakniigašša" 
            value={this.props.filterText}
            onChange={this.handleFilterTextChange} 
            className='input-lg'
          />
          {suggestionsListComponent}
        </React.Fragment>
        <InputGroup.Append >
          <InputGroup.Text>
           {this.props.loading ?
            <span className="spinner-border   text-secondary"></span>:
            <FontAwesomeIcon icon={faSearch} />
          }
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
      </Form.Group>
      </Form>
 
    );
  }
}

export {SearchBar};