import 'dotenv/config'
import cors from 'cors';
import express from 'express';
import expressWebsockets from 'express-ws';
import Reveal from 'reveal.js';
import path from 'path';
import fileStore from './fileStore';
import { spawnPython, execPython } from './utils/script';

const serverPort = parseInt(process.env.SERVER_PORT || '8080');
const storageBucket: typeof fileStore = fileStore;

const { app } = expressWebsockets(express());

app.use(cors());
app.use(express.json());

app.all('/*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

app.post('/parser', async (req, res) => {
    // Get script
    const data = req.body;
    let script = data.script;
    script = script.replace('&lt;', '<');
    script = script.replace('&gt;', '>');

    // Send parsed frames to client
    const frames = await spawnPython('utils/parse.py', script);
    if (!frames) return res.status(400);
    return res.status(200).json({ frames: `${frames}`.trim() });
});

app.post('/compiler', async (req, res) => {
    const data = req.body;
    const fileName = data.fileName;
    const TEMP = 'tmp';

    // Write json
    const file  = storageBucket.file(`${fileName}.json`);
    await file.save(JSON.stringify(data, null, 2), {
        metadata: {
            contentType: 'application/json',
            contentLength: undefined,
        }
    });

    // Write html and send presentation link to client
    await execPython('utils/compile.py', `${TEMP}/${fileName}.json`, `${TEMP}/${fileName}.html`);

    return res.status(200).json({ link: `s/${fileName}.html` });
});

// Serving presentation through reveal.js
const TEMP = path.join(__dirname, 'tmp');
const REVEAL_JS_PATH = path.join(__dirname, 'node_modules', 'reveal.js'); 
app.use('/s', express.static(TEMP));
app.use('/s/dist', express.static(path.join(REVEAL_JS_PATH, 'dist')));
app.use('/s/plugin', express.static(path.join(REVEAL_JS_PATH, 'plugin')));

app.listen(Number(serverPort), () => console.log(`Listening on localhost:${serverPort}`));