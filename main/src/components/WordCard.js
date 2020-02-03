import React, { Component } from "react";
import ReactHtmlParser from 'react-html-parser'; 
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeadphones } from '@fortawesome/free-solid-svg-icons'
import { Navbar, Form, InputGroup, Button, Card, Container, Badge, ListGroup } from 'bootstrap-4-react';


class WordCard extends React.Component {

  render() {

    const word = this.props.word;
    const definition = word.definition;
    let _nice_word = word.word.replace('|', '<span class="text-muted font-weight-normal">|</span>');
    
    return (

       <Card bg="dark" text="white" id={word.id}>
        <Card.Header className="clearfix">
        <Badge className="badge-info float-right"><i>{word.pos}</i></Badge>
        <h5><a className='text-muted'><FontAwesomeIcon icon={faHeadphones} /></a>&nbsp;{ReactHtmlParser (_nice_word) }</h5>
        </Card.Header>
        <Card.Body>
          <ListGroup variant="flush">
              { definition.map( 
                (definition, index) => 
                (
      <ListGroup.Item key={index} bg="secondary"  className='clearfix border-dark border'>
       <Badge pill bg="dark" className='float-right' >{definition.lang}</Badge>
        {definition.definition}  
      </ListGroup.Item>
                )) }
             
          </ListGroup>
        </Card.Body>
      </Card>
    );
  }
}

export {WordCard};