import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Button, ListGroup, Badge } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faInfoCircle, faChevronLeft, faChevronCircleRight, faThumbsUp  } from '@fortawesome/free-solid-svg-icons'
import ReactTooltip from 'react-tooltip';
import Joyride, { ACTIONS, EVENTS, LIFECYCLE, STATUS } from 'react-joyride';


export default class LexiconTour extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      run: false,
      stepIndex: 1,
      steps: [
        {
          content: (
               <div>
                    <h2>Tulgua tervehenä!</h2>
                    <ListGroup  variant="flush" >
                        <ListGroup.Item className='clearfix border-secondary border'>
                        <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-md.png`}  /></Badge>
                        Это словарь современного тверского карельского языка.<br /> 
                        В нем почти 3000 слов базовой лексики.<br /> 
                        И сейчас мы вам покажем как им пользоваться.<br />
                        Нажмите <strong> edeh <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong> 
                        чтобы начать знакомство со словарем.
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-md.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),

          locale: { next: <strong >edeh <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong> },
          placement: 'center',
          target: 'body',
          styles: {
            options: {
              width: 600,
              textAlign: 'left',
            },
          },
        },
        {
          content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                        Направление поиска:<br /> 
                        <span className='btn btn-primary btn-xs'>Karielan šana</span> по карельским словам <br />
                        <span className='btn btn-warning btn-xs'>Kiännökšeššä</span> по значению слов в финском или русском языке
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
          locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.search-bar-switcher'
        },
        {
          content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                        Вводим слово целиком или только его основу для поиска всех возможных вариантов.<br />
                        Например, <mark>kebi...</mark><br />
                        Карельские слова можно искать даже по нескольким первым буквам, 
                        слова в переводе только по полному совпадению
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
          locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.search-bar-input',
        },
        {
          content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                          Если не хватает &laquo;карельских&raquo; букв на клавиатуре, можно взять отсюда
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
          locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.krl-letters',   
        },  
        {
          content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                          Жмем чтобы начать поиск<br />
                          (или клавишу Enter)
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
          locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.search-run',   
        },
        {
           content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                            Одно из найденных слов
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
         locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.word',
          placement: 'right',
        },   
        {
          content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                            Можно послушать как слово правильно произносится
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
         locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.sound-btn',
        },   
        {
           content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                            Варианты перевода на русский и финский языки
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
        locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.word-translate',
          placement: 'right',
        },           
        {
           content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                            Часть речи
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
        locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh  <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.word-pos',
          placement: 'right',
        },
        {
           content:  (
               <div>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border small'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-sm.png`}  /></Badge>
                            Синонимы
                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border small'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-sm.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
               </div>
            ),
          locale: { back: <strong ><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    next: <strong >edeh <FontAwesomeIcon icon={faChevronCircleRight} size="lg" /></strong>  },
          target: '.word-alias',
          placement: 'top',
        },
        {
          content:  (
               <div>
                    <h4>
                        Opaštukkua karielan kieldä!<br />
                        Paiskua karielakši!
                    </h4>
                    <ListGroup  variant="flush">
                        <ListGroup.Item className='clearfix border-secondary border'>
                         <Badge pill bg="light" className='float-right' ><img src={`/static/img/ru-md.png`}  /></Badge>
                           Пользуйтесь с удовольствием! Учите карельский язык!<br />
                           <hr /> 
                           Работа над словарем продолжается.<br />
                           Ждем любые пожелания и предложения на почту  <a href='mailto:anatole@fedotochkin.ru'>anatole@fedotochkin.ru</a>

                        </ListGroup.Item>
                        <ListGroup.Item className='clearfix border-secondary border'>
                          <Badge pill bg="light" className='float-right' ><img src={`/static/img/fi-md.png`}  /></Badge>
                        % Sama asiat, suomea % 
                        </ListGroup.Item>
                    </ListGroup>
                
               </div>
            ),
          styles: {
            options: {
              width: 600,
              textAlign: 'left',
            },
          },
          locale: { back: <strong><FontAwesomeIcon icon={faChevronLeft} size="lg" /> tagah</strong>,
                    last: <strong aria-label="skip"><FontAwesomeIcon icon={faThumbsUp} size="lg" /> maltan</strong> },
          target: 'body',
          placement: 'center',

        }
      ]

    };
 
  }

   handleJoyrideCallback = data => {

    const { action, index, status, type } = data;

    if ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND].includes(type)) {
      this.setState({ stepIndex: index + (action === ACTIONS.PREV ? -1 : 1) });
    }
    else if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      this.setState({ run: false });
    }

    console.groupCollapsed(type);
    console.log(data); //eslint-disable-line no-console
    console.groupEnd();
  };


  handleClickStart(e) {

    this.props.pushSearchStr('kebi', false);
    this.setState({
      run: true,
    });
  };

  render() {

    const { run, steps, stepIndex } = this.state;
    const { breakpoint } = this.props;

    return (
    <div>
     <Button className='btn-primary btn-lg' data-tip='Abu' data-for='help-button' 
             onClick={this.handleClickStart.bind(this)}>
        <FontAwesomeIcon icon={faInfoCircle} size="lg" />
     </Button>
      <ReactTooltip id='help-button' place="left" type="info" border={true} effect="solid" />
      <Joyride steps={steps} 
                run={run}
                continuous={true}
                scrollToFirstStep={true}
                showProgress={true}
                callback={this.handleJoyrideCallback}
                 styles={{
                        options: {
                              overlayColor: 'rgba(52, 58, 64, 0.4)',
                              primaryColor: '#000',
                              textColor: '#343a40',
                              zIndex: 9000,
                            }
                 }}
      />
      </div>
    );
  }
}
