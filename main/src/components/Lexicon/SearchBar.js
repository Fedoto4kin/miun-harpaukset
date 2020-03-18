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

  handleSearchButtonClick(e) {
    this.props.pushSearchStr(this.state.searchText, this.state.reverse);
    e.preventDefault();
  }

  handleDiacrtButtonClick(e) {
     this.setState({ searchText: this.state.searchText + e.target.value }); 
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
                      onlabel="Kiännökšeššä"
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
                <Button value='č' className='btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  č
                </Button> 
                <Button value='š' className='btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  š
                </Button> 
                <Button value='ž' className='btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ž
                </Button> 
                <Button value='ä' className='btn-dark' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ä
                </Button>                
                <Button value='ö' className='btn-dark' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ö
                </Button>                
               
               
               
 
                <Button className='btn-light border-dark' onClick={this.handleSearchButtonClick.bind(this)}>
                  <FontAwesomeIcon icon={faSearch} />
                </Button>
              </InputGroup.Append>

          </InputGroup>
      </Form.Group>
      </Form>
      
 
    );
  }
}
