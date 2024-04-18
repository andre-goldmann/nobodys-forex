// import WSReqonet from '../../../lib/index.js';
import WSReqonet from 'ws-reqonet';
import { v4 as uuid } from 'uuid';

// Real
//const API_URL = 'http://127.0.0.1:8000';
// Mock
//const API_URL = 'http://127.0.0.1:6081';
// Prod:
const API_URL = 'https://85.215.32.163:6081';

export default function websocket(): WSReqonet {
    const id: string = uuid();
    const SERVER_URL = `${API_URL.replace(/http/, 'ws')}/ws/` + id;
    return new WSReqonet(SERVER_URL, [], { debug: true });
}

export { WSReqonet as Websocket };