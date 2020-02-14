import React, { Component } from "react";
import { Form, InputGroup, Button,  Container } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'


export default class SearchBar extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      searchText: this.props.search,
    };
  }


  handleButtonClick(e) {
    this.props.pushSearchStr(this.state.searchText);
    e.preventDefault();
  }

  handleSearchTextChange(e) {
    this.setState({ searchText: e.target.value}); 
  }
  
  handleFilterTextKeyPress(e) {
    if(e.charCode==13){
      this.props.pushSearchStr(e.target.value);
      e.preventDefault();
    }
  }

  render() {


    return (

       <Form className="w-100">
        <Form.Group> 
      
       <InputGroup className='input-group-lg'>
       <React.Fragment>
         <Form.Input  type="text" 
            placeholder="Täššä zavodikkua kirjuttua, štobi eččie šanakniigašša" 
            value={this.state.searchText}
            onChange={this.handleSearchTextChange.bind(this)} 
            onKeyPress={this.handleFilterTextKeyPress.bind(this)}
            className='input-lg'
          />

        </React.Fragment>
        <InputGroup.Append >
          <Button className='btn-dark' onClick={this.handleButtonClick.bind(this)}>
            <FontAwesomeIcon icon={faSearch} />
          </Button>
        </InputGroup.Append>
      </InputGroup>
      </Form.Group>
      </Form>
 
    );
  }
}
