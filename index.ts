import 'dotenv/config'
import cors from 'cors';
import express from 'express';
import expressWebsockets from 'express-ws';
import path from 'path';
import fileStore from './fileStore';
import { spawnPython, execPython } from './utils/script';

const serverPort = parseInt(process.env.PORT || process.env.SERVER_PORT || '8080');
const storageBucket: typeof fileStore = fileStore;
const UI = './ui/dist';
const TEMP = '../tmp';
const REVEAL = '../node_modules/reveal.js';

const { app } = expressWebsockets(express());

app.use(cors());
app.use(express.json({ limit: '50mb' }));

app.all('/*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

app.get('/api/health', (_, response) => {
    response.send({
        status: 'Healthy'
    });
});

app.post('/api/parser', async (req, res) => {
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

app.post('/api/compiler', async (req, res) => {
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
app.use('/api/s', express.static(path.join(__dirname, TEMP)));
app.use('/api/s/dist', express.static(path.join(__dirname, REVEAL, 'dist')));
app.use('/api/s/plugin', express.static(path.join(__dirname, REVEAL, 'plugin')));
app.get('/api/s/:file', function(req, res) {
    res.sendFile(path.join(__dirname, TEMP, req.params.file));
});

// Serving UI on index.html
app.use('/', express.static(path.join(__dirname, UI), {}))
app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, UI, 'index.html'));
});

app.listen(Number(serverPort), () => console.log(`Listening on localhost:${serverPort}`));