import React, { Component } from "react";
import { Link  } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeadphones } from '@fortawesome/free-solid-svg-icons'
import { Navbar, Form, InputGroup, Button, Card, Container, Badge, ListGroup } from 'bootstrap-4-react';
import ReactTooltip from 'react-tooltip';

export default class WordCard extends React.Component {

  constructor(props) {
    super(props);
    this.soundRef = React.createRef();
  }

  playAudio() {
    this.soundRef.current.play();
    return false;
  }

  render() {

    const word = this.props.word;

    const definition = word.definition.reduce(function (r, a) {
        r[a.lang] = r[a.lang] || [];
        r[a.lang].push(a.definition);
        return r;
    }, Object.create(null));

    let alias;
    let pos_tooltip = word.pos_name_ru + ' | ' + word.pos_name_fi;
    let nice_word = word.word.replace('|', '');
      
    if (word.alias_words.length) {
        alias = word.alias_words.map((d) => <Badge ml={2} className='badge-light' key={d.id}>{d.word.replace('|', '')}</Badge>) 
    }

    return (

       <Card bg="dark" text="white" id={word.id} >
        <Card.Header className="clearfix">
            <Badge className="badge-info float-right word-pos" data-tip={pos_tooltip}><i>{word.pos}</i></Badge>
        <h5 className='word'>
            <Button className='btn-sm btn-outline-warning sound-btn' 
                    onClick={this.playAudio.bind(this)}><FontAwesomeIcon icon={faHeadphones} />
              </Button>&nbsp;{ nice_word }</h5>
          <audio ref={this.soundRef}>
            <source src={word.speech}>
          </source>
        </audio>
        </Card.Header>
        <Card.Body>
         <ListGroup variant="flush" className='word-translate'>
            { Object.entries(definition).map((t,k) => 
              <ListGroup.Item key={k} bg="secondary" className='clearfix border-dark border' pl='4'>
               <Badge pill bg="dark" className='float-right' ><img src={`/static/img/${t[0]}-xs.png`} alt={t[0]} /></Badge>
               {t[1].length > 1 ? 
                <ol className="list-group-numbered list-group">
                  {t[1].map((m, i) => <li key={i}>{m}</li>)}
                </ol>: 
                  t[1]
               }
               </ListGroup.Item>
              )}  
          </ListGroup>
        </Card.Body>
        <Card.Footer>
          { alias &&
            <div className='word-alias'><span  className='text-light small'>Šama kuin:</span>{alias}</div>
          }
        </Card.Footer>
        <ReactTooltip  place="top" type="light" border={true} effect="solid" />
      </Card>
    );
  }
}