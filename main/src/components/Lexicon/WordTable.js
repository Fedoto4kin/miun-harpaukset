import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Card, Container, Alert, Row, Col} from 'bootstrap-4-react';
import { PointSpreadLoading } from 'react-loadingg';
import axios from 'axios';
import BottomScrollListener  from 'react-bottom-scroll-listener';

const WordCard = React.lazy(() => import('./WordCard'));

export default  class WordTable extends React.Component {

  constructor(props) {

    const url = "/api/v0/lexicon/";
    super(props);
    this.state = {
      'data': {results: [],
               next: false},
      'count': 0,
      'searching': false,
      'loading': false,
      'page': 1
    };
  }

  componentDidMount() {
    if (this.props.search) {
      this._search(this.props.search, this.props.reverse);
    }
  }

  UNSAFE_componentWillReceiveProps(nextProps) {
    //if ((this.props.search !== nextProps.search) || (this.props.reverse !== nextProps.reverse)) this._search(nextProps.search)
    this._search(nextProps.search, nextProps.reverse)
  }

  loadMore() {
     console.log('Bottom')
  }

  _search(search, reverse) {

    this.setState({searching: !this.state.searching});
    let params = {search: search}
    params.page = 1;
    if (reverse) params.reverse = true

    axios.get("/api/v0/lexicon/", {params: params})
      .then((response) => {
        let data = {
          'results': response.data.results,
          'next': !!response.data.next
        }
        this.setState({'count': response.data.count})
        this.setState({'data': data });
        this.setState({searching: false}); 
       
    });
  }

  uploadMore = () => {
  
    if (this.state.data.next) {
        this.setState({loading: !this.state.loading});
        this.setState({page: this.state.page + 1 });

        let params = {search: this.props.search}
        params.page = this.state.page;
        if (this.props.reverse) params.reverse = true

        axios.get("/api/v0/lexicon/", {params: params})
          .then((response) => {
            let data = {
              'results': this.state.data.results.concat(response.data.results),
              'next': !!response.data.next
            }
            this.setState({'data': data });
            this.setState({loading: false}); 
        });
    }
  
  }

  render() {

      const rows = [];
      const wordCount = this.state.count;
      let message = null;

      if (this.props.search && !this.state.searching) {
        if (wordCount) {
          message = 'Löydy ' + wordCount;
          message += ((wordCount > 1) ?  ' šanua': ' šana')
        } else message = 'Ei nimidä löydyn';             
      }

    
      this.state.data.results.forEach((word) => {
        rows.push(
          <React.Suspense key={word.id}>
           <Col md={6} sm={12} lg={4} pb={2}>
            <WordCard word={word} />
            </Col>
          </React.Suspense>
        
        );
      });

      return (

        <Container className='position-relative' style={{minHeight: '8em'}}>
          { !this.state.searching ?
          <div>
            { message && <Alert className='text-center alert alert-secondary show'>{message}</Alert> }
            <Row>{rows}</Row>
           </div> :
             <PointSpreadLoading size='large' color='#17a2b8'/>
          }
          { this.state.data.next  &&
             <div className='position-relative' style={{minHeight: '8em'}}>
            { this.state.loading == true && <PointSpreadLoading size='large' color='#17a2b8'/>}</div>
          }
          <BottomScrollListener onBottom={this.uploadMore} />
        </Container>
      );
  }
}
