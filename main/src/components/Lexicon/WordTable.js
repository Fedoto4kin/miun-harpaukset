import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Card, Container, Alert, Row, Col} from 'bootstrap-4-react';
import { PointSpreadLoading } from 'react-loadingg';
import axios from 'axios';

const WordCard = React.lazy(() => import('./WordCard'));

export default  class WordTable extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      'words': [],
      'loading': false
    };
  }

  componentDidMount() {
    if (this.props.search) this._search(this.props.search);
  }

  UNSAFE_componentWillReceiveProps(nextProps) {
    if (this.props.search !== nextProps.search) this._search(nextProps.search)
  }

  _search(search) {

    this.setState({loading: !this.state.loading}); 

    axios.get("/api/v0/lexicon/", { params: {search: search}})
      .then((response) => {
        this.setState({ 'words': response.data  });
        this.setState({loading: false}); 
    });
  }

  render() {

      const rows = [];

      const wordCount = this.state.words.length;
      let message = null;

      if (this.props.search && !this.state.loading) {
        if (wordCount) {
          message = 'Löydy ' + wordCount;
          message += ((wordCount > 1) ?  ' šanua': ' šana')
        } else message = 'Ei nimidä löydyn';             
      }

    
      this.state.words.forEach((word) => {
        rows.push(
          <React.Suspense key={word.id}>
           <Col md={6} sm={12} lg={4} pb={2}>
            <WordCard word={word}  />
            </Col>
          </React.Suspense>
        
        );
      });

      return (

        <Container className='position-relative' style={{minHeight: '8em'}}>
          { !this.state.loading ?
          <div>
            { message && <Alert className='text-center alert alert-secondary show'>{message}</Alert> }
            <Row>{rows}</Row>
          </div> :
             <PointSpreadLoading size='large' color='#17a2b8'/>
          }
          
        </Container>
      );
  }
}
