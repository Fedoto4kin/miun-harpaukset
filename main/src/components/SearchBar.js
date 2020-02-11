import React, { Component } from "react";
import { Form, InputGroup, Button,  Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'


export default class SearchBar extends React.Component {

  constructor(props) {
    super(props);
    this.handleFilterTextChange = this.handleFilterTextChange.bind(this);
    this.handleFilterTextKeyPress = this.handleFilterTextKeyPress.bind(this);
    this.handleButtonClick = this.handleButtonClick.bind(this);
  }
  
  handleFilterTextChange(e) {
    this.props.onFilterTextChange(e.target.value);
  }
  
  handleFilterTextKeyPress(e) {
    this.props.onFilterTextKeyPress(e);
  }

  handleButtonClick(e) {
    this.props.onClickButton(e);
  }

  render() {


    return (

       <Form className="w-100">
        <Form.Group> 
      
       <InputGroup className='input-group-lg'>
       <React.Fragment>
         <Form.Input  type="text" 
            placeholder="Täššä zavodikkua kirjuttua, štobi eččie šanakniigašša" 
            value={this.props.filterText}
            onChange={this.handleFilterTextChange} 
            onKeyPress={this.handleFilterTextKeyPress}
            className='input-lg'
          />

        </React.Fragment>
        <InputGroup.Append >
          <Button className='btn-dark' onClick={this.handleButtonClick}>
            <FontAwesomeIcon icon={faSearch} />
          </Button>
        </InputGroup.Append>
      </InputGroup>
      </Form.Group>
      </Form>
 
    );
  }
}
