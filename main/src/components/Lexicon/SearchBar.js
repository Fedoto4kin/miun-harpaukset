import React, { Component } from "react";
import { Form, InputGroup, Button,  Container, Dropdown } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import BootstrapSwitchButton from 'bootstrap-switch-button-react'

export default class SearchBar extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      searchText: this.props.search,
      reverse: this.props.reverse,
    };
  }

  handleButtonClick(e) {
    this.props.pushSearchStr(this.state.searchText, this.state.reverse);
    e.preventDefault();
  }

  handleSearchTextChange(e) {
    this.setState({ searchText: e.target.value}); 
  }
  
  handleFilterTextKeyPress(e) {
    if(e.charCode==13){
      this.props.pushSearchStr(e.target.value, this.state.reverse);
      e.preventDefault();
    }
  }

  render() {


    return (

       <Form className="w-100">
        <Form.Group> 
             <InputGroup>
                    <BootstrapSwitchButton
                      width='180'
                      checked={this.state.reverse}
                      offlabel='Karielan šana'
                      onlabel="Kiäneššä"
                      offstyle="primary" 
                      onstyle="warning" 
                      onChange={(checked) => {this.setState({ reverse: checked }) }}
                  />

             <React.Fragment>
               <Form.Input  type="text" 
                  placeholder="Zavodikkua kirjuttua täššä, štobi löydiä šanan šanakniigašta" 
                  value={this.state.searchText}
                  onChange={this.handleSearchTextChange.bind(this)} 
                  onKeyPress={this.handleFilterTextKeyPress.bind(this)}
                />

              </React.Fragment>
                <InputGroup.Append>

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
