import React from 'react';
import ReactDOM from "react-dom";
import Modal from 'react-bootstrap4-modal';
import axios from 'axios';
import { Button, Container, ListGroup, Badge } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion} from '@fortawesome/free-solid-svg-icons'

class About extends React.Component {
  
  constructor(props) {
      super(props);
      this.state = {
        open: false,
        pos: []
      };   
      axios.get("/api/v0/lexicon/pos/")
        .then((response) => {
          this.setState({ 'pos': response.data  });
        });
    }

  closeModal() { this.setState({ open: false }); };

  openModal() { this.setState({ open: true }); };

  render(){
    
    const listItems = this.state.pos.map((pos) =>  <ListGroup.Item key={pos.id} ><Badge  className="badge-info"><i>{pos.abbr}</i></Badge> {pos.name_ru} &mdash; {pos.name_fi}  </ListGroup.Item> );

    return (
      <div>
      <Modal visible={this.state.open} onClickBackdrop={this.modalBackdropClicked}>
        <div className="modal-header" >
          <h5 className="modal-title">Lyhenešanoih näh</h5>
          <button type="button" className="close"  onClick={this.closeModal.bind(this)}><span aria-hidden="true">×</span><span className="sr-only">Close</span></button>
        </div>
        <div className="modal-body">
        <ListGroup>
        {listItems}
        </ListGroup>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-outline-secondary btn-block" onClick={this.closeModal.bind(this)} >
            Ymmärdän
          </button>
        </div>
      </Modal>
      <Button  onClick={this.openModal.bind(this)} className='btn-info' size="lg" ><FontAwesomeIcon icon={faQuestion} size="lg" /></Button>
      </div>
    )
  }
}
export {About};