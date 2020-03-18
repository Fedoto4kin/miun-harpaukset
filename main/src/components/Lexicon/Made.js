import React from 'react';
import ReactDOM from "react-dom";
import Modal from 'react-bootstrap4-modal';
import { Button, Container, ListGroup, Badge } from 'bootstrap-4-react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEnvelope} from '@fortawesome/free-solid-svg-icons'


export default class Made extends React.Component {
  
  constructor(props) {
       super(props);
      this.state = {
        open: false,
      };   
     
  }

  closeModal() { this.setState({ open: false }); };

  openModal() { this.setState({ open: true }); };

  render(){

    return (
      <div>
      <Modal visible={this.state.open} onClickBackdrop={this.modalBackdropClicked}>
        <div className="modal-header" >
          <h5 className="modal-title">Luadijat</h5>
          <button type="button" className="close"  onClick={this.closeModal.bind(this)}><span aria-hidden="true">×</span><span className="sr-only">Close</span></button>
        </div>
        <div className="modal-body">
        <p>Web-programmista:<br/><b>Anatolii Fedotočkin</b> (<FontAwesomeIcon icon={faEnvelope} size="sm" /> <a href='mailto:anatole@fedotochkin.ru'>anatole@fedotochkin.ru</a>)</p>
        <p>Šanakniigan keriäjät:<br/> <b>Irina Novak</b>, <b>Irina Komissarova</b></p>
        <p>Iänehlugija:<br/> <b>Irina Komissarova</b><br/>
                <a href='https://vk.com/startmusictver' target='_blank'>StArt-iänehstudija</a>, Tveri-linna</p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-outline-secondary btn-block" onClick={this.closeModal.bind(this)} >
            šalvata
          </button>
        </div>
      </Modal>
      <Button  onClick={this.openModal.bind(this)} className='btn btn-dark' size="lg" >Luadijat</Button>
      </div>
    )
  }
}
