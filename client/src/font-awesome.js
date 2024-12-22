// src/font-awesome.js
import { library } from '@fortawesome/fontawesome-svg-core';
import { faVolumeUp, faBook, faStar, faSpinner} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faVolumeUp, faBook, faStar, faSpinner)

export { FontAwesomeIcon };
