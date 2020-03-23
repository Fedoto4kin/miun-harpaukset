import React from 'react';
import ReactDOM from "react-dom";
import Modal from 'react-bootstrap4-modal';
import axios from 'axios';
import { Button, Container, Badge } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCogs, faQuestion} from '@fortawesome/free-solid-svg-icons'

export default class About extends React.Component {
  
  constructor(props) {
      super(props);
      this.state = {
        open: false,
        pos: []
      };   
     
  }

  componentDidMount() {

     axios.get("/api/v0/lexicon/pos/")
        .then((response) => {
          this.setState({ 'pos': response.data  });
        });
  }

  closeModal() { this.setState({ open: false }); };

  openModal() { this.setState({ open: true }); };

  render(){
    
    const listItems = this.state.pos.map((pos) =>  <tr key={pos.id} ><td><Badge  className="badge-info"><i>{pos.abbr}</i></Badge></td><td>{pos.name_ru}</td><td>{pos.name_fi}</td></tr> );

    return (
      <div>
      <Modal visible={this.state.open} onClickBackdrop={this.modalBackdropClicked}>
        <div className="modal-header" >
          <h5 className="modal-title">Lyhennettyöh šanoih näh</h5>
          <button type="button" className="close"  onClick={this.closeModal.bind(this)}><span aria-hidden="true">×</span><span className="sr-only">Close</span></button>
        </div>
        <div className="modal-body">

            <table className='table table-borderless'>
            {listItems}
            </table>

        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-outline-secondary btn-block" onClick={this.closeModal.bind(this)} >
            maltan
          </button>
        </div>
      </Modal>
      <Button  onClick={this.openModal.bind(this)} className='btn-info' size="lg" ><FontAwesomeIcon icon={faQuestion} size="lg" /></Button>
      </div>
    )
  }
}
