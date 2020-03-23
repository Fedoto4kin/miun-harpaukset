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
      inputCursor: 0
    };

    this.searchInput = React.createRef();

  }

  handleSearchButtonClick(e) {
    this.props.pushSearchStr(this.state.searchText, this.state.reverse);
    this.searchInput.current.focus();
    e.preventDefault();
  }

  componentDidUpdate() {
    this.searchInput.current.focus();
    this.searchInput.current.selectionStart = this.state.inputCursor;
    this.searchInput.current.selectionEnd = this.state.inputCursor;
  }


  handleDiacrtButtonClick(e) {
    
    let position =  this.searchInput.current.selectionStart;
    let updated_text = [this.state.searchText.slice(0, position),
                        e.target.dataset.char, 
                        this.state.searchText.slice(position)].join('');

    this.setState({
     searchText: updated_text,
     inputCursor: position+1 
    }); 
   
  }

  handleSearchTextChange(e) {

    this.setState({ 
        inputCursor: this.searchInput.current.selectionStart,
        searchText: e.target.value
    }); 
  }

  
  handleFilterTextKeyPress(e) {
    this.setState({ inputCursor: this.searchInput.current.selectionStart }); 
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
               <input  type="text" 
                  className='form-control'
                  placeholder="Zavodikkua kirjuttua täššä, štobi löydiä šanan šanakniigašta" 
                  value={this.state.searchText}
                  ref={this.searchInput}
                  onChange={this.handleSearchTextChange.bind(this)} 
                  autoFocus={true}
                  onKeyPress={this.handleFilterTextKeyPress.bind(this)}
                />

              </React.Fragment>
                <InputGroup.Append>
                <span data-char='č' className='btn btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  č
                </span> 
                <span data-char='š' className='btn btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  š
                </span> 
                <span data-char='ž' className='btn btn-secondary' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ž
                </span> 
                <span data-char='ä' className='btn btn-dark' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ä
                </span>                
                <span data-char='ö' className='btn btn-dark' onClick={this.handleDiacrtButtonClick.bind(this)}>
                  ö
                </span>                
               
               
               
 
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
